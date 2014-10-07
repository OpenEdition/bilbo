# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on June 4, 2012

@author: Young-Min Kim, Jade Tavernier
"""
import subprocess, os
from bilbo.format.Extract_svm import Extract_svm

class SVM(object):
	"""
	SVM object is created in a Bilbo object
	SVM model learning and test
	"""

	def __init__(self, dirResult, options={}):
		"""
		Attributes
		----------
		dirResult : string
			directory for result files
		"""
		self.dirResult = dirResult
		self.options = options
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-4])


	def prepareTrain(self, corpus):
		"""
		Prepare SVM training data
		
		Parameters
		----------
		corpus : Corpus
		
		Attributes
		----------
		nbRef : String
			number of instances
		extractor : Extract_svm
		"""
		nbRef = corpus.nbReference(2) #corpus type = 2
		extractor = Extract_svm(self.options)
		extractor.extract(self.dirResult+"data04SVM_ori.txt", nbRef, 1, self.dirResult+"data04SVM_ori.txt", self.dirResult+"trainingdata_SVM.txt")


	def prepareTest(self, corpus):
		"""
		Prepare SVM test data
		
		Parameters
		----------
		corpus : Corpus
		
		Attributes
		----------
		nbRef : String
			number of instances
		extractor : Extract_svm
		"""
		nbRef = corpus.nbReference(2) #corpus type = 2
		extractor = Extract_svm(self.options)
		extractor.extract(self.dirResult+"data04SVM_ori.txt", nbRef, 0, self.dirResult+"data04SVM_ori.txt", self.dirResult+"newdata.txt")


	def runTrain(self, directoryModel):
		"""
		Run SVM training module from SVM light software
		Then call SVM test module to classify training data
		
		Parameters
		----------
		directoryModel : string
			directory where we save the model
		"""
		dependencyDir = os.path.join(self.rootDir, 'dependencies')
		command = dependencyDir+'/svm_light/svm_learn '+self.dirResult+'trainingdata_SVM.txt '+directoryModel+'svm_model'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()
		
		command = dependencyDir+'/svm_light/svm_classify '+self.dirResult+'trainingdata_SVM.txt '+directoryModel+'svm_model '+self.dirResult+'svm_predictions_training'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()


	def runTest(self, directoryModel):
		"""
		Run SVM test module from SVM light software to classify new data
		
		Parameters
		----------
		directoryModel : string
			directory where we save the model
		"""
		dependencyDir = os.path.join(self.rootDir, 'dependencies')
		command = dependencyDir+'/svm_light/svm_classify '+self.dirResult+'newdata.txt '+directoryModel+'svm_model '+self.dirResult+'svm_predictions_new'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()
