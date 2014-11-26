# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
	Make an evaluation of the current model, using a tagged corpus
	Usage:
		python src/bilbo/evaluation/simpleEval.py dirCorpus/ dirResult/
	Results of the evaluation will be in dirResult/evaluation.txt
"""
import sys
if __name__ == '__main__':
	sys.path.append('src/')
import os
from codecs import open
from bilbo.Bilbo import Bilbo
from bilbo.utils import defaultOptions
from formatEval import FormatEval, prepareEval
from bilbo.reference.Corpus import Corpus
import shutil
import glob
from tokenAccuracyEval import TokenAccuracyEval

class simpleEval():
	def __init__(self, bilboOptions, dirCorpus, dirResult, typeCorpus=1):
		self.dirCorpus = dirCorpus
		self.dirResult = dirResult
		self.dirModel = os.path.join('model', 'corpus'+str(typeCorpus), bilboOptions.m, '')
		self.corpusTag = 'bibl'
		
		# define bilbo options
		self.bilboOptions = bilboOptions
		self.bilboOptions.T = True
		self.bilboOptions.L = False
		self.bilboOptions.t = self.corpusTag
		self.bilboOptions.k = 'all'
		self.bilboOptions.o = 'simple'

	def eval(self):
		# prepare result directories
		self._cleanDirResult()
		# extract bibl form corpus and striptag it
		self.extractAndCleanCorpus()
		# get tmp file from training
		self.formatTrain()
		# label the corpus
		self.annotate()
		# eval both results
		self.tokenEval()

	# copy files from corpus, stripTag them and save them
	def extractAndCleanCorpus(self):
		files = os.path.join(self.dirCorpus, "*xml")
		for xmlFile in glob.glob(files):
			with open(xmlFile, 'r', encoding='utf-8') as content_file:
				content = content_file.read()
			striped = FormatEval.strip_tags(content, self.corpusTag)
			self._saveFile(striped, self.dirLabel, os.path.basename(xmlFile))

	# train with test data to get tmp file for evaluation
	def formatTrain(self):
		self.bilboOptions.T = True
		self.bilboOptions.L = False
		bilbo = Bilbo(self.dirResult, self.bilboOptions, "crf_model_simple") # To save tmpFiles in testDir
		corpus = Corpus(self.dirCorpus, self.bilboOptions)
		corpus.extract(1, self.corpusTag)
		bilbo.crf.prepareTrain(corpus, 1, "evaldata_CRF.txt", 1, 1) #CRF training data extraction

	# annotation of test data striped tagged
	def annotate(self):
		self.bilboOptions.T = False
		self.bilboOptions.L = True
		bilbo = Bilbo(self.dirResult, self.bilboOptions, "crf_model_simple")
		bilbo.annotate(self.dirLabel, self.dirModel, 1)

	# get tmp files, format them, hamonize tokens, eval the results
	def tokenEval(self):
		desiredContent = self._getFile(self.dirResult, 'evaldata_CRF_Wapiti.txt')
		labeledContent= self._getFile(self.dirResult, 'testEstCRF_Wapiti.txt')
		
		desiredContentHarmonized, labeledContentHarmonized = prepareEval.prepareEval(desiredContent, labeledContent)
		
		evalText, labels, values = TokenAccuracyEval.evaluate(labeledContentHarmonized, desiredContentHarmonized)
		
		finalEval = "\t".join(labels) + "\n"
		finalEval += "\t".join(['{:f}'.format(v) for v in values]) + "\n"
		finalEval += evalText
		
		self._saveFile(finalEval, self.dirResult, 'evaluation.txt')

	# prepare directories
	def _cleanDirResult(self):
		# create Result directory
		if not os.path.isdir(self.dirResult):
			os.mkdir(self.dirResult)
		
		# unlink old files
		pattern = os.path.join(self.dirResult, '*')
		dirs = glob.glob(pattern)
		for d in dirs:
			if os.path.isdir(d):
				shutil.rmtree(d)
		
		# create label directory
		self.dirLabel = os.path.join(self.dirResult, 'Label')
		os.mkdir(self.dirLabel)

	# get a file in tmp* directory
	def _getFile(self, fileDir, pattern):
		pattern = os.path.join(fileDir,'tmp*', pattern)
		files = glob.glob(pattern)
		with open(files[0], 'r', encoding='utf-8') as content_file:
			content = content_file.read()
			return content

	def _saveFile(self, content, dirName, fileName):
		fileName = os.path.join(dirName, fileName)
		with open(fileName, 'w', encoding='utf-8') as content_file:
			content_file.write(content)

if __name__ == '__main__':
	parser = defaultOptions()
	options, args = parser.parse_args(sys.argv[1:])
	
	dirCorpus = args[0] if len(args)>=1 else sys.exit('You should give a corpus directory')
	dirResult = args[1] if len(args)>=2 else sys.exit('You should give a result directory')
	se = simpleEval(options, dirCorpus, dirResult)
	se.eval()
