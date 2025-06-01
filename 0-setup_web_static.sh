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

# Get current user
CURRENT_USER=$(whoami)
CURRENT_GROUP=$(id -gn)

# Set permissions
chown -R "$CURRENT_USER":"$CURRENT_GROUP" /data/
chmod -R 755 /data/
find /data/ -type f -exec chmod 644 {} \;

# Backup default nginx configuration
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak

# Create new nginx configuration
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        autoindex off;
    }
}
EOF

# Enable the site if not already enabled
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Remove the default symbolic link if it exists
rm -f /etc/nginx/sites-enabled/default

# Create symbolic link
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

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

# Verify nginx is running
if ! service nginx status >/dev/null; then
    echo "Error: nginx is not running"
    exit 1
fi

# Wait a moment for nginx to fully start
sleep 2

# Test if the configuration is working
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html)
if [ "$response" != "200" ]; then
    echo "Error: /hbnb_static is not properly configured (HTTP response: $response)"
    exit 1
fi

echo "Setup completed successfully"
exit 0 