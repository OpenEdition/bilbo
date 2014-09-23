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
	def __init__(self, options, dirCorpus, testPercentage, numberOfPartition = 10):
		options.T = True
		options.t = 'bibl'
		#options.k = 'all'
		#print options
		
		dirPartitions = Partition.getDirPartitionNames(dirCorpus, testPercentage, numberOfPartition)
		for dirPartition in dirPartitions:
			print "dirPartition", dirPartition
			(annotateDir, testDir, trainDir, modelDir, resultDir) = Partition.getDirTestNames(dirPartition)
			
			#self._del_tmp_file(modelDir)
			bilbo = Bilbo(modelDir, options, "crf_model_simple") # To save tmpFiles in modelDir
			bilbo.train(trainDir, modelDir, 1)

	def _del_tmp_file(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*')
		tmpDirs = glob.glob(pattern)
		for tmpDir in tmpDirs:
			shutil.rmtree(tmpDir)


if __name__ == '__main__':
	parser = defaultOptions()
	options, args = parser.parse_args(sys.argv[1:])
	
	# usage python src/bilbo/evalution/bilboTrain.py [bilbo option] dirCorpus 10
	numberOfPartition = int(sys.argv[3]) if len(sys.argv)==4 else 10
	p = bibloTrain(options, str(sys.argv[1]), str(sys.argv[2]), numberOfPartition)
	