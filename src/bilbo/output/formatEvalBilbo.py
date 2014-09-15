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

debug = True
#debug = False

args = sys.argv[1:]
fichier = str(args[0])

def addSpaces(text):
	text = re.sub(" ", ' ', text)
	text = re.sub("([^\p{L}\p{N}])", r' \1 ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

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
		for elem in bibl.iter():
			text = elem.text
			if text:
				text = addSpaces(text)
				for mot in text.split(" "):
					if not spaces.match(mot) and not mot=='':
						tag = elem.tag
						if tag in tagSubstitute:
							tag = tagSubstitute[tag]
						if debug:
							print (tag + "\t'" + mot.strip() + "'").encode('utf-8')
						else:
							print tag.encode('utf-8')

			# Si un élément a du texte à la fin de lui, il faut le montrer comme nolabel
			tail = elem.tail
			if tail and not spaces.match(tail):
				tail = addSpaces(tail)
				numIter = sum(1 for _ in elem.iter())
				# Si l'élément contient d'autres éléments, le nolabel doit être écrit après ceux-ci
				if numIter > 1:
					#print "NOLABEL '"+tail.strip().encode("utf-8")+"' IN " + str(numIter)
					nextTail.append(tail)
					nextIter.append(numIter)
				else:
					for motintail in tail.split(" "):
						if not spaces.match(motintail) and not motintail=='':
							if debug:
								print ("nolabel" + "\t'" + motintail.strip() + "'").encode("utf-8")
							else:
								print "nolabel"

				if len(nextIter):
					# Imprimer les nolabel qui manquent
					nextIter = map(lambda x: x-1, nextIter)
					thisIter = nextIter[len(nextIter)-1]
					if thisIter <= 0:
						nextIter.pop()
						thisTail = nextTail.pop()
						for motintail in thisTail.split(" "):
							if not spaces.match(motintail) and not motintail=='':
								if debug:
									print ("nolabel" + "\t'" + motintail.strip() + "'").encode("utf-8")
								else:
									print "nolabel"
		if nextIter or nextTail:
			print "This file has a biiiiiig bug and should be debuged"
			print "nextIter: " + nextIter
			print "nextTail: " + nextTail
		print
