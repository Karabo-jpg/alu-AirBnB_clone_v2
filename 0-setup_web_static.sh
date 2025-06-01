#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Exit on error
set -e

apt-get -y update
apt-get -y install nginx
service nginx start

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

service nginx restart

exit 0 