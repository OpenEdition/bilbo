# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from codecs import open
import glob
import os
import random
from bs4 import BeautifulSoup, NavigableString
import regex as re

class FormatEval():

	@staticmethod
	# addWhiteSpace to change XML so <editor>Me</editor>and you<c>.</c> becomes <editor>Me</editor> and you<c>.</c>
	def getBiblFromDir(dirName, addWhiteSpace=False, pattern="*xml"):
		files = os.path.join(dirName,pattern)
		biblList = []
		for xmlFile in glob.glob(files):
			with open(xmlFile, 'r', encoding='utf-8') as content_file:
				content = content_file.read()
			bibls = FormatEval.getBiblList(content)
			biblList += bibls
		if addWhiteSpace:
			biblList = FormatEval.addWhiteSpace(biblList)
		#print biblList, len(biblList)
		#print biblList[len(biblList)-1].encode('utf8')
		#print str(type(biblList[0]))
		return biblList

	@staticmethod
	# test : xml string
	def getBiblList(text, duplicateBibl=False):
		parsedText = BeautifulSoup(text)
		allBibl = []
		biblInside = 0
		allBiblTag = parsedText.findAll('bibl')
		for bibl in allBiblTag:
			if not duplicateBibl:
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
		cut = int(len(shuffled) * (int(testPercentage) / 100.0))
		testCorpus = shuffled[:cut]
		trainCorpus = shuffled[cut:]
		#print cut, len(testCorpus), len(trainCorpus), testPercentage
		return testCorpus, trainCorpus

	@staticmethod
	def stripTags(xmlList, tagCorpus='bibl'):
		striped = []
		for line in xmlList:
			soup = BeautifulSoup(line)
			for tag in soup.findAll():
				if tag.name != tagCorpus:
					tag.unwrap()
					
			txt = unicode(soup)
			#print str(type(txt)), ("———" + txt).encode('utf8')
			striped.append(txt)
		return striped

	@staticmethod
	# this is realy bad, but we use it to make FormatEvalBiblo work, and accept wrong XML
	# TODO: correct FormatEvalBiblo !!
	def addWhiteSpace(xmlList, tagCorpus='bibl'):
		spaced = []
		for line in xmlList:
			line = re.sub('<\/',' </', line, encoding='utf8')
			line = re.sub('>','> ', line, encoding='utf8')
			spaced.append(line.strip())
			
		return spaced

if __name__ == '__main__':
	myList = FormatEval.getBiblFromDir('evaluate', addWhiteSpace=True)
	for txt in myList:
		print str(type(txt)), ("———" + txt).encode('utf8')
