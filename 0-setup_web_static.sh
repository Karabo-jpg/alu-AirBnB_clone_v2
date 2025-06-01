#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Install nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Create the folder structure
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create test HTML file with proper HTML structure
cat > /data/web_static/releases/test/index.html << EOF
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>
EOF

# Remove current symbolic link if it exists
rm -rf /data/web_static/current

# Create new symbolic link
ln -sf /data/web_static/releases/test /data/web_static/current

# Get current user
CURRENT_USER=$(whoami)
CURRENT_GROUP=$(id -gn)

# Set permissions
chown -R "$CURRENT_USER":"$CURRENT_GROUP" /data/
chmod -R 755 /data/
find /data/ -type f -exec chmod 644 {} \;

# Create nginx configuration
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        try_files \$uri \$uri/ =404;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Create symbolic link for nginx config if it doesn't exist
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Remove default nginx static page
rm -rf /var/www/html/*

# Create new default index.html
echo "Hello World!" > /var/www/html/index.html

# Test nginx configuration
nginx -t

# Restart nginx
service nginx restart

# Wait for nginx to start
sleep 2

# Verify directories exist
if [ ! -d "/data" ] || [ ! -d "/data/web_static" ] || [ ! -d "/data/web_static/releases" ] || [ ! -d "/data/web_static/releases/test" ]; then
    echo "Error: Required directories are missing"
    exit 1
fi

# Verify index.html exists
if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    echo "Error: index.html is missing"
    exit 1
fi

# Verify symbolic link exists
if [ ! -L "/data/web_static/current" ]; then
    echo "Error: Symbolic link is missing"
    exit 1
fi

# Verify nginx is running
if ! service nginx status >/dev/null; then
    echo "Error: nginx is not running"
    exit 1
fi

# Test if the configuration is working
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html)
if [ "$response" != "200" ]; then
    echo "Error: /hbnb_static is not properly configured (HTTP response: $response)"
    # For debugging
    echo "Current nginx error log:"
    tail /var/log/nginx/error.log
    exit 1
fi

echo "Setup completed successfully"
exit 0 