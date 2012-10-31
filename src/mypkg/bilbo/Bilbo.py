# -*- coding: utf-8 -*-
'''
-----------------------------------------------------------------------------------------------------------------------
BILBO : Automatic annotation of bibliographic reference

(C) Copyright 2012 by Young-Min Kim (youngminn.kim@gmail.com) and Jade Tavernier
(jade.tavernier@gmail.com). This is initially written by Young-Min Kim for the prototype 
and modified by Jade Tavernier for code reorganization in an object oriented design.
 
BILBO is an open source software for automatic annotation of bibliographic reference.
It provides the segmentation and tagging of input string. It is principally based on
Conditional Random Fields (CRFs), machine learning technique to segment and label
sequence data. As external softwares, Mallet is used for CRF learning and inference
and SVMlight is used for sequence classification. BILBO is licensed under a Creative
Commons Attribution-NonCommercial-ShareAlike 2.5 Generic License (CC BY-NC-SA 2.5).
---------------------------------------------------------------------------------------------------------------------------

Created on 18 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''

from mypkg.format.CRF import CRF
from mypkg.format.SVM import SVM
from mypkg.reference.Corpus import Corpus
import os
import time

class Bilbo(object):
	'''
	A machine Bilbo that trains a CRF (and a SVM) model and automatically annotates new references.
	'''

	def __init__(self, dirResult="Result/"): #Set the default result directory
		'''
		Attributes
		----------
		crf : CRF
		svm : SVM
		dirResult : string
			directory for output files
		'''
		self.crf = CRF(dirResult)
		self.svm = SVM(dirResult)
		self.dirResult = dirResult

		
	def train(self, dirCorpus, dirModel, type):
		'''
		CRF model learning (corpus 1 and 2), SVM model learning (corpus 2)
		Corpus object declaration
		
		Parameters
		----------
		dirCorpus : string
			directory where training references (notes) are
		dirModel : string
			directory where CRF and SVM models are saved
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		'''
		corpus = Corpus(dirCorpus)
		if type == 1:
			corpus.extract(1, "bibl")
			self.crf.prepareTrain(corpus, 1, "trainingdata_CRF_C1.txt", 1, 1)	#CRF training data extraction
			self.crf.runTrain(dirModel, "trainingdata_CRF_C1.txt")				#CRF model learning
		elif type == 2:
			corpus.extract(2, "note")
			self.crf.prepareTrain(corpus, 2, "data04SVM_ori.txt", 1) #Source data extraction for SVM note classification
			
			self.svm.prepareTrain(corpus)	#Training data extraction for SVM note classification
			self.svm.runTrain(dirModel)		#SVM model learning
			
			self.crf.prepareTrain(corpus, 2, "trainingdata_CRF_C2.txt", 1, 1)	#CRF training data extraction
			self.crf.runTrain(dirModel, "trainingdata_CRF_C2.txt") #CRF model learning
		
	
	
	def annotate(self, dirCorpus, dirModel, type, external=0):		
		'''
		Automatic annotation of references 
		
		Parameters
		----------
		dirCorpus : string
			directory where the references to be annotated are
		dirModel : string
			directory where the learned CRF model and SVM model have been saved
		typeCorpus : int, {1, 2, 3}
			1 : corpus 1, 2 : corpus 2...
		external : int, {1, 0}
			1 : if the references are external data except CLEO, 0 : if that of CLEO
			it is used to decide whether Bilbo learn call a SVM classification or not.
		'''
		nbRef = 0					#Number of references
		corpus = Corpus(dirCorpus)	#
		files = corpus.getFiles()
		filesTab = self._list_split(files, 50)
		for fname in filesTab:
			if type == 1:
				corpus = self.annotateCorpus1(dirModel, corpus, fname)
			elif type == 2:
				corpus = self.annotateCorpus2(dirModel, corpus, fname, external)
				
			corpus.deleteAllFiles()



	def annotateCorpus1(self, dirModel, corpus, fname):
		'''
		Automatic annotation of reference type 1 (reference)
		
		Parameters
		----------
		dirModel : string
			directory where the learned CRF model has been saved
		corpus : Corpus
			set of references that we want to annotate
		fname :	string
			name of file to be annotated
		'''
		corpus.extract(1, "bibl", fname)
		self.crf.prepareTest(corpus, 1)
		self.crf.runTest(dirModel, 'testdata_CRF.txt')

		corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "bibl", 1)
		return corpus
	


	def annotateCorpus2(self, dirModel, corpus, fname, external=0):
		'''
		Automatic annotation of reference type 2 (note)
		
		Parameters
		----------
		dirModel : string
			directory where learned CRF model and SVM model have been saved
		corpus : Corpus
			set of notes that we want to annotate
		fname :	string
			name of file to be annotated
		external : int, {1, 0}
			1 : if external data, 0 : if CLEO data

		See also
		--------
		Oct. 18, 2012 	SVM classification problem is fixed
						Check the classification result of reference (reference.train) in 'addTagReferences' method
						of 'Corpus' class that is called in 'annotateCorpus2' method of 'Bilbo' class.
		'''
		corpus.extract(2, "note", fname, external)
		
		if external == 0:
			self.crf.prepareTest(corpus, 2, -1) 	#last argument:int, -1:prepare source data for SVM learning, default:0
			
			self.svm.prepareTest(corpus)
			self.svm.runTest(dirModel)
		
			newlistReferences = self.crf.prepareTest(corpus, 2)
			self.crf.runTest(dirModel, 'testdata_CRF.txt')
			self.crf.postProcessTest("testEstCRF.txt", "testEstCLNblCRF.txt", newlistReferences.getReferences())
			corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "note", 2, newlistReferences.getReferences())
			
		else:										#if external data : external=1, we do not call a SVM model
			self.crf.prepareTest(corpus, 2, 2)		#indiceSvm=2 at prepareTest(self, corpus, typeCorpus, indiceSvm = 0, indices="")
			self.crf.runTest(dirModel, 'testdata_CRF.txt')
			corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "note", 2)

		return corpus
	

	def _list_split(self, flist, size):
		'''
		Split a filelist
		
		Parameters
		----------
		flist : list
			list to be split
		size : int
			new file list size
		result : list
			new file list
		'''	
		result = [[]]
		while len(flist) > 0:
			if len(result[-1]) >= size: result.append([])
			result[-1].append(flist.pop(0))
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