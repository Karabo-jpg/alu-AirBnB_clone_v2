#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Install nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Create the folder structure
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create test HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Set permissions
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/
find /data/ -type f -exec chmod 644 {} \;

# Update nginx configuration
nginx_conf="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}"

echo "$nginx_conf" > /etc/nginx/sites-available/default

# Enable the site if not already enabled
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Test nginx configuration
nginx -t

# Restart nginx
service nginx restart

# Verify everything is set up correctly
if [ ! -d "/data" ] || [ ! -d "/data/web_static" ] || [ ! -d "/data/web_static/releases" ] || [ ! -d "/data/web_static/releases/test" ]; then
    echo "Error: Required directories are missing"
    exit 1
fi

if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    echo "Error: index.html is missing"
    exit 1
fi

if [ ! -L "/data/web_static/current" ]; then
    echo "Error: Symbolic link is missing"
    exit 1
fi

# Verify permissions
if [ "$(stat -c '%a' /data)" != "755" ] || \
   [ "$(stat -c '%a' /data/web_static)" != "755" ] || \
   [ "$(stat -c '%a' /data/web_static/releases)" != "755" ]; then
    echo "Error: Directory permissions are incorrect"
    exit 1
fi

if [ "$(stat -c '%a' /data/web_static/releases/test/index.html)" != "644" ]; then
    echo "Error: File permissions are incorrect"
    exit 1
fi

# Verify nginx is running and configured
if ! service nginx status >/dev/null; then
    echo "Error: nginx is not running"
    exit 1
fi

if ! curl -s http://localhost/hbnb_static/ | grep -q "Holberton School"; then
    echo "Error: /hbnb_static is not properly configured"
    exit 1
fi

exit 0 