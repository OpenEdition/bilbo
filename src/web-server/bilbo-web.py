# -*- coding: utf-8 -*-

import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

from bilboweb import bilboWeb, annotate, urls
import web
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()


# Rendre le dossier tmp/ accessible en écriture au serveur web

# **** config pour apache : ****
#<VirtualHost xxx.xxx.xxx.xxx:80>
#	ServerName example.com
#	
#	DocumentRoot /path/to/bilbo/src/web-server/
#	
#	ErrorLog  /var/log/bilbo-web_error.log
#	CustomLog /var/log/bilbo-web_access.log combined
#	
#	<Directory /path/to/bilbo/src/web-server/>
#		Order deny,allow
#		Allow from all
#	</Directory>
#	
#	WSGIApplicationGroup %{GLOBAL}
#	WSGIScriptAlias / /path/to/bilbo/src/web-server/bilbo-web.py
#</VirtualHost>

# **** config pour nginx - uwsgi : ****
#server {
#	listen 80;
#	server_name example.com;
#	root /path/to/bilbo/src/web-server;
#	
#	location / {
#		include uwsgi_params;
#		uwsgi_read_timeout 3600;
#		uwsgi_cache off;
#		uwsgi_pass unix:/var/run/uwsgi/bilbo.sock;
#	}
#}

#[uwsgi]
#socket = /var/run/uwsgi/bilbo.sock
#master = true
#processes = 16
#plugins = http,python
#chdir = /path/to/src/web-server
#module = bilbo-web
#uid = www-data
#gid = www-data
#post-buffering = 1
