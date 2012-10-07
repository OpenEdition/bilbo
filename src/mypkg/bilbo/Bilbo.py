# -*- coding: utf-8 -*-
'''
-----------------------------------------------------------------------------------------------------------------------
BILBO : Automatic annotation of bibliographic reference

(C) Copyright 2012 by Young-Min Kim (youngminn.kim@gmail.com) and Jade Tavernier
(ton mail). This is initially written by Young-Min Kim for the prototype and modified by
Jade Tavernier for code reorganization in an object oriented design.
 
BILBO is an open source software for automatic annotation of bibliographic reference.
It provides the segmentation and tagging of input string. It is principally based on
Conditional Random Fields (CRFs), machine learning technique to segment and label
sequence data. As external softwares, Mallet is used for CRF learning and inference
and SVMlight is used for sequence classification. BILBO is licensed under a Creative
Commons Attribution-NonCommercial-ShareAlike 2.5 Generic License (CC BY-NC-SA 2.5).
---------------------------------------------------------------------------------------------------------------------------

Created on 18 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''

from mypkg.format.CRF import CRF
from mypkg.format.SVM import SVM
from mypkg.reference.Corpus import Corpus
import os
import time

class Bilbo(object):

	def __init__(self, repResult="Result/"):
		self.crf = CRF(repResult)
		self.svm = SVM(repResult)
		self.repResult = repResult

		
	'''
	train : apprentissage reference corpus 1
		repCorpus : directory ou se trouve le corpus d'apprentissage 
		repModel : 		directory ou se trouve le model correspondant au corpus
		type : integer 1 : corpus 1, 2 : corpus 2...
	'''
	def train(self, repCorpus, repModel, type):
		corpus = Corpus(repCorpus)
		
		if type == 1:
			corpus.extract(1, "bibl")
			self.crf.prepareTrain(corpus, 1, "trainingdata_CRF_C1.txt", 1, 1)
			self.crf.runTrain(repModel, "trainingdata_CRF_C1.txt")
		elif type == 2:
			corpus.extract(2, "note")
			self.crf.prepareTrain(corpus, 2, "data04SVM_ori.txt", 1)
			
			self.svm.prepareTrain(corpus)
			self.svm.runTrain(repModel)
			
			self.crf.prepareTrain(corpus, 2, "trainingdata_CRF_C2.txt", 1, 1)
			self.crf.runTrain(repModel, "trainingdata_CRF_C2.txt")
		
	
	
	'''
	annotate : annote les references du type corpus 1
		repCorpus : 	directory ou se trouve les fichiers a annoter
		repModel : 		directory ou se trouve le model correspondant au corpus
		type :			integer :1 si coprus 1, 2 si corpus 2...
		externe : 		si ce sont des donnée externe = 1 (autre que le cleo), 0 sinon
		
	'''
	def annotate(self, repCorpus, repModel, type, externe=0):
		nbRef = 0
		corpus = Corpus(repCorpus)
		fichiers = corpus.getFiles()
		fichiersTab = self._list_split(fichiers, 50)
		for fichierTab in fichiersTab:
			if type == 1:
				corpus = self.annotateCorpus1(repModel, corpus, fichierTab)
			elif type == 2:
				corpus = self.annotateCorpus2(repModel, corpus, fichierTab, externe)
				
			corpus.deleteAllFiles()


	'''
	annotateCorpus1 : annote les references du type corpus 2
		repModel : 		directory ou se trouve le model correspondant au corpus
		corpus : 		objet Corpus correspondant au corpus que l'on souhaite annoter
		fichier :		fichier a annoter
		
	'''
	def annotateCorpus1(self, repModel, corpus, fichier):
		corpus.extract(1, "bibl", fichier)
		self.crf.preparerTest(corpus, 1)
		self.crf.runTest(repModel, 'testdata_CRF.txt')

		corpus.addTagReferences(self.repResult+"testEstCRF.xml", "bibl", 1)
		return corpus
	
	'''
	annotateCorpus2 : annote les references du type corpus 2
		repModel : 		directory ou se trouve le model correspondant au corpus
		corpus : 		objet Corpus correspondant au corpus que l'on souhaite annoter
		fichier :		fichier a annoter
		externe : 		si donnée externe = 1
	'''
	def annotateCorpus2(self, repModel, corpus, fichier, externe=0):

		corpus.extract(2, "note", fichier)
	
		if externe == 0:
			self.crf.preparerTest(corpus, 2, -1)
			
			self.svm.prepareTest(corpus)
			self.svm.runTest(repModel)
		
			self.crf.preparerTest(corpus, 2)
		else:
			self.crf.preparerTest(corpus, 2, 2)
			
		self.crf.runTest(repModel, 'testdata_CRF.txt')
		corpus.addTagReferences(self.repResult+"testEstCRF.xml", "note", 2)

		
		return corpus
	
	'''
	_list_split : decoupe une liste en plusieur liste
		list : liste a decouper
		size : taille des nouvelles listes
		return : liste des nouvelles listes
	'''
	def _list_split(self, list, size):
		result = [[]]
		while len(list) > 0:
			if len(result[-1]) >= size: result.append([])
			result[-1].append(list.pop(0))
		return result
	
	
	
	'''memoire'''
	def mem(self, size="rss"):
		"""Generalization; memory sizes: rss, rsz, vsz."""
		return os.popen('ps -p %d -o %s | tail -1' % (os.getpid(), size)).read()
	
	def rss(self):
		"""Return ps -o rss (resident) memory in kB."""
		return self.mem("rss")
	
	def rsz(self):
		"""Return ps -o rsz (resident + text) memory in kB."""
		return self.mem("rsz")
	
	def vsz(self):
		"""Return ps -o vsz (virtual) memory in kB."""
		return self.mem("vsz")