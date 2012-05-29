'''
Created on 18 avr. 2012

@author: jade
'''

import subprocess
from mypkg.format.note.featureSelection4SVM import *
from mypkg.format.Extract import Extract 
from mypkg.reference.ListReferences import ListReferences 
from mypkg.output.GenerateXml import GenerateXml

class CRF(object):
	'''
	classdocs
	'''


	def __init__(self, repResult):
		'''
		Constructor
		'''
		self.generateXml = GenerateXml()
		self.repResult = repResult
		
	'''
	preparerApprentissage
	corpus : objet Corpus
	indices : si l'on veut utiliser le meme fichier indice_trainning le passer en parametre
	'''
	def preparerApprentissage1(self, corpus, indices=""):
		listReferences = corpus.getListReferences(1)
		newListReferences = ListReferences(listReferences, 1)
		extractor = Extract()
		nbRef = corpus.nbReference(1)
		'fichier genere les indices'
		if indices == "":
			extractor.randomgen(nbRef, "../../KB/config/train_indices.txt", 1, newListReferences)
		else:
			extractor.randomgen(nbRef, indices, 0, newListReferences)
			
		'fichier pour le crf'
		extractor.extractor(1, nbRef, self.repResult+"trainingdata_CRF.txt", newListReferences, 1, 1)
		
		return newListReferences
	
	def preparerApprentissage2(self, corpus, indices=""):
		listReferences = corpus.getListReferences(2)
		newListReferences = ListReferences(listReferences, 2)
		extractor = Extract()
		nbRef = corpus.nbReference(2)
			
		'fichier pour le crf'
		#extractor.extractor(2, nbRef, self.repResult+"data04SVM_ori.txt", newListReferences)
		selector(self.repResult+"data04SVM_ori.txt", nbRef, 1, self.repResult+"data04SVM_ori.txt")

		return newListReferences
	
	'''
	preparerTest
	'''
	def preparerTest(self, corpus, indices=""):
		listReferences = corpus.getListReferences(1)
		listReferencesObj = ListReferences(listReferences, 1)
		
		extractor = Extract()
		nbRef = corpus.nbReference(1)
		'fichier genere les indices'
		if indices == "":
			extractor.randomgen(nbRef, "KB/config/train_indices.txt", 1, listReferencesObj)
		else:
			extractor.randomgen(nbRef, indices, 0, listReferencesObj)
			

		'fichier pour le crf'
		
		extractor.extractor(1, nbRef, self.repResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),1), -1, 1)
		extractor.extractor(1, nbRef, self.repResult+"testdataonlylabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),1), -2, 1)
		
		extractor.extractor(1, nbRef, self.repResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),1), 0, 1)


		
		return 
		
		
	'''
	runTrain : lance le crf mallet pour l'apprentissage
	'''
	def runTrain(self, repertoire) :
		#training
		command = 'java -cp  \"dependencies/mallet/class:dependencies/mallet/lib/mallet-deps.jar\" cc.mallet.fst.SimpleTagger  --train true --model-file '+repertoire+'revuescrf '+self.repResult+'trainingdata_CRF.txt >> '+repertoire+'log_mallet.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()	

		
		return
	
	'''
	runTest : lance le crf mallet pour annoter de nouvelles donnees
	'''
	def runTest(self, repertoire) :
		command = 'java -cp  \"dependencies/mallet/class:dependencies/mallet/lib/mallet-deps.jar\" cc.mallet.fst.SimpleTagger  --model-file '+repertoire+'revuescrf '+self.repResult+'testdata_CRF.txt > '+self.repResult+'testEstCRF.txt '
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
		self.generateXml.simpleComp(self.repResult+"testdata_CRF.txt", self.repResult+'testEstCRF.txt', 2, self.repResult+'testEstCRF.xml')	
		return
	
	'''
	def preparer(self, codedirname, indicator):	
		print 'Start extracting training or test data...'
		var = raw_input('If you want to generate a new list of training/test data indicator file, enter y. If not, just enter : ')
		
		command = ''
		if len(var) > 0 :
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 100 1 > train_indices.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			print 'training indices are regenerated.\n'
			
		if indicator == 10 or indicator == 20 :
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 1 1 > trainingdata_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 0 1 > testdata_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 1 > testdatawithlabel_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -2 1 > testdataonlylabel_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			if indicator == 20 :
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 1 4 > trainingdata_rich_CRF.txt' # 4:extract input and label 
				process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
				process.wait()
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 3 > testdata_rich_CRF.txt'	# 3: extract input
				process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
				process.wait()
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 4 > testdatawithlabel_rich_CRF.txt'
				process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
				process.wait()
		else :
			if indicator == 1 :
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 1 1 > trainingdata_CRF.txt'
			elif indicator == 0 :
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 0 1 > testdata_CRF.txt'
			elif indicator == -1 :
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 1 > testdatawithlabel_CRF.txt'
			elif indicator == -2 :
				command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -2 1 > testdataonlylabel_CRF.txt'
					
			print command
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()

		return
	'''
