#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Install nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Stop Apache if it's running (it conflicts with nginx on port 80)
service apache2 stop
systemctl disable apache2

# Create directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a simple HTML file
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test /data/web_static/current

# Set permissions (using root since we're running with sudo)
chown -R root:root /data/
chmod -R 755 /data/

# Backup default nginx configuration
mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak

# Configure nginx with minimal configuration
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root /var/www/html;
    index index.html index.htm;

    location = / {
        return 200 'Nginx is running\n';
    }

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
        autoindex off;
    }
}
EOF

# Remove any existing enabled sites
rm -rf /etc/nginx/sites-enabled/*

# Enable our site
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Ensure nginx working directory exists
mkdir -p /var/www/html

# Test nginx configuration
nginx -t

# Stop nginx if it's running
service nginx stop

# Start nginx fresh
service nginx start

# Verify setup
echo "Checking configuration..."
if [ ! -d "/data/web_static/releases/test" ]; then
    echo "Error: Test directory not created"
    exit 1
fi

if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    echo "Error: index.html not created"
    exit 1
fi

if [ ! -L "/data/web_static/current" ]; then
    echo "Error: Symbolic link not created"
    exit 1
fi

# Wait a moment for nginx to fully start
sleep 2

# Test nginx response
echo "Testing nginx response..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html)
if [ "$response" != "200" ]; then
    echo "Error: Nginx configuration failed (Status: $response)"
    echo "Debugging information:"
    echo "Directory listing:"
    ls -la /data/web_static/current/
    ls -la /data/web_static/releases/test/
    echo "Nginx error log:"
    tail /var/log/nginx/error.log
    echo "Testing direct access:"
    curl -v http://localhost/hbnb_static/index.html
    echo "Nginx status:"
    service nginx status
    exit 1
fi

echo "Setup completed successfully"
exit 0 