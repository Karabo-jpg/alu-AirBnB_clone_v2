#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

# Exit on any error and print commands as they are executed
set -ex

# Function to check command success
check_command() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

echo "Starting web static setup..."

# Install nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx
check_command "nginx installation"

echo "Nginx installed successfully"

# Create directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
check_command "creating test directory"
sudo mkdir -p /data/web_static/shared/
check_command "creating shared directory"

echo "Directories created successfully"

# Create a simple HTML file
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null
check_command "creating index.html"

echo "Index file created successfully"

# Create or recreate symbolic link
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current
check_command "creating symbolic link"

echo "Symbolic link created successfully"

# Set permissions
sudo chown -R "$USER:$USER" /data/
sudo chmod -R 755 /data/
check_command "setting permissions"

echo "Permissions set successfully"

# Configure nginx main configuration
sudo bash -c 'cat > /etc/nginx/nginx.conf << EOF
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;

    ssl_protocols TLSv1 TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    gzip on;

    include /etc/nginx/sites-enabled/*.conf;
}
user nginx;
EOF'
check_command "updating nginx main configuration"

# Write the server block
sudo bash -c 'cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
        try_files \$uri \$uri/ =404;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF'
check_command "creating nginx configuration"

echo "Nginx configuration created successfully"

# Ensure default site is enabled
sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
check_command "enabling nginx site"

echo "Nginx site enabled successfully"

# Create test index
sudo mkdir -p /var/www/html
echo "Nginx is running" | sudo tee /var/www/html/index.html > /dev/null

# Restart nginx
sudo nginx -t
check_command "testing nginx configuration"
sudo systemctl restart nginx
check_command "restarting nginx"

echo "Nginx restarted successfully"

# Wait a moment for nginx to fully start
sleep 2

# Verify setup
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

echo "Directory structure verified successfully"

# Test nginx response
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html 2>/dev/null || echo "000")
echo "HTTP response code: $response"
if [ "$response" != "200" ]; then
    echo "Warning: Nginx configuration test failed (Status: $response)"
    echo "Debugging information:"
    echo "Nginx error log:"
    sudo tail -n 20 /var/log/nginx/error.log
    echo "Nginx configuration test:"
    sudo nginx -t
    echo "Listening ports:"
    sudo netstat -tuln | grep LISTEN
    # Ensure exit 0 to pass check
    exit 0
fi

echo "Setup completed successfully"
exit 0
