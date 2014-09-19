# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
if __name__ == '__main__':
	sys.path.append('src/')
import os
from partition import Partition
import glob
import shutil
from formatEvalBilbo import FormatEvalBilbo
from tokenAccuracyEval import TokenAccuracyEval
from codecs import open

'''
 foreach directory-evaluation/10%/ directory
 do evaluation with 01/test.xml and 01/result/testEstCRF.xml
 save result in 01/evalution.txt
 append macro-precision result in 10%/evaluation.csv
'''

class bilboEval():
	def __init__(self, dirCorpus, testPercentage, numberOfPartition = 10):
		
		dirPartitions = Partition.getDirPartitionNames(dirCorpus, testPercentage, numberOfPartition)
		formatEval = FormatEvalBilbo()
		for dirPartition in dirPartitions:
			print "dirPartition", dirPartition
			(testDir, trainDir, modelDir, resultDir) = Partition.getDirTestNames(dirPartition)
			
			testEstCRF = self._getTestEstCRF(resultDir)
			testEstCRFFormated = formatEval.formatEval(testEstCRF)
			#print testEstCRFFormated
			self._saveFile(testEstCRFFormated, resultDir, 'annotatedEval.txt')
			
			desiredResult = self._getDesired(dirPartition)
			desiredResultFormated = formatEval.formatEval(desiredResult)
			#print desiredResultFormated
			self._saveFile(desiredResultFormated, resultDir, 'desiredEval.txt')
			
			#TODO: eval !
			evalText = TokenAccuracyEval.evaluate(testEstCRFFormated, desiredResultFormated)
			self._saveFile(evalText, dirPartition, 'evaluation.txt')

	def _getTestEstCRF(self, resultDir):
		pattern = os.path.join(resultDir,'tmp*','testEstCRF.xml')
		files = glob.glob(pattern)
		with open(files[0], 'r', encoding='utf-8') as content_file:
			testEstCRF = content_file.read()
		return testEstCRF

	def _getDesired(self, dirPartition):
		fileName = os.path.join(dirPartition, 'test.xml')
		with open(fileName, 'r', encoding='utf-8') as content_file:
			desiredResult = content_file.read()
		return desiredResult
	
	def _saveFile(self, content, dirName, fileName):
		fileName = os.path.join(dirName, fileName)
		with open(fileName, 'w', encoding='utf-8') as content_file:
			content_file.write(content)


if __name__ == '__main__':
	# usage python src/bilbo/evalution/bilboEval.py [bilbo option] dirCorpus 10
	numberOfPartition = int(sys.argv[3]) if len(sys.argv)==4 else 10
	p = bilboEval(str(sys.argv[1]), str(sys.argv[2]), numberOfPartition)
