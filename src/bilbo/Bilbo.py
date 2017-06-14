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

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.format.CRF import CRF
from bilbo.format.SVM import SVM
from bilbo.reference.Corpus import Corpus
import os, sys
import shutil
from tempfile import mkdtemp
from glob import glob
from codecs import open
import re

class Bilbo(object):
    def __init__(self, dirResult='', options={}, crfmodelname="crf_model_simple"): #Set the default result directory
        main = os.path.realpath(__file__).split('/')
        self.rootDir = "/".join(main[:len(main)-3])
		
        if dirResult == '' : dirResult = os.path.join(self.rootDir, 'Result')
        if not os.path.exists(dirResult): os.makedirs(dirResult)
        self.dirResult = mkdtemp(dir = dirResult) + '/'
        self.crf = CRF(self.dirResult, options)
        self.svm = SVM(self.dirResult, options)
        self.options = options
        self.crfmodelname = crfmodelname


    def train(self, dirCorpus, dirModel, typeCorpus):
        corpus = Corpus(dirCorpus, self.options)
        corpus_bibl = Corpus(dirCorpus, self.options)
        self.crf.setDirModel(dirModel)
        if typeCorpus == 1:
            print("Extract references...")
            corpus.extract(1, "bibl")
            print("crf training data extraction...")
            self.crf.prepareTrain(corpus, 1, "trainingdata_CRF.txt", 1, 1) #CRF training data extraction
            self.crf.runTrain(dirModel, "trainingdata_CRF_Wapiti.txt", self.crfmodelname) #CRF model learning
				
        if typeCorpus == 2:
            print("Extract notes...")
            corpus.extract(2, "note")
            optsvm = self.options.s
            if optsvm == True :
                print("svm source data extraction...")
                self.crf.prepareTrain(corpus, 2, "data04SVM_ori.txt", 1) #Source data extraction for SVM note classification
                print("svm training data extraction...")
                self.svm.prepareTrainNote(corpus) #Training data extraction for SVM note classification
                print("svm training...")
                self.svm.runTrain(dirModel) #SVM model learning
            
            print("crf training data extraction...")
            self.crf.prepareTrain(corpus, 2, "trainingdata_CRF.txt", 1, 1, optsvm) #CRF training data extraction
            self.crf.runTrain(dirModel, "trainingdata_CRF_Wapiti.txt", self.crfmodelname) #CRF model learning
            #self.crf.runTrain(dirModel, "trainingdata_CRF_nega_Wapiti.txt", "revueswapiti_nega", 0.0000001) #Do not work, too homogeneous
        
        elif typeCorpus == 3:
            print("Extract paragraphs...")
            corpus.extract(3, "p")
            optsvm = self.options.s
            if optsvm == True :
                print("svm source data extraction...")
                self.crf.prepareTrain(corpus, 3, "data04SVM_ori.txt", 1) #Source data extraction for SVM note classification
                print("svm training data extraction...")
                self.svm.prepareTrainP(corpus) #Training data extraction for SVM note classification
                print("svm training...")
                self.svm.runTrain(dirModel) #SVM model learning

                print("Lower crf training data extraction...")
                self.crf.prepareTrain(corpus, 3, "trainingdata_LowerCRF.txt", 1, 1, optsvm) #CRF training data extraction
                self.crf.runTrain(dirModel, "trainingdata_LowerCRF_Wapiti.txt", self.crfmodelname+'_Lower') #CRF model learning

                corpus_bibl.extractBibl(3, "bibl")
                print("Upper crf training data extraction...")
                self.crf.prepareTrain(corpus_bibl, 3, "trainingdata_UpperCRF.txt", 1, 1) #CRF training data extraction
                self.crf.runTrain(dirModel, "trainingdata_UpperCRF_OriginalWapiti.txt", self.crfmodelname+'_Upper') #CRF model learning
                
            else :
                print("CRF training data extraction...")
                self.crf.prepareTrain(corpus, 3, "trainingdata_CRF.txt", 1, 1, 'False')
                self.crf.runTrain(dirModel, "trainingdata_CRF_Wapiti.txt", self.crfmodelname+'_P')

        print
    #self.deleteTmpFiles()


    def annotate(self, dirCorpus, dirModel, typeCorpus, external=0):
        print('Corpus: '+dirCorpus)
        corpus = Corpus(dirCorpus, self.options)
        self.crf.setDirModel(dirModel)
        files = corpus.getFiles()
        filesTab = self._list_split(files, 50)
        for fname in filesTab:
            if typeCorpus == 1:
                corpus = self.annotateCorpus1(dirModel, corpus, fname)
            if typeCorpus == 2:
                corpus = self.annotateCorpus2(dirModel, corpus, fname, external)
            if typeCorpus == 3:
                corpus = self.annotateCorpus3(dirModel, corpus, fname, external)
            #corpus.deleteAllFiles()
			
		#self.deleteTmpFiles()


    def annotateCorpus1(self, dirModel, corpus, fname):
        print ("Extract references...")
        corpus.extract(1, "bibl", fname)
        print ("crf data extraction for labeling...")
        self.crf.prepareTest(corpus, 1)
        print ("crf run test for labeling...")
        self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
        print ("corpus add tag for labeling...")
        corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "bibl", 1)
        
        return corpus


    def annotateCorpus2(self, dirModel, corpus, fname, external=0):
        print ("Extract notes...")
        corpus.extract(2, "note", fname, external)
        if external == 0 and self.options.s : #if not external data and svm option is true
            print ("svm source data extraction...")
            self.crf.prepareTest(corpus, 2, -1) 	#last argument:int, -1:prepare source data for SVM learning, default:0
            print ("svm data extraction for labeling...")
            self.svm.prepareTest(corpus)
            self.svm.runTest(dirModel)
            
            print ("crf data extraction for labeling...")
            newlistReferences = self.crf.prepareTest(corpus, 2)
            self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
            self.crf.postProcessTest("testEstCRF.txt", "testEstCLNblCRF.txt", newlistReferences.getReferences())
            corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "note", 2, newlistReferences.getReferences())
        else:										#if external data : external=1, we do not call a SVM model
            print ("crf data extraction for labeling...")
            self.crf.prepareTest(corpus, 2, 2)		#indiceSvm=2 at prepareTest(self, corpus, typeCorpus, indiceSvm = 0)
            print ("crf run test for labeling...")
            self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname)
            print ("corpus add tag for labeling...")
            corpus.addTagReferences(self.dirResult, "testEstCRF.xml", "note", 2)
        return corpus
        
        
        
    def annotateCorpus3(self, dirModel, corpus, fname, external=0):
        corpus_Bibl = Corpus('Result/test/corpus_JustBibl/', self.options)
        print("Extract paragraphs...")
        corpus.extract(3, "p", fname, external)
        if external == 0 and self.options.s : #if not external data and svm option is true
            
            print("svm source data extraction...")
            self.crf.prepareTest(corpus, 3, -1) 	#last argument:int, -1:prepare source data for SVM learning, default:0
            print("svm data extraction for labeling...")
            self.svm.prepareTestP(corpus)
            self.svm.runTest(dirModel)
            print("Lower crf data extraction for labeling...")
            newlistReferences = self.crf.prepareTest(corpus, 3) 
            self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname+'_Lower')
            self.crf.postProcessTest("testEstCRF.txt", "testEstCLNblCRF.txt", newlistReferences.getReferences())
            corpus.addTagReferencesP(self.dirResult, "testEstCRF.xml", "p", 3, newlistReferences.getReferences())
            '''
            print("Upper crf data extraction for labeling...")
            
            corpus_Bibl.extractBibl(3, "bibl", fname)
            self.crf.prepareTestWithoutSVM(corpus_Bibl, 3) 
            
            print ("crf run test for labeling...")
            self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname+'_Upper')
            print ("corpus add tag for labeling...")
            
            #corpus.addTagReferencesFinal(self.dirResult, "testEstCRF.xml", "p", 3)
            corpus.addTagReferencesFinal(self.dirResult, "testEstCRF.xml", "p", 3, newlistReferences.getReferences())
            
        else:
           
            print("Upper crf data extraction for labeling...")
            self.crf.prepareTestWithoutSVM(corpus, 3, 2)         
            print ("crf run test for labeling...")
            self.crf.runTest(dirModel, 'testdata_CRF_Wapiti.txt', self.crfmodelname+'_P')
            print ("corpus add tag for labeling...")
            corpus.addTagReferencesBibl(self.dirResult, "testEstCRF.xml", "p", 3)
            '''
            
        return corpus
        
    def postprocess(self, fname) :
        file = open (fname, 'r', encoding='utf8', errors='replace')
        output = open (fname+'2', 'w', encoding='utf8', errors='replace')
        content = file.readlines()
        for line in content:
            line = re.sub('<hi.*?>', '', line)
            line = re.sub('</hi>', '', line)
            line = line.strip()
            newline=''
            if line.startswith('<bibl>'):
                line = re.sub('<bibl>', '', line)
            if line.endswith('</bibl>'):
                line = re.sub('</bibl>', '', line)
            output.write(line)
            output.write('\n')
        output.close()
        
    def scandirs(self,path):
        for root, dirs, files in os.walk(path):
            for currentFile in files:
                print ("processing file: " )+ currentFile
                exts = ('.xml')
                if any(currentFile.lower().endswith(ext) for ext in exts):
                    os.remove(os.path.join(root, currentFile))
                    
    def replaceName(self,folder):
        for filename in os.listdir(folder):
            infilename = os.path.join(folder,filename)
            if not os.path.isfile(infilename): continue
            oldbase = os.path.splitext(filename)
            newname = infilename.replace('.xml2', '.xml')
            output = os.rename(infilename, newname)
        

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
        result = [[]]
        while len(flist) > 0:
            if len(result[-1]) >= size: result.append([])
            result[-1].append(flist.pop(0))
        return result


    """memory"""
    def mem(self, size="rss"):
        return os.popen('ps -p %d -o %s | tail -1' % (os.getpid(), size)).read()

    def rss(self):
        return self.mem("rss")

    def rsz(self):
        return self.mem("rsz")

    def vsz(self):
        return self.mem("vsz")
