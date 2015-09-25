# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on June 4, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from subprocess import PIPE
import glob
import subprocess, os
from codecs import open
from bilbo.format.Extract_svm import Extract_svm
from bilbo.format.Extract_svm_3 import Extract_svm_3

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

	def createCorpusFolderFirstClass (self,fileName):
		with open(fileName, encoding='utf8') as f:
        		i=0
        		for line in f:
            			if line.startswith('<impl>'):
                			output = open("./model/corpus3/revues/impl/"+str(i)+".txt",'w', encoding='utf8')
                			output.write(line)
                			output.close()
            			i=i+1
	
	def createCorpusFolderSecondClass (self,fileName):
		with open(fileName, encoding='utf8') as f:
        		i=0
        		for line in f:
            			if line.startswith('<impl>'):
                			output = open("./model/corpus3/revues/Noimpl/"+str(i)+".txt",'w', encoding='utf8')
                			output.write(line)
                			output.close()
            			i=i+1

	def createCorpusFolderTest(self,fileName):
		with open(fileName, encoding='utf8') as f:
                        i=0
                        for line in f:
                                if line.startswith('<impl>'):
                                        output = open("./model/corpus3/new_model/"+str(i)+".txt",'w', encoding='utf8')
                                        output.write(line)
                                        output.close()
                                i=i+1
        

        def readFile(self,folderPath):
		foldernames = glob.glob(folderPath)
		print foldernames
		filenames = glob.glob('*.dat')
    		print filenames
		for folder in foldernames:
        		output= open(self.dirResult+'trainingdata_SVM.txt','a')
        		for files in filenames:
            
            			with open(files,'r') as f:
                    			output.write(f.read())
        def readFileC3(self,folderPath):
                filenames = glob.glob(folderPath+'*.dat')
       		output= open(self.dirResult+'trainingdata_SVM.txt','a')
		for files in filenames:
			f = open(files,'r')
			output.write(f.read())
		 
	def prepareTrainC3(self, fname, dirFirstClass, dirSecondClass,dirResults): 
		'''
		Prepare SVM training data
		
		Parameters
		----------
		corpus : Corpus
		
		Attributes
		----------
		nbRef : String
			number of instances
		extractor : Extract_svm
		'''
		extractor = Extract_svm_3(self.options)
		extractor.transform(fname, dirFirstClass, dirResults+"/firstClass.dat", "+1")
           	extractor.transform(fname, dirSecondClass, dirResults+"/SecondClass.dat", "-1")
	
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
                extractor.transform(self.dirResult+"data04SVM_ori.txt", nbRef, 1, self.dirResult+"data04SVM_ori.txt", self.dirResult+"trainingdata_SVM.txt")


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

        def prepareTestC3(self, fname, dirTestCorpus, dirResults):
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

                extractor = Extract_svm_3(self.options)
		extractor.transform(fname, dirTestCorpus, dirResults+"/test.dat", "+1")

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

        def runTrainC3(self, directoryModel):
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

        def runTestC3(self, directoryModel):
                """
                Run SVM test module from SVM light software to classify new data
                
                Parameters
                ----------
                directoryModel : string
                        directory where we save the model
                """
                dependencyDir = os.path.join(self.rootDir, 'dependencies')
                command = dependencyDir+'/svm_light/svm_classify '+'./model/corpus3/new_model/test.dat '+directoryModel+'/datFiles/svm_model '+self.dirResult+'svm_predictions_new'
		#print self.dirResult
		#print 'command
                process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
                process.wait()

