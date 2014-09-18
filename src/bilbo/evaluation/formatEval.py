# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from codecs import open
import glob
import os
import random
from bs4 import BeautifulSoup, NavigableString

class FormatEval():

	@staticmethod
	def getBiblFromDir(dirName, pattern = "*xml"):
		files = os.path.join(dirName,pattern)
		biblList = []
		for xmlFile in glob.glob(files):
			with open(xmlFile, 'r', encoding='utf-8') as content_file:
				content = content_file.read()
			bibls = FormatEval.getBiblList(content)
			biblList += bibls
		#print biblList, len(biblList)
		#print biblList[len(biblList)-1].encode('utf8')
		#print str(type(biblList[0]))
		return biblList

	@staticmethod
	# test : xml string
	def getBiblList(text):
		parsedText = BeautifulSoup(text)
		allBibl = []
		biblInside = 0
		allBiblTag = parsedText.findAll('bibl')
		for bibl in allBiblTag:
			if biblInside > 0: # do not duplicate line of <bibl> inside <bibl>
				biblInside -= 1
				continue
			line = unicode(bibl)
			allBibl.append(line)
			biblInside = len(bibl.findAll('bibl'))
			#print str(biblInside), unicode(bibl).encode('utf8')
		
		return allBibl

	@staticmethod
	# myList : list to shuffle
	# testPercentage : percentage of lenght of the first list
	def getShuffledCorpus(myList, testPercentage):
		shuffled = list(myList)
		random.shuffle(shuffled)
		cut = int(len(shuffled) / int(testPercentage))
		testCorpus = shuffled[:cut]
		trainCorpus = shuffled[cut:]
		#print cut, len(testCorpus), len(trainCorpus), testPercentage
		return testCorpus, trainCorpus

FormatEval.getBiblFromDir('evaluate')