# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from codecs import open
import glob
import os
from lxml import html
import HTMLParser
import random

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
		#print biblList[len(biblList)-1]
		#print str(type(biblList[0]))
		return biblList

	@staticmethod
	# test : xml string
	def getBiblList(text):
		content = text
		tree = html.fromstring(content)
		allBiblPath = tree.xpath('//bibl[not(ancestor::bibl)]')
		allBibl = [html.tostring(bibl, encoding='utf8').decode('utf8') for bibl in allBiblPath]
		
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