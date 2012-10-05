# -*- coding: utf-8 -*-
'''
Created on 18 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''

import subprocess

from mypkg.format.Extract_crf import Extract_crf
from mypkg.reference.ListReferences import ListReferences 
from mypkg.output.GenerateXml import GenerateXml


class CRF(object):

	def __init__(self, repResult):
		self.generateXml = GenerateXml()
		self.repResult = repResult
		
	'''
	prepareTrain
		corpus : objet Corpus
		numCorpus : int :type de corpus 1, 2 ou 3
		fichierRes : nom du fichier de sortie
		tr : indicator check, it gives the valid instance indices 
		extr :  
		indices : si l'on veut utiliser le meme fichier indice_trainning le passer en parametre
		
	'''
	def prepareTrain(self, corpus, numCorpus, fichierRes, tr=-1, extr=-1, indices=""):
		listReferences = corpus.getListReferences(numCorpus)
		newListReferences = ListReferences(listReferences, numCorpus)
		extractor = Extract_crf()
		nbRef = corpus.nbReference(numCorpus)

		'generation des indices'
		extractor.randomgen(newListReferences, 1)
				
		'fichier pour le crf'
		if numCorpus == 2 and extr == 1:
			'modifie les indice pour indiquer les reference nonbibl'
			
			extractor.extractorIndices("model/corpus2/svm_revues_predictions_training", newListReferences) 
			extractor.extractor(1, nbRef, self.repResult+fichierRes, newListReferences, tr, extr)
			
		else:
			extractor.extractor(numCorpus, nbRef, self.repResult+fichierRes, newListReferences, tr, extr)
		
		return newListReferences
	
	'''
	preparerTest
		corpus : objet Corpus
		numCorpus : int :type de corpus 1, 2 ou 3
		indiceSvm : 0 normale, -1: data04SVM, 2 : external data => svm isn't call
		indices : fichier save indice
	'''
	def preparerTest(self, corpus, numCorpus, indiceSvm = 0, indices=""):
		listReferences = corpus.getListReferences(numCorpus)
		listReferencesObj = ListReferences(listReferences, numCorpus)
		
		extractor = Extract_crf()
		nbRef = corpus.nbReference(numCorpus)
		
		'fichier genere les indices'
		extractor.randomgen(ListReferences(listReferencesObj.getReferences(),numCorpus), 0)
		
		if indiceSvm == -1:
			extractor.extractor(numCorpus, nbRef, self.repResult+"data04SVM_ori.txt", ListReferences(listReferencesObj.getReferences(),numCorpus))
		else:
			'fichier pour le crf'
			if numCorpus == 2 and indiceSvm != 2 :
				extractor.extractorIndices4new("model/corpus2/svm_revues_predictions_new", ListReferences(listReferencesObj.getReferences(),numCorpus))
			
			'''
			*BUG REPORT*
			Oct. 5, 2012 Currently we have a problem. Label extracting is not working well for several notes. 
						 No problem when we just annotate them with Bilbo but if we want to evaluate the result
						 using already annotated test data, it's problematic. I didn't find the reason yet 
						 but by extracting test data just as training data with (1,1) for the last arguments,
						 instead of (-1,1), I temporarily fixed the problem. Need to check 'extractor' in 
						 Extract_crf.py. TO BE FIXED............................................................
			'''
			extractor.extractor(1, nbRef, self.repResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),numCorpus), 1, 1)
			#extractor.extractor(1, nbRef, self.repResult+"testdataonlylabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),numCorpus), -2, 1)

			extractor.extractor(1, nbRef, self.repResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),numCorpus), 0, 1)


		
		return 
		
		
	'''
	runTrain : lance le crf mallet pour l'apprentissage
		repertoire : repertoire u l'on veut sauvegarder le model 
		fichier : fichier genere par preparTrain en l'occurence trainingdata_CRF_C2.txt
	'''
	def runTrain(self, repertoire, fichier) :
		#training
		command = 'java -cp  \"dependencies/mallet/class:dependencies/mallet/lib/mallet-deps.jar\" cc.mallet.fst.SimpleTagger  --train true --model-file '+repertoire+'revuescrf '+self.repResult+fichier+' >> '+repertoire+'log_mallet.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()	

		
		return
	
	'''
	runTest : lance le crf mallet pour annoter de nouvelles donnees
	'''
	def runTest(self, repertoire, fichier) :
		command = 'java -cp  \"dependencies/mallet/class:dependencies/mallet/lib/mallet-deps.jar\" cc.mallet.fst.SimpleTagger  --model-file '+repertoire+'revuescrf '+self.repResult+fichier+' > '+self.repResult+'testEstCRF.txt '
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
		self.generateXml.simpleComp(self.repResult+"testdata_CRF.txt", self.repResult+'testEstCRF.txt', 2, self.repResult+'testEstCRF.xml')	
		return
	
