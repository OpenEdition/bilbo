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
from formatEval import prepareEval
from codecs import open

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
			
			print "label", resultDir, 'testEstCRF_Wapiti.txt'
			print "desire", trainDir, 'evaldata_CRF_Wapiti.txt'
			labeledContent = self._getFile(resultDir, 'testEstCRF_Wapiti.txt')
			desiredContent = self._getFile(trainDir, 'evaldata_CRF_Wapiti.txt') # tmpFiles from training of testDir are saved in trainDir !

			# harmonize the two lists, they are not tokenized the same way
			desiredContentHarmonized, labeledContentHarmonized = prepareEval.prepareEval(desiredContent, labeledContent)

			self._saveFile(labeledContentHarmonized, resultDir, 'annotatedEval.txt')
			self._saveFile(desiredContentHarmonized, resultDir, 'desiredEval.txt')
			
			evalText, labels, values = TokenAccuracyEval.evaluate(labeledContentHarmonized, desiredContentHarmonized)
			allValues.append(values)
			self._saveFile(evalText, dirPartition, 'evaluation.txt')
		
		# calculate average of results for all partitions
		average = [float(sum(col))/len(col) for col in zip(*allValues)]
		allValues.append(average)
		
		# print all results and average on the last line
		finalEval = "\t".join(labels) + "\n"
		finalEval += "\n".join(["\t".join(['{:f}'.format(v) for v in values]) for values in allValues])
		self._saveFile(finalEval, self.partitions.getDirPercentName(), 'evaluation.tsv')

	def _getFile(self, fileDir, pattern):
		pattern = os.path.join(fileDir,'tmp*', pattern)
		files = glob.glob(pattern)
		with open(files[0], 'r', encoding='utf-8') as content_file:
			print content_file
			content = content_file.read()
			return content

	def _saveFile(self, content, dirName, fileName):
		fileName = os.path.join(dirName, fileName)
		with open(fileName, 'w', encoding='utf-8') as content_file:
			content_file.write(content)


if __name__ == '__main__':
	# usage python src/bilbo/evalution/bilboEval.py [bilbo option] dirCorpus 10
	numberOfPartition = int(sys.argv[3]) if len(sys.argv)>=4 else 10
	prefix = sys.argv[4] if len(sys.argv)>=5 else ''
	be = bilboEval(str(sys.argv[1]), str(sys.argv[2]), numberOfPartition, prefix)
	be.eval()
