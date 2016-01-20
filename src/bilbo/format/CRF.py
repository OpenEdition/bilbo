# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.format.Extract_crf import Extract_crf
from bilbo.reference.ListReferences import ListReferences 
from bilbo.output.GenerateXml import GenerateXml
import subprocess, os
import glob
import shutil
from codecs import open

class CRF(object):
	"""
	CRF object is created in a Bilbo object
	CRF model learning and test
	"""

	def __init__(self, dirResult, options={}):
		"""
		Attributes
		----------
		generateXml : GenerateXml
		dirResult : string
			directory for result files
		"""
		self.generateXml = GenerateXml()
		self.dirResult = dirResult
		self.options = options
		self.dirModel = ""
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-4])


	def setDirModel(self, dirModel):
		self.dirModel = dirModel

	def createFolder(self, folderInit, folderResult):
		list_files = glob.glob (folderInit+'*')
		newpath = folderResult 
		if os.path.exists(newpath):
			shutil.rmtree(newpath)	
		os.makedirs(newpath)
		j = 0
		for file in list_files :
			j = j + 1
			with open(file, 'r', encoding='utf8') as f:
				folderPath = 'class_'+str(j)
				classPath = newpath+folderPath
				if not os.path.exists(classPath):
                			os.makedirs(classPath)
				i=0
				for line in f:
					if line.startswith('<impl>'):
						output = open(classPath+'/'+str(i)+".xml",'w', encoding = 'utf8')
						output.write(line)
						output.close()
					i=i+1

	def prepareTrain(self, corpus, typeCorpus, fileRes, tr=-1, extOption=-1, optsvm=True):
		"""
		Prepare CRF training data
		
		Parameters
		----------
		corpus : Corpus
		typeCorpus : int, {1, 2, 3}
			1 : corpus 1, 2 : corpus 2...
		fileRes : string
			output file name
		tr : int, {1, 0, -1, -2} (default -1)
			check if training or test data
			1 : train, 0 : test without label, -1 : test with label, -2 : test only label
		extOption : int, {-1, 1, ...} (default -1)
			extra option for crf training/test data format
			check if data is internal data, if yes we'll use a modified index for corpus type 2
			-1 : data format for SVM
			1 : data format for normal CRF training/test data
			2-5 : (not yet provided)
		"""
		listReferences = corpus.getListReferences(typeCorpus)
		newListReferences = ListReferences(listReferences, typeCorpus)
		extractor = Extract_crf(self.options)
		nbRef = corpus.nbReference(typeCorpus)

		'generation of training index for each reference'
		extractor.randomgen(newListReferences, 1)
				
		'if corpus type 2 and extOption=1, we use a modified index list' #!!!!!!!!!!
		if typeCorpus == 2 and extOption == 1:
			'modify the indices to eliminate the reference (or not print the reference) classified as non-bibl BY SVM'
			if optsvm == True : #if not, do not modify
				extractor.extractIndices(self.dirResult+"svm_predictions_training", newListReferences)
			extractor.extract(typeCorpus, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
   		if typeCorpus == 3 :
                        extractor.extract(typeCorpus, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
			
		else: # typeCorpus == 1 or (typeCorpus == 2 and isFrstExt == -1)
			########## SOURCE DATA EXTRACTION FOR SVM OR CORPUS 1 (BUT THESE ARE DIFFERENT !!!)
			extractor.extract(typeCorpus, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
   		'if corpus type 2 and extOption=1, we use a modified index list' #!!!!!!!!!!
		return

	def prepareTest(self, corpus, typeCorpus, indiceSvm = 0):
		"""
		Prepare CRF test data
		
		Parameters
		----------
		corpus : Corpus
		typeCorpus : int, {1, 2, 3}
			1 : corpus 1, 2 : corpus 2...
		indiceSvm : int, {0, -1, 2}
			0 : normal(corpus 1)
			-1 : data04SVM (corpus2),
			-3 : corpus3
			2 : external data => svm isn't called
		"""
		listReferences = corpus.getListReferences(typeCorpus)
		listReferencesObj = ListReferences(listReferences, typeCorpus)
		
		extractor = Extract_crf(self.options)
		nbRef = corpus.nbReference(typeCorpus)
		
		'generation of test index for each reference'
		extractor.randomgen(ListReferences(listReferencesObj.getReferences(),typeCorpus), 0)
		
		if indiceSvm == -1:
			extractor.extract(typeCorpus, nbRef, self.dirResult+"data04SVM_ori.txt", ListReferences(listReferencesObj.getReferences(),typeCorpus))
		
		if indiceSvm == -2:
                        extractor.extract(typeCorpus, nbRef, self.dirResult+"data04SVM_ori.txt", ListReferences(listReferencesObj.getReferences(),typeCorpus))

		else:
			'file for CRF training'
			if typeCorpus == 2 and indiceSvm != 2 :
				extractor.extractIndices4new(self.dirResult+"svm_predictions_new", ListReferences(listReferencesObj.getReferences(),typeCorpus))
			
				extractor.extract(typeCorpus, nbRef, self.dirResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -1, 1)
				extractor.extract(typeCorpus, nbRef, self.dirResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), 0, 1)
                        'file for CRF training'
                        if typeCorpus == 3  :
                                #extractor.extractIndices4new(self.dirResult+"svm_predictions_new", ListReferences(listReferencesObj.getReferences(),typeCorpus))

                        	extractor.extract(typeCorpus, nbRef, self.dirResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -1, 1)
                        	extractor.extract(typeCorpus, nbRef, self.dirResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), 0, 1)

		return ListReferences(listReferencesObj.getReferences(),typeCorpus)


	def runTrain(self, directory, fichier, modelname, penalty=0.00001) :
		"""
		Run CRF training module from Wapiti software
		
		Parameters
		----------
		directory : string
			directory where we save the model
		fichier : string
			filename that has been generated by preprareTrain
		"""
		dependencyDir = os.path.join(self.rootDir, 'dependencies')
		command = dependencyDir+"/wapiti-1.4.0/wapiti train -p "+self.rootDir+"/KB/config/wapiti/pattern_ref -2 "+str(penalty)+" "+self.dirResult+fichier+" "+directory+modelname
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()

		return


	def runTest(self, directory, fichier, modelname, addStr="") :
		"""
		Run CRF test module from Wapiti software to label new data
		
		Parameters
		----------
		directory : string
			directory where we save the model
		fichier : string
			filename that has been generated by preprareTest
		"""
		dependencyDir = os.path.join(self.rootDir, 'dependencies')
		command = dependencyDir+"/wapiti-1.4.0/wapiti label -m "+directory+modelname+" "+self.dirResult+fichier+" "+self.dirResult+"testEstCRF"+addStr+"_Wapiti.txt"
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
		'Create testEstCRF.txt keeping only predicted labels'
		fafter = open(self.dirResult+"testEstCRF"+addStr+".txt", 'w', encoding='utf8')
		for line in open(self.dirResult+"testEstCRF"+addStr+"_Wapiti.txt", 'r', encoding='utf8') :
			line = line.split()
			if len(line) > 0 :
				fafter.write(str(line[len(line)-1]))
				fafter.write("\n")
			else : fafter.write("\n")
		fafter.close()
		if addStr == "" :
			self.generateXml.simpleComp(self.dirResult+"testdata_CRF.txt", self.dirResult+'testEstCRF.txt', 2, self.dirResult+'testEstCRF.xml')
		return


	def postProcessTest(self, fnameCRFresult, fnameCRFtoAdd, refsAfterSVM):
		"""
		Post-processing of labeling result. After a normal CRF labeling, we return to the SVM classification result,
		then check which notes should be annotated as non-bibliographic ones, then actually modify the labeling result.
		
		Parameters
		----------
		fnameCRFresult : string
			directory where we save the model
		fnameCRFtoAdd : string
			filename that has been generated by preprareTest
		refsAfterSVM : list of 'Reference' objects
			reference list containing SVM classification result
		"""
		
		fbefore = open(self.dirResult+fnameCRFresult, 'r')
		fafter = open(self.dirResult+fnameCRFtoAdd, 'w')
		
		for reference in refsAfterSVM :
			if reference.train != -1 :
				line = fbefore.readline()
				while (len(line.split()) > 0) :
					fafter.write(str(line))
					line = fbefore.readline()
				fafter.write("\n")
			elif len(reference.getWord()) > 0 : # if there is no word in the reference, it was already ignored in printing before
				line = fbefore.readline()
				while (len(line.split()) > 0) :
					fafter.write("nonbibl \n")
					line = fbefore.readline()
				fafter.write("\n")
		fafter.close()
		fbefore.close()
		
		self.generateXml.simpleComp(self.dirResult+"testdata_CRF.txt", self.dirResult+fnameCRFtoAdd, 2, self.dirResult+'testEstCRF.xml')
		
		return
