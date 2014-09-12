# -*- coding: utf-8 -*-

import sys
import re
import xml.etree.ElementTree as ET

# usage : python formatEvalBilbo.py /home/ollagnier/Documents/tools/bilbo-3/KB/data/corpus1/XML_annotated2/test/test_corpus1_full/test_tag_light.xml > correct.txt
# usage : python formatEvalBilbo.py /home/ollagnier/Documents/tools/bilbo-3/KB/data/corpus1/XML_annotated2/test/test_corpus1_full/result_test_Corpus1_predit.xml > predit.txt

debug = True
#debug = False

args = sys.argv[1:]
fichier = str(args[0])

def hasChildNamed(elem, name):
	for child in elem.iter():
		if child.find(name) is not None:
			return True
	return False

if __name__ == '__main__':

	with open(fichier, 'r') as content_file:
		content = content_file.read()

	root = ET.fromstring("<listbibl>" + content + "</listbibl>")

	spaces = re.compile('^[\s ]+$', flags=re.UNICODE) # It is not a typo, ' ' is a nbsp !
	biblDone = False
	nextIter = []
	nextTail = []

	for elem in root.iter():
		if elem.tag == 'booktitle':
			elem.tag = 'title'
		if elem.tag == 'relatedItem':
			elem.tag = 'bookindicator'
		if elem.text:
			elem.text = re.sub(" ", 'BLABLA', elem.text)
			elem.text = re.sub("([(’«»._',’“”’/\"!?():-])", r' \1 ', elem.text)
			elem.text = re.sub('\s{2,}', ' ', elem.text)
			#print "\t" + elem.text
			#print elem.tag + ", " + elem.text
			for mot in elem.text.split(" "):
				if not spaces.match(mot) and not mot=='':
					tag = elem.tag
					if tag == 'bibl':
						tag = 'nolabel'
					if debug: print tag + "\t'" + mot.strip().encode("utf-8") + "'"
					else: print tag

		# Si un élément a du texte à la fin de lui, il faut le montrer comme nolabel
		tail = elem.tail
		if tail and not spaces.match(tail):
			tail = re.sub(" ", r' ', tail)
			tail = re.sub("([(’«».',“_”’’/\"!?():-])", r' \1 ', tail)
			tail = re.sub('\s{2,}', ' ', tail)
			numIter = sum(1 for _ in elem.iter())
			# Si l'élément contient d'autres éléments, le nolabel doit être écrit après ceux-ci
			if numIter > 1:
				#print "NOLABEL '"+tail.strip().encode("utf-8")+"' IN " + str(numIter)
				nextTail.append(tail)
				nextIter.append(numIter)
			else:
				for motintail in tail.split(" "):
					if not spaces.match(motintail) and not motintail=='':
						if debug: print "nolabel" + "\t'" + motintail.strip().encode("utf-8") + "'"
						else: print "nolabel"

			if len(nextIter):
				# Imprimer les nolabel qui manquent
				nextIter = map(lambda x: x-1, nextIter)
				thisIter = nextIter[len(nextIter)-1]
				if thisIter <= 0:
					nextIter.pop()
					thisTail = nextTail.pop()
					for motintail in thisTail.split(" "):
						if not spaces.match(motintail) and not motintail=='':
							if debug: print "nolabel" + "\t'" + motintail.strip().encode("utf-8") + "'"
							else: print "nolabel"

		# Faire un saut de ligne entre chaque 'bibl', sauf le premier et pas dans les bibl imbriquées
		if elem.tag == 'bibl':
			if biblDone:
				print
			else:
				biblDone = True
			hasBiblInside = hasChildNamed(elem, 'bibl')
			if hasBiblInside:
				biblDone = False
