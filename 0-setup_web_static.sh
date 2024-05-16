#!/usr/bin/env bash
# Bash script to set up webservers for the deployment of web_static

# check if nginx is already installed
PACKAGE="nginx"
if dpkg -l | grep -q "^ii  $PACKAGE "; then
	echo "$PACKAGE is already installed."
else
	echo "$PACKAGE is not installed. Installing..."

	# upgrade apt
	apt update

	# install nginx non-interactively
	apt install nginx -y
fi

# start nginx
service nginx start

# create directories
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# create fake HTML file with simple content
touch /data/web_static/releases/test/index.html
echo "<h1>Webstatic is live</h1>" > /data/web_static/releases/test/index.html

# create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to the ubuntu user
chown -R ubuntu:ubuntu /data/

# update nginx configuration to serve content of /data/web_static/current to hbnb_static
line_num=$(sed -n '/location \/ {/{=;q;}' /etc/nginx/sites-available/default)
insert_line_num=$((line_num - 1))
sed -i "${insert_line_num}i \\
\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default

# update symbolic link to nginx configuration file
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# restart nginx
service nginx restart

# exit successfully
exit 0
