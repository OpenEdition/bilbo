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
 annotate with bilbo with 01/test/test.xml file
 save result in 01/result/
'''

class bilboAnnotate():
	def __init__(self, options, dirCorpus, testPercentage, numberOfPartition = 10):
		options.L = True
		options.t = 'bibl'
		options.k = 'all'
		options.o = 'simple'
		#print options
		
		dirPartitions = Partition.getDirPartitionNames(dirCorpus, testPercentage, numberOfPartition)
		for dirPartition in dirPartitions:
			(annotateDir, testDir, trainDir, modelDir, resultDir) = Partition.getDirTestNames(dirPartition)
			
			self._del_tmp_file(resultDir)
			bilbo = Bilbo(resultDir, options, "crf_model_simple")
			bilbo.annotate(annotateDir, modelDir, 1)

	def _del_tmp_file(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*')
		tmpDirs = glob.glob(pattern)
		for tmpDir in tmpDirs:
			shutil.rmtree(tmpDir)

if __name__ == '__main__':
	parser = defaultOptions()
	options, args = parser.parse_args(sys.argv[1:])
	
	# usage python src/bilbo/evalution/bilboAnnotate.py [bilbo option] dirCorpus 10
	numberOfPartition = int(sys.argv[3]) if len(sys.argv)==4 else 10
	p = bilboAnnotate(options, str(sys.argv[1]), str(sys.argv[2]), numberOfPartition)
	