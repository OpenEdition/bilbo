# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
if __name__ == '__main__':
	sys.path.append('src/')
import os
from partition import Partition
import glob
import shutil
from tokenAccuracyEval import TokenAccuracyEval
from codecs import open
from bilbo.Bilbo import Bilbo
from bilbo.format.CRF import CRF
from bilbo.reference.Corpus import Corpus
from bilbo.utils import *


'''
 foreach directory-evaluation/10%/ directory
 do evaluation with 01/test.xml and 01/result/testEstCRF.xml
 save result in 01/evalution.txt
 append macro-precision result in 10%/evaluation.csv
'''

class bilboEval():
	def __init__(self, dirCorpus, testPercentage, numberOfPartition = 10):
		
		dirPartitions = Partition.getDirPartitionNames(dirCorpus, testPercentage, numberOfPartition)
		allValues = []
		for dirPartition in dirPartitions:
			#print "dirPartition", dirPartition
			(annotateDir, testDir, trainDir, modelDir, resultDir) = Partition.getDirTestNames(dirPartition)
			
			testEstCRF = self._getTestEstCRF(resultDir)
			testEstCRFFormated = self._formatEval(testEstCRF)
			##print testEstCRFFormated
			
			desiredResult = self._getDesired(testDir, trainDir)
			desiredResultFormated = self._formatEval(desiredResult)
			#print desiredResultFormated

			desiredResultFormated, testEstCRFFormated = self._harmonizeList(desiredResultFormated, testEstCRFFormated)

			testEstCRFFormated = "\n".join(testEstCRFFormated)
			desiredResultFormated = "\n".join(desiredResultFormated)
			self._saveFile(testEstCRFFormated, resultDir, 'annotatedEval.txt')
			self._saveFile(desiredResultFormated, resultDir, 'desiredEval.txt')
			
			evalText, labels, values = TokenAccuracyEval.evaluate(testEstCRFFormated, desiredResultFormated)
			allValues.append(values)
			self._saveFile(evalText, dirPartition, 'evaluation.txt')
		finalEval = ",".join(labels) + "\n"
		finalEval += "\n".join([",".join(v) for v in allValues])
		self._saveFile(finalEval, Partition.getDirPercentName(dirCorpus, testPercentage), 'evaluation.csv')

	# output is not the same length, before debug, dirty solution to harmonise output
	def _harmonizeList(self, shortList, longList):
		indexLong = 0
		indexShort = 0
		lengthShort = len(shortList)
		lengthLong = len(longList)
		newShortList = []
		newLongList = []
		while True:
			while True:
				#print "short", indexShort, lengthShort
				wordShort = shortList[indexShort].split("\t")
				if len(wordShort) > 1 or indexShort == lengthShort-1:
					break
				indexShort += 1
			while True:
				#print "long", indexLong, lengthLong
				wordLong = longList[indexLong].split("\t")
				if len(wordLong) > 1 or indexLong == lengthLong-1:
					break
				indexLong += 1
			
			if indexShort == lengthShort-1 or indexLong == lengthLong-1:
				break
			
			if wordShort[1] == wordLong[1]:
				newShortList.append(shortList[indexShort])
				newLongList.append(longList[indexLong])
			else:
				if (len(wordLong[1]) < len(wordShort[1])):
					feature = wordLong[0]
					nom = wordLong[1]
					while (nom != wordShort[1]):
						#print nom, "différent", wordShort[1], "first", indexLong, lengthLong
						indexLong +=1
						wordLong = longList[indexLong].split("\t")
						nom += wordLong[1]
					newLongList.append(feature + "\t" + nom)
					newShortList.append(shortList[indexShort])
					#print wordShort, nom, indexLong, shortList[indexShort], longList[indexLong], indexShort
				else:
					feature = wordShort[0]
					nom = wordShort[1]
					while (nom != wordLong[1]):
						#print nom, "différent", wordLong[1], "second", indexShort, lengthShort
						indexShort +=1
						wordShort = shortList[indexShort].split("\t")
						nom += wordShort[1]
						newShortList.append(feature + "\t" + nom)
						newLongList.append(longList[indexLong])
						#print wordShort, nom, indexLong, shortList[indexShort], longList[indexLong], indexShort
			indexShort += 1
			indexLong += 1
		#print str(len(newShortList)), str(len(newLongList))
		return newShortList, newLongList

	def _getTestEstCRF(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*','testEstCRF_Wapiti.txt')
		files = glob.glob(pattern)
		with open(files[0], 'r', encoding='utf-8') as content_file:
			testEstCRF = content_file.read()
		return testEstCRF

	def _getDesired(self, testDir, trainDir):
		self._del_tmp_file(trainDir)
		parser = defaultOptions()
		options, args = parser.parse_args([])
		options.T = True
		options.t = 'bibl'
		options.k = 'all'
		bilbo = Bilbo(trainDir, options, "crf_model_simple") # To save tmpFiles in testDir
		corpus = Corpus(testDir, options)
		bilbo.crf.setDirModel(testDir)
		corpus.extract(1, "bibl")
		bilbo.crf.prepareTrain(corpus, 1, "evaldata_CRF.txt", 1, 1) #CRF training data extraction
		
		pattern = os.path.join(trainDir,'tmp*','evaldata_CRF_Wapiti.txt')
		files = glob.glob(pattern)
		with open(files[0], 'r', encoding='utf-8') as content_file:
			desiredResult = content_file.read()
		return desiredResult

	def _del_tmp_file(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*')
		tmpDirs = glob.glob(pattern)
		for tmpDir in tmpDirs:
			shutil.rmtree(tmpDir)

	def _saveFile(self, content, dirName, fileName):
		fileName = os.path.join(dirName, fileName)
		with open(fileName, 'w', encoding='utf-8') as content_file:
			content_file.write(content)

	def _formatEval(self, content):
		formated = []
		for line in content.split("\n"):
			words = line.split()
			#print words
			if words:
				formated.append(words[-1] + "\t" + words[0])
				#formated.append(words[0])
			else:
				formated.append('')
		return formated

if __name__ == '__main__':
	# usage python src/bilbo/evalution/bilboEval.py [bilbo option] dirCorpus 10
	numberOfPartition = int(sys.argv[3]) if len(sys.argv)==4 else 10
	p = bilboEval(str(sys.argv[1]), str(sys.argv[2]), numberOfPartition)
