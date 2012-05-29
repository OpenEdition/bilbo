'''
Created on 18 avr. 2012

@author: jade
'''

from mypkg.format.CRF import CRF
from mypkg.reference.Corpus import Corpus
import os
import time

class Bilbo(object):
	'''
	classdocs
	'''


	def __init__(self, repResult="Result/"):
		'''
		Constructor
		'''
		self.crf = CRF(repResult)
	
	def apprentissage(self, repCorpus):
		corpus = Corpus(repCorpus)
		corpus.extractCorpus1()
		
		self.crf.preparerApprentissage1(corpus)
		self.crf.runTrain("model/corpus1/")
		
	def apprentissageCorpus2(self, repCorpus):
		print os.getcwd()
		corpus = Corpus(repCorpus)
		corpus.extractCorpus2()
		
		self.crf.preparerApprentissage2(corpus)
		self.crf.runTrain("model/corpus2/")
		
	def annoter(self, repCorpus):
		atime = time.time()
		corpus = Corpus(repCorpus)
		corpus.extractCorpus1()
		btime = time.time()
		difftime = btime - atime
		difftuple = time.gmtime(difftime)
		print( "temps ecoule pour l'extraction des references : %i heures %i minutes %i secondes" % ( difftuple.tm_hour, difftuple.tm_min, difftuple.tm_sec) )
		
		self.crf.preparerTest(corpus)
		self.crf.runTest("model/corpus1/")
		ctime = time.time()
		difftime = ctime - atime
		difftuple = time.gmtime(difftime)
		print( "temps ecoule  pour l'annotation via mallet : %i heures %i minutes %i secondes" % ( difftuple.tm_hour, difftuple.tm_min, difftuple.tm_sec) )
		
		corpus.addTagReferences("Result/testEstCRF.xml")
		corpus.buildAnnotateFiles()
		dtime = time.time()
		difftime = dtime - atime
		difftuple = time.gmtime(difftime)
		print( "temps ecoule  pour generation du fichier final : %i heures %i minutes %i secondes" % ( difftuple.tm_hour, difftuple.tm_min, difftuple.tm_sec) )
		#corpusAnnote = Corpus("Result/testEstCRF.xml")
		#corpusAnnote.buildAnnotateFiles()
		
	def annoterCorpus2(self, repCorpus):
		return