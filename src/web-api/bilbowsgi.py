# -*- coding: utf-8 -*-

import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

from bilboweb import bilboWeb, annotate, urls
import web
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
