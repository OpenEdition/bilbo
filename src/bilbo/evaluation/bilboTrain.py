# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
if __name__ == '__main__':
	sys.path.append('src/')
import os
from bilbo.Bilbo import Bilbo
from bilbo.utils import *
from partition import Partition
import glob
import shutil


'''
 foreach directory-evaluation/10%/ directory
 train bilbo with 01/train/train.xml file
 save model in 01/model/
'''

class bibloTrain():
	def __init__(self, bilboOptions, dirCorpus, testPercentage, corpusType, optsvm, numberOfPartition=10, prefix=''):
		self.bilboOptions = bilboOptions
		self.bilboOptions.T = True
		self.bilboOptions.L = False
		self.bilboOptions.t = corpusType
		if optsvm == 'True':
			self.bilboOptions.s = True
		else:
			pass
		#self.bilboOptions.k = 'all'
		#print('options: ',self.bilboOptions)
		self.partitions = Partition(dirCorpus, testPercentage, numberOfPartition, prefix)
		self.dirPartitions = self.partitions.getDirPartitionNames()
	
	def train(self):
		for dirPartition in self.dirPartitions:
			print "dirPartition", dirPartition
			(annotateDir, testDir, trainDir, modelDir, resultDir) = self.partitions.getDirTestNames(dirPartition)
			
			self._del_tmp_file(trainDir) # tmp file of test data are here
			bilbo = Bilbo(modelDir, self.bilboOptions, "crf_model_simple") # tmpFiles saved in modelDir if -k all
			if self.bilboOptions.t == 'bibl':
				print('Training Bilbo 1')
				bilbo.train(trainDir, modelDir, 1)
			elif self.bilboOptions.t == 'note':
				print('Training Bilbo 2')
				bilbo.train(trainDir, modelDir, 2)

	def _del_tmp_file(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*')
		tmpDirs = glob.glob(pattern)
		for tmpDir in tmpDirs:
			shutil.rmtree(tmpDir)


if __name__ == '__main__':
	parser = defaultOptions()
	options, args = parser.parse_args(sys.argv[1:])
	# usage python src/bilbo/evalution/bilboTrain.py [bilbo option] dirCorpus 10
	numberOfPartition = int(args[2]) if len(args)>=3 else 10
	prefix = args[3] if len(args)>=4 else ''
	bt = bibloTrain(options, str(args[0]), str(args[1]), str(sys.argv[5]), str(sys.argv[6]), numberOfPartition, prefix)
	bt.train()
