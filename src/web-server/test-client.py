# -*- coding: utf-8 -*-
import urllib
import json

url = 'http://localhost:8079'

texts = []
fich = open("../../test/entite-tei-2236.xml", "r")
resultat = fich.readlines()
fich.close()

texts.append(''.join(resultat))
texts.append(''.join(resultat))

query = {'corpus':1, 'texts':texts}
data = urllib.urlencode(query, True)

res = urllib.urlopen(url, data).read()

results = json.loads(res)

for result in results:
	print result
