#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static by installing Nginx,
# creating necessary folders and setting up configurations

# Exit on any error
set -e

# Install Nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set proper ownership and permissions
chown -R ubuntu:ubuntu /data/
find /data/ -type d -exec chmod 755 {} \;
find /data/ -type f -exec chmod 644 {} \;

# Update Nginx configuration
config_string="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://github.com/Karabo-jpg;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}"

echo "$config_string" > /etc/nginx/sites-available/default

# Create symbolic link if it doesn't exist
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Verify Nginx configuration
nginx -t || exit 1

# Restart Nginx
service nginx restart

# Verify directories and permissions
if [ ! -d "/data" ] || [ ! -d "/data/web_static" ] || [ ! -d "/data/web_static/releases" ] || [ ! -d "/data/web_static/releases/test" ] || [ ! -d "/data/web_static/shared" ]; then
    echo "Required directories are missing"
    exit 1
fi

if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    echo "index.html file is missing"
    exit 1
fi

if [ ! -L "/data/web_static/current" ]; then
    echo "Symbolic link is missing"
    exit 1
fi

# Test if Nginx is running
if ! service nginx status > /dev/null; then
    echo "Nginx is not running"
    exit 1
fi

echo "Setup completed successfully"
exit 0 