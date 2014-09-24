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
	def __init__(self, dirCorpus, testPercentage, numberOfPartition=10, prefix=''):
		self.partitions = Partition(dirCorpus, testPercentage, numberOfPartition, prefix)
		self.dirPartitions = self.partitions.getDirPartitionNames()

	def eval(self):
		allValues = []
		for dirPartition in self.dirPartitions:
			#print "dirPartition", dirPartition
			(annotateDir, testDir, trainDir, modelDir, resultDir) = self.partitions.getDirTestNames(dirPartition)
			
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
		
		average = [float(sum(col))/len(col) for col in zip(*allValues)]
		allValues.append(average)
		
		finalEval = "\t".join(labels) + "\n"
		finalEval += "\n".join(["\t".join(['{:f}'.format(v) for v in values]) for values in allValues])
		self._saveFile(finalEval, self.partitions.getDirPercentName(), 'evaluation.tsv')

	def _getFeatureAndName(self, token):
		words = token.split("\t")
		feature = words[0]
		name = words[1] if len(words) > 1 else ""
		if len(name.split()) > 1:
			name = "".join(name.split()) # kind of a bug: get rid of non printing utf-8 characters
		return feature, name

	# output is not the same length, before debug, dirty solution to harmonise output
	def _harmonizeList(self, shortList, longList):
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
			words = line.split(" ")
			#print words
			if len(words)>1:
				formated.append(words[-1].strip() + "\t" + words[0].strip())
				#formated.append(words[0])
			else:
				formated.append('')
		return formated


if __name__ == '__main__':
	# usage python src/bilbo/evalution/bilboEval.py [bilbo option] dirCorpus 10
	numberOfPartition = int(sys.argv[3]) if len(sys.argv)>=4 else 10
	prefix = sys.argv[4] if len(sys.argv)>=5 else ''
	be = bilboEval(str(sys.argv[1]), str(sys.argv[2]), numberOfPartition, prefix)
	be.eval()
