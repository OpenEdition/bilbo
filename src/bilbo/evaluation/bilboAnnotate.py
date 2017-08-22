# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
if __name__ == '__main__':
	sys.path.append('src/')
import os
from bilbo.Bilbo import Bilbo
from bilbo.utils import *
from bilbo.reference.Corpus import Corpus
from partition import Partition
import glob
import shutil

'''
 foreach directory-evaluation/10%/ directory
 annotate with bilbo with 01/test/test.xml file
 save result in 01/result/
'''

class bilboAnnotate():
	def __init__(self, bilboOptions, dirCorpus, testPercentage, corpusType, optsvm, numberOfPartition=10, prefix=''):
		self.bilboOptions = bilboOptions
		self.bilboOptions.L = True
		self.bilboOptions.T = False
		self.bilboOptions.t = corpusType
		self.bilboOptions.k = 'all'
		self.bilboOptions.o = 'simple'
		if optsvm == 'True':
			self.bilboOptions.s = True
		#print self.bilboOptions
		
		self.partitions = Partition(dirCorpus, testPercentage, numberOfPartition, prefix)
		self.dirPartitions = self.partitions.getDirPartitionNames()

	def annotate(self):
		for dirPartition in self.dirPartitions:
			print("dirPartition", dirPartition)
			(annotateDir, testDir, trainDir, modelDir, resultDir) = self.partitions.getDirTestNames(dirPartition)
			
			# annotation of test data striped tagged
			self._setBilboAnnotate()
			self._del_tmp_file(resultDir)
			bilbo = Bilbo(resultDir, self.bilboOptions, "crf_model_simple") # To save tmpFiles in resultDir
			if self.bilboOptions.t == 'bibl':
				print('Bilbo 1 add annotation')
				bilbo.annotate(annotateDir, modelDir, 1)
			if self.bilboOptions.t == 'note':
				print('Bilbo 2 add annotation')
				bilbo.annotate(annotateDir, modelDir, 2)
			
			# train with test data for evaluation
			self._setBilboTrain()
			self._del_tmp_file(trainDir)
			bilbo = Bilbo(trainDir, self.bilboOptions, "crf_model_simple") # To save tmpFiles in trainDir
			corpus = Corpus(testDir, self.bilboOptions)
			if self.bilboOptions.t == 'bibl':
				corpus.extract(1, "bibl")
				bilbo.crf.prepareTrain(corpus, 1, "evaldata_CRF.txt", 1, 1) #CRF training data extraction
			if self.bilboOptions.t == 'note':
				corpus.extract(2, "note")
				if self.bilboOptions.s == 'True':
					bilbo.crf.prepareTrain(corpus, 2, "data04SVM_ori.txt", 1) #Source data extraction for SVM note classification
					bilbo.svm.prepareTrain(corpus) #Training data extraction for SVM note classification
					bilbo.svm.runTrain(modelDir) #SVM model learning
					bilbo.crf.prepareTrain(corpus, 2, "evaldata_CRF.txt", 1, 1, "True")
				else:
					bilbo.crf.prepareTrain(corpus, 2, "evaldata_CRF.txt", 1, 1, "False")

	def _setBilboAnnotate(self):
		self.bilboOptions.L = True
		self.bilboOptions.T = False
	
	def _setBilboTrain(self):
		self.bilboOptions.L = False
		self.bilboOptions.T = True

	def _del_tmp_file(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*')
		tmpDirs = glob.glob(pattern)
		for tmpDir in tmpDirs:
			shutil.rmtree(tmpDir)


if __name__ == '__main__':
	parser = defaultOptions()
	options, args = parser.parse_args(sys.argv[1:])
	# usage python src/bilbo/evalution/bilboAnnotate.py [bilbo option] dirCorpus 10
	numberOfPartition = int(args[2]) if len(args)>=3 else 10
	prefix = args[3] if len(args)>=4 else ''
	ba = bilboAnnotate(options, str(args[0]), str(args[1]), str(sys.argv[5]), str(sys.argv[6]), numberOfPartition, prefix)
	ba.annotate()
