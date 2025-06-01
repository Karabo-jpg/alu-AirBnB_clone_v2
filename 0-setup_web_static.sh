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

# Configure nginx with minimal configuration
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80;
    listen [::]:80;
    server_name localhost;

    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Remove any existing enabled sites
rm -rf /etc/nginx/sites-enabled/*

# Enable our site
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Ensure nginx working directory exists
mkdir -p /var/www/html

# Create a test index file
echo "Nginx is running" > /var/www/html/index.html

# Stop nginx completely
service nginx stop
killall nginx

# Start nginx fresh
service nginx start

# Wait for nginx to start
sleep 5

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

# Test nginx response
echo "Testing nginx response..."
echo "Checking nginx process:"
ps aux | grep nginx
echo "Checking port 80:"
netstat -tuln | grep :80
echo "Testing connection:"
curl -v http://127.0.0.1/hbnb_static/index.html

# Final test
response=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/hbnb_static/index.html)
if [ "$response" != "200" ]; then
    echo "Error: Nginx configuration failed (Status: $response)"
    echo "Debugging information:"
    echo "Directory listing:"
    ls -la /data/web_static/current/
    ls -la /data/web_static/releases/test/
    echo "Nginx error log:"
    tail /var/log/nginx/error.log
    echo "Nginx access log:"
    tail /var/log/nginx/access.log
    echo "Nginx status:"
    service nginx status
    exit 1
fi

echo "Setup completed successfully"
exit 0 