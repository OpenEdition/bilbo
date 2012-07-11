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
from mypkg.extra.Memory import Memory
import os
import time

class Bilbo(object):

	def __init__(self, repResult="Result/"):
		self.repResult = repResult
		self.crf = CRF(self.repResult)
		self.svm = SVM(self.repResult)
        
		
	'''
	apprentissage : apprentissage reference corpus 1
		repCorpus : repertoire ou se trouve le corpus d'apprentissage 
	'''
	def apprentissage(self, repCorpus):
		corpus = Corpus(repCorpus)
		corpus.extractCorpus1()
		
		self.crf.prepareTrain(corpus, 1, "trainingdata_CRF_C1.txt", 1, 1)
		self.crf.runTrain("model/corpus1/", "trainingdata_CRF_C1.txt")
	
	'''
	apprentissageCorpus2 : apprentissage reference corpus 2
		repCorpus : repertoire ou se trouve le corpus d'apprentissage 
	'''	
	def apprentissageCorpus2(self, repCorpus):
		print os.getcwd()
		corpus = Corpus(repCorpus)
		corpus.extractCorpus2()
		
		self.crf.prepareTrain(corpus, 2, "data04SVM_ori.txt", 1)
		#self.crf.runTrain("model/corpus2/", "data04SVM_ori.txt")
		
		self.svm.prepareTrain(corpus)
		self.svm.runTrain("model/corpus2/")
		
		self.crf.prepareTrain(corpus, 2, "trainingdata_CRF_C2.txt", 1, 1)
		self.crf.runTrain("model/corpus2/", "trainingdata_CRF_C2.txt")
		
	'''
	annoter : annote les references du type corpus 1
		repCorpus : repertoire ou se trouve les fichiers a annoter
	'''
	def annoter(self, repCorpus):
		btime = 0
		ctime = 0
		dtime = 0
		
		nbRef = 0
		corpus = Corpus(repCorpus)
		fichiers = corpus.getFiles()
		fichiersTab = self._list_split(fichiers, 50)
		for fichierTab in fichiersTab:
			atime = time.time()
			corpus.extractCorpus1(fichierTab)
			
			nbRef += corpus.nbReference(1)
			print nbRef
			
			btime = time.time()
			difftime = btime - atime
			difftuple = time.gmtime(difftime)
	
			print( "temps ecoule pour l'extraction des references : %i heures %i minutes %i secondes" % ( difftuple.tm_hour, difftuple.tm_min, difftuple.tm_sec) )
			print self.rss()
			print self.vsz()
			
			self.crf.preparerTest(corpus, 1)
			self.crf.runTest("model/corpus1/", 'testdata_CRF.txt')
			ctime = time.time()
			difftime = ctime - btime
			difftuple = time.gmtime(difftime)
	
			print( "temps ecoule  pour l'annotation via mallet : %i heures %i minutes %i secondes" % ( difftuple.tm_hour, difftuple.tm_min, difftuple.tm_sec) )
			print self.rss()
			print self.vsz()

			corpus.addTagReferences(self.repResult+"testEstCRF.xml")
			dtime = time.time()
			difftime = dtime - ctime
			difftupleA = time.gmtime(difftime)
			'''corpus.buildAnnotateFiles()
			etime = time.time()
			difftime = etime - dtime
			difftuple = time.gmtime(difftime)'''

			print( "temps ecoule  pour generation du fichier final A : %i heures %i minutes %i secondes" % ( difftupleA.tm_hour, difftupleA.tm_min, difftupleA.tm_sec) )
			#print( "temps ecoule  pour generation du fichier final B : %i heures %i minutes %i secondes" % ( difftuple.tm_hour, difftuple.tm_min, difftuple.tm_sec) )
			corpus.deleteAllFiles()
			print self.rss()
			print self.vsz()

		#corpusAnnote = Corpus("Result/testEstCRF.xml")
		#corpusAnnote.buildAnnotateFiles()
		
	'''
	annoterCorpus2 : annote les references du type corpus 2
		repCorpus : repertoire ou se trouve les fichiers a annoter
	'''
	def annoterCorpus2(self, repCorpus):
		corpus = Corpus(repCorpus)
		fichiers = corpus.getFiles()
		fichiersTab = self._list_split(fichiers, 50)
		
		for fichierTab in fichiersTab:
			corpus.extractCorpus2()
		
			self.crf.preparerTest(corpus, 2, -1)
			
			self.svm.prepareTest(corpus)
			self.svm.runTest("model/corpus2/")
			
			self.crf.preparerTest(corpus, 2)
			self.crf.runTest("model/corpus2/", 'testdata_CRF.txt')
		
		return
	
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