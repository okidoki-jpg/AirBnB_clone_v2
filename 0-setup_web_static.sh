#!/usr/bin/env bash
# installing and configuring nginx to test aliases

apt-get -y update
apt-get -y install nginx

mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test
echo "Page is Live" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/

sed -i 's|name _;|name _;\
\
		location /hbnb_static {\
			alias /data/web_static/current;\
		}|' /etc/nginx/sites-available/default

service nginx restart
