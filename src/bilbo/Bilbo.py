# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
-----------------------------------------------------------------------------------------------------------------------
BILBO : Automatic labeling of bibliographic reference

(C) Copyright 2012 by Young-Min Kim (youngminn.kim@gmail.com) and Jade Tavernier
(jade.tavernier@gmail.com). This is initially written by Young-Min Kim for the prototype
and modified by Jade Tavernier for code reorganization in an object oriented design.

BILBO is an open source software for automatic annotation of bibliographic reference.
It provides the segmentation and tagging of input string. It is principally based on
Conditional Random Fields (CRFs), machine learning technique to segment and label
sequence data. As external softwares, Wapiti is used for CRF learning and inference
and SVMlight is used for sequence classification. BILBO is licensed under a Creative
Commons Attribution-NonCommercial-ShareAlike 2.5 Generic License (CC BY-NC-SA 2.5).
---------------------------------------------------------------------------------------------------------------------------

Created on April 08, 2012

@author: Young-Min Kim, Jade Tavernier, Ollagnier Anaïs
"""
from bilbo.format.MSVM import MSVM
from bilbo.format.CRF import CRF
from bilbo.format.SVM import SVM
from bilbo.reference.Corpus import Corpus
import os
import shutil
import glob
from tempfile import mkdtemp

class Bilbo(object):
	"""
	A machine Bilbo that trains a CRF (and a SVM) model and automatically labels new references.
	"""

	def __init__(self, dirResult='', options={}, crfmodelname="crf_model_simple"): #Set the default result directory
		"""
		Attributes
		----------
		crf : CRF
		svm : SVM
		dirResult : string
			directory for output files
		"""
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-3])
		
		if dirResult == '' : dirResult = os.path.join(self.rootDir, 'Result')
		if not os.path.exists(dirResult): os.makedirs(dirResult)
		self.dirResult = mkdtemp(dir = dirResult) + '/'
		self.crf = CRF(self.dirResult, options)
		self.svm = SVM(self.dirResult, options)
		self.msvm = MSVM(self.dirResult, options)
		self.options = options
		self.crfmodelname = crfmodelname


	def train(self, dirCorpus, dirModel, typeCorpus):
		"""
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
		"""
		corpus = Corpus(dirCorpus, self.options)
		self.crf.setDirModel(dirModel)
		if typeCorpus == 1:
			print "Extract references..."
			corpus.extract(1, "bibl")
			print "crf training data extraction..."
			self.crf.prepareTrain(corpus, 1, "trainingdata_CRF.txt", 1, 1) #CRF training data extraction
			self.crf.runTrain(dirModel, "trainingdata_CRF_Wapiti.txt", self.crfmodelname) #CRF model learning
				
		elif typeCorpus == 2:
			print "Extract notes..."
			corpus.extract(2, "note")
			optsvm = self.options.s
			if optsvm == True :
				print "svm source data extraction..."
				self.crf.prepareTrain(corpus, 2, "data04SVM_ori.txt", 1) #Source data extraction for SVM note classification
				print "svm training data extraction..."
				self.svm.prepareTrain(corpus) #Training data extraction for SVM note classification
				print "svm training..."
				self.svm.runTrain(dirModel) #SVM model learning
			
			print "crf training data extraction..."
			self.crf.prepareTrain(corpus, 2, "trainingdata_CRF.txt", 1, 1, optsvm) #CRF training data extraction
			self.crf.runTrain(dirModel, "trainingdata_CRF_Wapiti.txt", self.crfmodelname) #CRF model learning
			#self.crf.runTrain(dirModel, "trainingdata_CRF_nega_Wapiti.txt", "revueswapiti_nega", 0.0000001) #Do not work, too homogeneous
			print
                   
	        elif typeCorpus == 3:
			
			optsvm = self.options.s
			if optsvm == True :
                                print "msvm training data extraction..."
				fname = "model/corpus3/"+self.options.m+"/inputID.txt"
				list_files = glob.glob ('Data/*/')
				for f in list_files :
					folderName = os.path.relpath(f,"..")
					folderName = folderName.split('/')
					self.msvm.count(fname, f, str(folderName[2])+'.dat')
				i = 0
				for f in list_files :
					i = i + 1
					folderName = os.path.relpath(f,"..")
					folderName = folderName.split('/')
					self.msvm.transform(fname, f, str(folderName[2])+'.dat', str(i))
				self.msvm.concataneFiles(self.dirResult, "class.train")
				self.msvm.mixLines("class.train", "class_mix.train", self.dirResult)
				print "msvm training..."
				self.msvm.runTrain(dirModel)
                                #self.crf.prepareTrain(corpus, 3, "data04SVM_ori.txt", 1) #Source data extraction for SVM note classification
				#print "create corpus folder first class"
				#self.svm.createCorpusFolderFirstClass("model/corpus3/revues/ref_courtes_Bibl.xml")
    				#print "create corpus folder second class"
				#self.svm.createCorpusFolderSecondClass("model/corpus3/revues/ref_courtes_NoBibl.xml")
				#print "svm training data extraction..."
				#self.svm.prepareTrainC3("model/corpus3/revues/inputID.txt","model/corpus3/revues/impl/","model/corpus3/revues/Noimpl/","model/corpus3/revues/datFiles/") #Training data extraction for SVM note classification
				
				#self.svm.readFileC3("model/corpus3/revues/datFiles/")
				
				#print "svm training..."
				#self.svm.runTrainC3("model/corpus3/revues/datFiles/") #SVM model learn
				#print "crf training data extraction..."
                        	#self.crf.prepareTrain(corpus, 3, "trainingdata_CRF_Original.txt", 1, 1) #CRF training data extraction

                        	#self.crf.runTrain(dirModel, "trainingdata_CRF_Original_Original_OriginalWapiti.txt", self.crfmodelname) #CRF model learning
                        	#self.crf.runTrain(dirModel, "trainingdata_CRF_nega_Wapiti.txt", "revueswapiti_nega", 0.0000001) #Do not work, too homogeneous
                        	#print

			#else:
							
			#print "crf training data extraction..."
			#self.crf.prepareTrain(corpus, 3, "trainingdata_CRF_Original.txt", 1, 1) #CRF training data extraction
			
			#self.crf.runTrain(dirModel, "trainingdata_CRF_Original_Wapiti.txt", self.crfmodelname) #CRF model learning
			print
           	
		#self.deleteTmpFiles()


	def annotate(self, dirCorpus, dirModel, typeCorpus, external=0):
		"""
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
		"""
		corpus = Corpus(dirCorpus, self.options)
		self.crf.setDirModel(dirModel)	#
		files = corpus.getFiles()
		filesTab = self._list_split(files, 50)
		for fname in filesTab:
			if typeCorpus == 1:
				corpus = self.annotateCorpus1(dirModel, corpus, fname)
			if typeCorpus == 2:
				corpus = self.annotateCorpus2(dirModel, corpus, fname, external)
                        if typeCorpus == 3:
                                corpus = self.annotateCorpus3(dirModel, corpus, fname, external)
				print dirModel
			#corpus.deleteAllFiles()
			
		#self.deleteTmpFiles()


	def annotateCorpus1(self, dirModel, corpus, fname):
		"""
		Automatic annotation of reference type 1 (reference)
		
		Parameters
		----------
		dirModel : string
			directory where the learned CRF model has been saved
		corpus : Corpus
			set of references that we want to annotate
		fname :	string
			name of file to be annotated
		"""
		print "Extract references..."
		corpus.extract(1, "bibl", fname)
		print "crf data extraction for labeling..."
		self.crf.prepareTest(corpus, 1)
		print "crf run test for labeling..."
		self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
		print "corpus add tag for labeling..."
		corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "bibl", 1)
		
		return corpus


	def annotateCorpus2(self, dirModel, corpus, fname, external=0):
		"""
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
		"""
		print "Extract notes..."
		corpus.extract(2, "note", fname, external)
		if external == 0 and self.options.s : #if not external data and svm option is true
			print "svm source data extraction..."
			self.crf.prepareTest(corpus, 2, -1) 	#last argument:int, -1:prepare source data for SVM learning, default:0
			print "svm data extraction for labeling..."
			self.svm.prepareTest(corpus)
			self.svm.runTest(dirModel)
		
			print "crf data extraction for labeling..."
			newlistReferences = self.crf.prepareTest(corpus, 2)
			self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
			self.crf.postProcessTest("testEstCRF.txt", "testEstCLNblCRF.txt", newlistReferences.getReferences())
			corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "note", 2, newlistReferences.getReferences())
			
		else:										#if external data : external=1, we do not call a SVM model
			print "crf data extraction for labeling..."
			self.crf.prepareTest(corpus, 2, 2)		#indiceSvm=2 at prepareTest(self, corpus, typeCorpus, indiceSvm = 0)
			print "crf run test for labeling..."
			self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
			print "corpus add tag for labeling..."
			corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "note", 2)

		return corpus


        def annotateCorpus3(self, dirModel, corpus, fname, external=0):
                """
                Automatic annotation of reference type 2 (note)
                
                Parameters
                ----------
                dirModel : string
                        directory where learned CRF model and SVM model have been saved
                corpus : Corpus
                        set of notes that we want to annotate
                fname : string
                        name of file to be annotated
                external : int, {1, 0}
                        1 : if external data, 0 : if CLEO data

                See also
                --------
                Oct. 18, 2012   SVM classification problem is fixed
                                                Check the classification result of reference (reference.train) in 'addTagReferences' method
                                                of 'Corpus' class that is called in 'annotateCorpus2' method of 'Bilbo' class.
                """
                print "Extract implied reference..."
                corpus.extract(3, "impl", fname, external)
                #if external == 0 and self.options.s : #if not external data and svm option is true
                        #print "svm source data extraction..."
                        #self.crf.prepareTest(corpus, 3, -2)     #last argument:int, -1:prepare source data for SVM learning, default:0
			#self.svm.createCorpusFolderTest("DataTest/ref_courtes_p_Clean.xml")                        
			
			#print "svm data extraction for labeling..."
                        #self.svm.prepareTestC3("model/corpus3/revues/inputID.txt", "model/corpus3/new_model/", "model/corpus3/new_model/")
			#self.svm.runTestC3(dirModel)
			
                        #print "crf data extraction for labeling..."
                        #print self.crfmodelname
			#newlistReferences = self.crf.prepareTest(corpus, 3)
                        #self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
			
                        #self.crf.postProcessTest("testEstCRF.txt", "testEstCLNblCRF.txt", newlistReferences.getReferences())
                        #corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "impl", 3, newlistReferences.getReferences())
		
                #else:                                                                           #if external data : external=1, we do not call a SVM model
		print "crf data extraction for labeling..."
		self.crf.prepareTest(corpus, 3, -3)              #indiceSvm=2 at prepareTest(self, corpus, typeCorpus, indiceSvm = 0)
		print "crf run test for labeling..."
		self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
		print "corpus add tag for labeling..."
		corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "impl", 3)
			
                return corpus
		
	def deleteTmpFiles(self):
		dirResultRoot = os.path.abspath(os.path.join(self.dirResult, os.path.pardir))+'/'
		toKeep = []
		if self.options.k == 'primary' :
			toKeep = ['testEstCRF.xml', 'testEstCRF.txt', 'testdatawithlabel_CRF.txt']
		if self.options.k != 'all' :
			for dir_name, sub_dirs, files in os.walk(self.dirResult):
				for f in files :
					if f in toKeep :
						shutil.copyfile(dir_name+f, dirResultRoot+f)
					os.unlink(os.path.join(dir_name, f))
			os.rmdir(self.dirResult)
			

	def _list_split(self, flist, size):
		"""
		Split a filelist
		
		Parameters
		----------
		flist : list
			list to be split
		size : int
			new file list size
		result : list
			new file list
		"""
		result = [[]]
		while len(flist) > 0:
			if len(result[-1]) >= size: result.append([])
			result[-1].append(flist.pop(0))
		return result


	"""memory"""
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
