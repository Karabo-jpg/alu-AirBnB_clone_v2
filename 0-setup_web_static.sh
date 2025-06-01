#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

# Exit on any error
set -e

# Function to check command success
check_command() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Get current user
CURRENT_USER=$(whoami)
CURRENT_GROUP=$(id -gn)

# Install nginx if not already installed
sudo apt-get -y update
check_command "apt-get update"
sudo apt-get -y install nginx
check_command "nginx installation"

# Stop Apache if it's running (it conflicts with nginx on port 80)
if systemctl is-active apache2 >/dev/null 2>&1; then
    sudo service apache2 stop
    sudo systemctl disable apache2
fi

# Create directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
check_command "creating test directory"
sudo mkdir -p /data/web_static/shared/
check_command "creating shared directory"

# Create a simple HTML file
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null
check_command "creating index.html"

# Create or recreate symbolic link
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current
check_command "creating symbolic link"

# Set permissions
sudo chown -R "$CURRENT_USER:$CURRENT_GROUP" /data/
sudo chmod -R 755 /data/
check_command "setting permissions"

# Configure nginx
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
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF'
check_command "creating nginx configuration"

# Ensure default site is enabled
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
check_command "enabling nginx site"

# Create test index
sudo mkdir -p /var/www/html
echo "Nginx is running" | sudo tee /var/www/html/index.html > /dev/null

# Stop nginx if running
sudo service nginx stop || true

# Start nginx
sudo service nginx start
check_command "starting nginx"

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

# Test nginx response
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html)
if [ "$response" != "200" ]; then
    echo "Error: Nginx configuration failed (Status: $response)"
    echo "Debugging information:"
    echo "Nginx error log:"
    sudo tail /var/log/nginx/error.log
    echo "Nginx configuration test:"
    sudo nginx -t
    echo "Listening ports:"
    sudo netstat -tuln | grep LISTEN
    exit 1
fi

echo "Setup completed successfully"
exit 0 