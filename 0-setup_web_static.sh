#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Install nginx if not already installed
apt-get -y update
apt-get -y install nginx

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

# Configure nginx
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }
}" > /etc/nginx/sites-available/default

# Enable the site
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Remove default nginx static page
rm -rf /var/www/html/*
echo "Nginx is running" > /var/www/html/index.html

# Test nginx configuration
nginx -t

# Restart nginx
service nginx restart

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
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html)
if [ "$response" != "200" ]; then
    echo "Error: Nginx configuration failed (Status: $response)"
    echo "Debugging information:"
    ls -l /data/web_static/current/
    ls -l /data/web_static/releases/test/
    cat /var/log/nginx/error.log
    curl -v http://localhost/hbnb_static/index.html
    exit 1
fi

echo "Setup completed successfully"
exit 0 