# -*- coding: utf-8 -*-
'''
Created on 18 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''

import subprocess

from mypkg.format.Extract_crf import Extract_crf
from mypkg.reference.ListReferences import ListReferences 
from mypkg.output.GenerateXml import GenerateXml


class CRF(object):

	def __init__(self, dirResult):
		self.generateXml = GenerateXml()
		self.dirResult = dirResult
		
	'''
	prepareTrain
		corpus : Corpus object
		typeCorpus : int : corpus type 1, 2 or 3
		fileRes : output result file name
		tr : check if training or test data, : -2(test), -1(test), 0(test), 1(train), 
		extOption : check if the data is internal data then we'll use a modified index for corpus type 2
		indices : valid reference index file after SVM classification (corpus 2)
	'''
	def prepareTrain(self, corpus, typeCorpus, fileRes, tr=-1, extOption=-1, indices=""):
		listReferences = corpus.getListReferences(typeCorpus)
		newListReferences = ListReferences(listReferences, typeCorpus)
		extractor = Extract_crf()
		nbRef = corpus.nbReference(typeCorpus)

		'generation of training index for each reference'
		extractor.randomgen(newListReferences, 1)
				
		'if corpus type 2 and extOption=1, we use a modified index list'
		if typeCorpus == 2 and extOption == 1:
			'!!! modifie les indice pour indiquer les reference nonbibl <- This is not correct'
			'!!! modify the indices to eliminate the reference (or not print the reference) classified as non-bibl'
			
			extractor.extractorIndices("model/corpus2/svm_revues_predictions_training", newListReferences) 
			extractor.extractor(1, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
			
		else: # typeCorpus == 1 or (typeCorpus == 2 and isFrstExt == -1)
			########## SOURCE DATA EXTRACTION FOR SVM OR CORPUS 1 (BUT THESE ARE DIFFERENT !!!!!!!!!!!!!!!!!!!!!)
			extractor.extractor(typeCorpus, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
		
		return newListReferences
	
	'''
	prepareTest
		corpus : Corpus object
		typeCorpus : int : corpus type 1, 2 or 3
		indiceSvm : 0 normal(corpus 1), -1: data04SVM (corpus2), 2 : external data => svm isn't called
		indices : valid reference index file after SVM classification (corpus 2)
	'''
	def prepareTest(self, corpus, typeCorpus, indiceSvm = 0, indices=""):
		listReferences = corpus.getListReferences(typeCorpus)
		listReferencesObj = ListReferences(listReferences, typeCorpus)
		
		extractor = Extract_crf()
		nbRef = corpus.nbReference(typeCorpus)
		
		'generation of test index for each reference'
		extractor.randomgen(ListReferences(listReferencesObj.getReferences(),typeCorpus), 0)
		
		if indiceSvm == -1:
			extractor.extractor(typeCorpus, nbRef, self.dirResult+"data04SVM_ori.txt", ListReferences(listReferencesObj.getReferences(),typeCorpus))
		else: 
			'fichier pour le crf'
			if typeCorpus == 2 and indiceSvm != 2 :
				extractor.extractorIndices4new("model/corpus2/svm_revues_predictions_new", ListReferences(listReferencesObj.getReferences(),typeCorpus))
			
			'''
			Oct. 7, 2012 Currently we have a problem for processing corpus2. References should be eliminated when they
						are classified as non-bibliographic references but now label them as <nonbibl>. 
						Anyway no problem for the processing corpus 1...
			'''
			extractor.extractor(1, nbRef, self.dirResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -1, 1)
			extractor.extractor(1, nbRef, self.dirResult+"testdataonlylabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -2, 1)
			
			extractor.extractor(1, nbRef, self.dirResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), 0, 1)


		
		return 
		
		
	'''
	runTrain : lance le crf mallet pour l'apprentissage
		directory : directory u l'on veut sauvegarder le model 
		fichier : fichier genere par preparTrain en l'occurence trainingdata_CRF_C2.txt
	'''
	def runTrain(self, directory, fichier) :
		#training
		command = 'java -cp  \"dependencies/mallet/class:dependencies/mallet/lib/mallet-deps.jar\" cc.mallet.fst.SimpleTagger  --train true --model-file '+directory+'revuescrf '+self.dirResult+fichier+' >> '+directory+'log_mallet.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()	

		
		return
	
	'''
	runTest : lance le crf mallet pour annoter de nouvelles donnees
	'''
	def runTest(self, directory, fichier) :
		command = 'java -cp  \"dependencies/mallet/class:dependencies/mallet/lib/mallet-deps.jar\" cc.mallet.fst.SimpleTagger  --model-file '+directory+'revuescrf '+self.dirResult+fichier+' > '+self.dirResult+'testEstCRF.txt '
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
		self.generateXml.simpleComp(self.dirResult+"testdata_CRF.txt", self.dirResult+'testEstCRF.txt', 2, self.dirResult+'testEstCRF.xml')	
		return
	
