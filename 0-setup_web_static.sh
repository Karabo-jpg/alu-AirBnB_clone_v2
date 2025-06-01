#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static by installing Nginx,
# creating necessary folders and setting up configurations

# Install Nginx if not already installed
apt-get update
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

# Give ownership to ubuntu user and group
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/

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

# Test Nginx configuration and restart
nginx -t
service nginx restart

exit 0 