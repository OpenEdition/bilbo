import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

from bilboweb import bilboWeb, annotate, urls
import web
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()


# **** config pour apache : ****
 
#<VirtualHost xxx.xxx.xxx.xxx:80>
	#ServerName example.com
	
	#DocumentRoot /path/to/bilbo/src/web-server/
	
	#ErrorLog  /var/log/bilbo-web_error.log
	#CustomLog /var/log/bilbo-web_access.log combined
	
	#<Directory /path/to/bilbo/src/web-server/>
		#Order deny,allow
		#Allow from all
	#</Directory>
	
	#WSGIApplicationGroup %{GLOBAL}
	#WSGIScriptAlias / /path/to/bilbo/src/web-server/bilbo-web.wsgi
#</VirtualHost>

# Rendre le dossier tmp/ accessible en écriture au serveur web
