# -*- coding: utf-8 -*-
"""
Usage: python bilboweb.py 8079 (or another port)

Makes use of the simple web framework "web.py" http://webpy.org/ ~ https://github.com/webpy/webpy
"""
import web
import sys
import os
import shutil
import codecs
import json
from pprint import pprint

#Import bilbo
sys.path.append('..')
from bilbo.Bilbo import Bilbo
from bilbo.utils import *
from bilbo.reference.File import File

urls = (
	'/', 'bilboWeb',
	'/bilbo', 'bilboWeb',
	'/annotate', 'annotate',
)

class annotate:
	def POST(self):
		request = web.input(('corpus'), texts=[])
		corpus = int(request.corpus)

		if (corpus < 1 or corpus > 2):
			return web.webapi.BadRequest()

		cpt = len(request.texts)
		if (cpt>0):
			files = annoterCorpus(corpus, request)
		else:
			return web.webapi.BadRequest()

		#recupere le resultat de BILBO
		resultat = []
		while cpt > 0:
			cpt -= 1
			resultat.append(files[cpt].result)

		retour = json.dumps(resultat)
		if ('callback' in request): # support jsonp
			retour = request.callback + '(' + retour + ')'
		
		web.header('Content-Type','application/json;')
		return retour

	def GET(self):
		return self.POST()

class bilboWeb:
	def GET(self):
		render = web.template.render('templates/')
		return render.bilbo()
	
def annoterCorpus(corpus, request):
	dirModel = os.path.abspath('../../model/corpus' + str(corpus) + "/revues/") + "/"

	if corpus == 2: optStr = '-T -t note'
	else: optStr = '-T -t bibl'
	
	if hasattr(request, 'doi'):
		optStr += ' -d'
	
	parser = defaultOptions()
	options, args = parser.parse_args(optStr.split())

	cpt = 0
	files = []
	for text in request.texts:
		cpt += 1
		files.append(File('file' + str(cpt), options, text.encode('utf8')))

	bilbo = Bilbo('', options, "crf_model_simple")
	bilbo.annotate(files, dirModel, corpus)
	return files

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
