# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
fichier XML annoté source
formatEvalBilbo.py -s => testEval-source.txt

fichier XML pas annoté => fichier XML annoté bilbo
-k all => testEstCRF.xml => formatEvalBilbo.py => testEval.txt

toKenAccuracy testEval.txt testEval-source.txt
"""

import sys
import regex as re
import xml.etree.ElementTree as ET
from codecs import open

# usage : python formatEvalBilbo.py testEstCRF.xml > correct.txt

args = sys.argv[1:]
fichier = str(args[0])

def addSpaces(text):
	text = re.sub(" ", ' ', text)
	text = re.sub("([^\p{L}\p{N}])", r' \1 ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

def printText(text, tag):
	if text and not spaces.match(text):
		text = addSpaces(text)
		for mot in text.split(" "):
			if not spaces.match(mot) and not mot=='':
				print (tag + "\t'" + mot.strip() + "'").encode('utf-8')
				#print (mot.strip() + "'").encode('utf-8')
				
def recursItem(bibl, parentName):
	elems = list(bibl)
	if elems:
		for elem in elems:
			tag = elem.tag
			if tag in tagSubstitute:
				tag = tagSubstitute[tag]
			
			# texte du début de balise
			text = elem.text
			printText(text, tag)
			
			# enfants
			children = list(elem)
			if children:
				recursItem(elem, elem.tag)
			
			# texte de fin de balise
			tail = elem.tail
			printText(tail, parentName)
	else: # cas d'un <bibl> avec uniquement du texte
		text = bibl.text
		printText(text, parentName)


if __name__ == '__main__':

	with open(fichier, 'r', encoding='utf-8') as content_file:
		content = content_file.read()

	content = "<listbibl>" + content + "</listbibl>"
	root = ET.fromstring(content.encode('utf-8'))

	spaces = re.compile('^[\s \t\n]+$') # It is not a typo, ' ' is a nbsp !
	tagSubstitute = {'booktitle':'title', 'relatedItem':'bookindicator', 'bibl':'nolabel'}
	biblDone = False
	nextIter = []
	nextTail = []

	for bibl in root.findall('.//bibl'):
		cpt = 0
		recursItem(bibl, 'nolabel')
		print
