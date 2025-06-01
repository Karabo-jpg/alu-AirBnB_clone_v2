#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Install nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Create directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a simple HTML file
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

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership and permissions
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/

# Configure nginx
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current/;
    }
}
EOF

# Create symbolic link if it doesn't exist
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Test and restart nginx
nginx -t
service nginx restart

# Wait for nginx to start
sleep 2

# Test the configuration
curl -s http://localhost/hbnb_static/index.html > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: /hbnb_static is not properly configured"
    echo "Debugging information:"
    ls -l /data/web_static/current/
    ls -l /data/web_static/releases/test/
    curl -v http://localhost/hbnb_static/index.html
    cat /var/log/nginx/error.log
    exit 1
fi

exit 0 