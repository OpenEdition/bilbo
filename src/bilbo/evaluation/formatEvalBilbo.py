# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
fichier XML annoté source
formatEvalBilbo.py -s => testEval-source.txt

fichier XML pas annoté => fichier XML annoté bilbo
-k all => testEstCRF.xml => formatEvalBilbo.py => testEval.txt

toKenAccuracy testEval.txt testEval-source.txt

# TODO:
this version can separate word like : <editor>Me</editor>and you<c>.</c>, => Me and you.
but Bilbo do not => Meand you.
which is the right thing to do, although the xml is obviously not well formed !
"""

import sys
import regex as re
import xml.etree.ElementTree as ET
from codecs import open

# TODO: ne pas utiliser xml.etree testEstCRF.xml contient du xml non valide : <c> : < </c>
# TODO: corriger l'écriture de testEstCRF.xml !

# usage : python formatEvalBilbo.py testEstCRF.xml > correct.txt

class FormatEvalBilbo():
	def __init__(self):
		self.spaces = re.compile('^[\s \t\n]+$') # It is not a typo, ' ' is a nbsp !
		self.tagSubstitute = {'booktitle':'title', 'relatedItem':'bookindicator', 'bibl':'nolabel'}

	def formatEval(self, text):
		self.text = ''
		content = "<listbibl>" + text + "</listbibl>"
		root = ET.fromstring(content.encode('utf-8'))
		for bibl in root.findall('.//bibl'):
			cpt = 0
			self.recursItem(bibl, 'nolabel')
			self.text += "\n"
		return self.text

	def addSpaces(self, text):
		text = re.sub(" ", ' ', text)
		text = re.sub("([^\p{L}\p{N}])", r' \1 ', text)
		text = re.sub('\s{2,}', ' ', text)
		return text

	def printText(self, text, tag):
		if text and not self.spaces.match(text):
			text = self.addSpaces(text)
			for mot in text.split(" "):
				if not self.spaces.match(mot) and not mot=='':
					self.text += tag + "\t'" + mot.strip() + "'\n"
					#print (tag + "\t'" + mot.strip() + "'").encode('utf-8')
					#print (mot.strip() + "'").encode('utf-8')
					#self.text += mot.strip() + "'\n" # do not erase, very useful for debug
					
	def recursItem(self, bibl, parentName):
		elems = list(bibl)
		if elems:
			for elem in elems:
				tag = elem.tag
				if tag in self.tagSubstitute:
					tag = self.tagSubstitute[tag]
				
				# texte du début de balise
				text = elem.text
				self.printText(text, tag)
				
				# enfants
				children = list(elem)
				if children:
					self.recursItem(elem, elem.tag)
				
				# texte de fin de balise
				tail = elem.tail
				self.printText(tail, parentName)
		else: # cas d'un <bibl> avec uniquement du texte
			text = bibl.text
			self.printText(text, parentName)


if __name__ == '__main__':
	args = sys.argv[1:]
	fichier = str(args[0])
	
	with open(fichier, 'r', encoding='utf-8') as content_file:
		content = content_file.read()
	
	fe = FormatEvalBilbo()
	formated =  fe.formatEval(content)
	print formated.encode('utf-8')

