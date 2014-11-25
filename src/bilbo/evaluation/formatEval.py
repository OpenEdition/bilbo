# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from codecs import open
import glob
import os
import sys
import random
from bs4 import BeautifulSoup, NavigableString
import regex as re

class FormatEval():

	#@staticmethod
	## addWhiteSpace to change XML so <editor>Me</editor>and you<c>.</c> becomes <editor>Me</editor> and you<c>.</c>
	#def getBiblFromDir(dirName, addWhiteSpace=False, pattern="*xml"):
		#files = os.path.join(dirName,pattern)
		#biblList = []
		#for xmlFile in glob.glob(files):
			#with open(xmlFile, 'r', encoding='utf-8') as content_file:
				#content = content_file.read()
			#bibls = FormatEval.getBiblList(content)
			#biblList += bibls
		#if addWhiteSpace:
			#biblList = FormatEval.addWhiteSpace(biblList)
		##print biblList, len(biblList)
		##print biblList[len(biblList)-1].encode('utf8')
		##print str(type(biblList[0]))
		#return biblList

	@staticmethod
	# find all bibl in a directory
	# return a list of (filename, bibl_index)
	def get_bibl_fist_from_dir(dirName, file_pattern="*xml"):
		files = os.path.join(dirName, file_pattern)
		biblList = []
		for xmlFile in glob.glob(files):
			with open(xmlFile, 'r', encoding='utf-8') as content_file:
				content = content_file.read()
				#print xmlFile
				bibls = FormatEval.count_bibl_and_process(content)
				filename = os.path.basename(xmlFile)
				bibls = [(filename, index) for index in bibls]
				biblList += bibls

		return biblList

	@staticmethod
	# step one bibl at a time, not counting bibl inside bibl
	# if keep is a list of index, will keep only those bibl
	def count_bibl_and_process(text, keep=None):
		all_bibl = []
		bibl_counter = -1
		bibl_inside = 0

		parsedText = BeautifulSoup(text, 'xml')
		allBiblTag = parsedText.findAll('bibl')
		for bibl in allBiblTag:
			if bibl_inside > 0: # do not count <bibl> inside <bibl>
				bibl_inside -= 1
				#print bibl_counter
				continue
			bibl_inside = len(bibl.findAll('bibl'))
			bibl_counter +=1
			if keep and not (bibl_counter in keep):
				bibl.replace_with('')
			else:
				all_bibl.append(bibl_counter)

		if keep:
			return (all_bibl, unicode(parsedText))
		return all_bibl

	#@staticmethod
	## test : xml string
	#def getBiblList(text, duplicateBibl=False):
		#parsedText = BeautifulSoup(text)
		#allBibl = []
		#biblInside = 0
		#allBiblTag = parsedText.findAll('bibl')
		#for bibl in allBiblTag:
			#if not duplicateBibl:
				#if biblInside > 0: # do not duplicate line of <bibl> inside <bibl>
					#biblInside -= 1
					#continue
			#line = unicode(bibl)
			#allBibl.append(line)
			#biblInside = len(bibl.findAll('bibl'))
			##print str(biblInside), unicode(bibl).encode('utf8')
		
		#return allBibl

	@staticmethod
	# myList : list to shuffle
	# testPercentage : percentage of length of the first list
	def getShuffledCorpus(myList, testPercentage):
		shuffled = list(myList)
		random.shuffle(shuffled)
		cut = int(len(shuffled) * (int(testPercentage) / 100.0))

		testCorpus = {}
		for filename, index in shuffled[:cut]:
			if filename in testCorpus:
				testCorpus[filename].append(index)
			else:
				testCorpus[filename] = [index]

		trainCorpus = {}
		for filename, index in shuffled[cut:]:
			if filename in trainCorpus:
				trainCorpus[filename].append(index)
			else:
				trainCorpus[filename] = [index]

		#print cut, len(testCorpus), len(trainCorpus), testPercentage
		return testCorpus, trainCorpus

	@staticmethod
	# take a document (string) and strip all tags inside the given tag
	def strip_tags(text, tagCorpus='bibl'):
		parsedText = BeautifulSoup(text, 'xml')
		allBiblTag = parsedText.findAll(tagCorpus)
		for tag in allBiblTag:
			for children in tag.findAll():
				children.unwrap()
		return unicode(parsedText)

	#@staticmethod
	#def stripTags(xmlList, tagCorpus='bibl'):
		#striped = []
		#for line in xmlList:
			#soup = BeautifulSoup(line)
			#for tag in soup.findAll():
					#tag.unwrap()
					
			#txt = '<'+tagCorpus+'>' + unicode(soup) + '</' + tagCorpus + '>'
			##print str(type(txt)), ("———" + txt).encode('utf8')
			#striped.append(txt)
		#return striped

	@staticmethod
	# this is realy bad, but we use it to make FormatEvalBiblo work, and accept wrong XML
	# fortunatly it is not needed :D
	def addWhiteSpace(xmlList, tagCorpus='bibl'):
		spaced = []
		for line in xmlList:
			line = re.sub('<\/',' </', line, encoding='utf8')
			line = re.sub('>','> ', line, encoding='utf8')
			spaced.append(line.strip())

		return spaced

"""
 Using the content of tmp files from labeling and training
 Format them as ['label \t word'] lists
 Harmonise the length of each list, creating same token on each line
 Return each list as one big string
"""
class prepareEval():
	# TODO: use this class in bilboEval
	@staticmethod
	def prepareEval(desiredContent, labeledContent):
		pe = prepareEval()
		desiredContentFormated = pe.splitForEval(desiredContent)
		labeledContentFormated = pe.splitForEval(labeledContent)
		
		desiredContentHarmonized, labeledContentHarmonized = pe.harmonizeList(desiredContentFormated, labeledContentFormated)
		
		return "\n".join(desiredContentHarmonized), "\n".join(labeledContentHarmonized)

	def splitForEval(self, content):
		formated = []
		for line in content.split("\n"):
			words = line.split(" ")
			#print words
			if len(words)>1:
				formated.append(words[-1].strip() + "\t" + words[0].strip())
				#formated.append(words[0])
			else:
				formated.append('')
		return formated

	def _getFeatureAndName(self, token):
		words = token.split("\t")
		feature = words[0]
		name = words[1] if len(words) > 1 else ""
		if len(name.split()) > 1:
			name = "".join(name.split()) # kind of a bug: get rid of non printing (but spliters) utf-8 characters
		return feature, name

	# output is not the same length, before debug, dirty solution to harmonise output
	def harmonizeList(self, shortList, longList):
		indexLong = 0
		indexShort = 0
		lengthShort = len(shortList)
		lengthLong = len(longList)
		newShortList = []
		newLongList = []
		while True:
			featureShort, partShort = self._getFeatureAndName(shortList[indexShort])
			featureLong , partLong = self._getFeatureAndName(longList[indexLong])
			
			while True:
				if partShort == partLong:
					#print indexShort, partShort.encode('utf8'), indexLong, partLong.encode('utf8'), "RESOLVED"
					break
				#print indexShort, partShort.encode('utf8'), len(partShort), indexLong, partLong.encode('utf8'), len(partLong)
				if partShort < partLong:
					indexShort +=1
					_, partShortAppend = self._getFeatureAndName(shortList[indexShort])
					partShort += partShortAppend
				else:
					indexLong +=1
					_, partLongAppend  = self._getFeatureAndName(longList[indexLong])
					partLong += partLongAppend

			textShort = featureShort + "\t" + partShort if partShort else ''
			newShortList.append(textShort)
			textLong = featureLong + "\t" + partLong if partLong else ''
			newLongList.append(textLong)
			
			indexShort += 1
			indexLong += 1
			
			if indexShort == lengthShort or indexLong == lengthLong:
				break
		
		#print str(len(newShortList)), indexShort, lengthShort, str(len(newLongList)), indexLong, lengthLong
		return newShortList, newLongList

#if __name__ == '__main__':
	#myList = FormatEval.getBiblFromDir(sys.argv[1], addWhiteSpace=True)
	#myList = FormatEval.stripTags(myList)
	#for txt in myList:
		#print str(type(txt)), ("———" + txt).encode('utf8')
