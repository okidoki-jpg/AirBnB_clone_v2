#!/usr/bin/env bash

apt-get -y update
apt-get -y install nginx

mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test
echo "Page is Live" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/

sed -i 's|name _;|name _;\
\
		location /hbnb_static {\
			alias /data/web_static/current;\
			index index.html;\
		}|' /etc/nginx/sites-available/default

service nginx restart
