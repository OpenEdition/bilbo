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
from codecs import open

class CRF(object):
    def __init__(self, dirResult, options={}):
        self.generateXml = GenerateXml()
        self.dirResult = dirResult
        self.options = options
        self.dirModel = ""
        main = os.path.realpath(__file__).split('/')
        self.rootDir = "/".join(main[:len(main)-4])


    def setDirModel(self, dirModel):
        self.dirModel = dirModel


    def prepareTrain(self, corpus, typeCorpus, fileRes, tr=-1, extOption=-1, optsvm=True):
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
        if typeCorpus == 3 and extOption == 1:
            'modify the indices to eliminate the reference (or not print the reference) classified as non-bibl BY SVM'
            if optsvm == True : #if not, do not modify
                extractor.extractIndices(self.dirResult+"svm_predictions_training", newListReferences)
            extractor.extract(typeCorpus, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
        else: # typeCorpus == 1 or (typeCorpus == 2 and isFrstExt == -1)
        ########## SOURCE DATA EXTRACTION FOR SVM OR CORPUS 1 (BUT THESE ARE DIFFERENT !!!)
            extractor.extract(typeCorpus, nbRef, self.dirResult+fileRes, newListReferences, tr, extOption)
            
        return

    def prepareTest(self, corpus, typeCorpus, indiceSvm = 0):
        listReferences = corpus.getListReferences(typeCorpus)
        listReferencesObj = ListReferences(listReferences, typeCorpus)
        
        extractor = Extract_crf(self.options)
        nbRef = corpus.nbReference(typeCorpus)
        #print(nbRef)
        #print(listReferences)
        extractor.randomgen(ListReferences(listReferencesObj.getReferences(),typeCorpus), 0)
        
        if indiceSvm == -1:
            extractor.extract(typeCorpus, nbRef, self.dirResult+"data04SVM_ori.txt", ListReferences(listReferencesObj.getReferences(),typeCorpus))
        else:
            if typeCorpus == 2 and indiceSvm != 2 :
                extractor.extractIndices4new(self.dirResult+"svm_predictions_new", ListReferences(listReferencesObj.getReferences(),typeCorpus))
                extractor.extract(typeCorpus, nbRef, self.dirResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -1, 1)
                extractor.extract(typeCorpus, nbRef, self.dirResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), 0, 1)
            if typeCorpus == 3 and indiceSvm != 2 :
                extractor.extractIndices4new(self.dirResult+"svm_predictions_new", ListReferences(listReferencesObj.getReferences(),typeCorpus))
                extractor.extract(typeCorpus, nbRef, self.dirResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -1, 1)
                extractor.extract(typeCorpus, nbRef, self.dirResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), 0, 1)
        return ListReferences(listReferencesObj.getReferences(),typeCorpus)
        
        
    def prepareTestWithoutSVM(self, corpus, typeCorpus, indiceSvm = 0):
        listReferences = corpus.getListReferences(typeCorpus)
        listReferencesObj = ListReferences(listReferences, typeCorpus)
        
        extractor = Extract_crf(self.options)
        nbRef = corpus.nbReference(typeCorpus)
        #print(nbRef)
        #print(listReferences)
        extractor.randomgen(ListReferences(listReferencesObj.getReferences(),typeCorpus), 0)
        
        extractor.extract(typeCorpus, nbRef, self.dirResult+"testdatawithlabel_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), -1, 1)
        extractor.extract(typeCorpus, nbRef, self.dirResult+"testdata_CRF.txt",ListReferences(listReferencesObj.getReferences(),typeCorpus), 0, 1)
        return ListReferences(listReferencesObj.getReferences(),typeCorpus)


    def runTrain(self, directory, fichier, modelname, penalty=0.00001) :
        dependencyDir = os.path.join(self.rootDir, 'dependencies')
        command = dependencyDir+"/wapiti-1.4.0/wapiti train -p "+self.rootDir+"/KB/config/wapiti/pattern_ref -2 "+str(penalty)+" "+self.dirResult+fichier+" "+directory+modelname
        #print('Wapiti :'+command)        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        return


    def runTest(self, directory, fichier, modelname, addStr="") :
        dependencyDir = os.path.join(self.rootDir, 'dependencies')
        command = dependencyDir+"/wapiti-1.4.0/wapiti label -m "+directory+modelname+" "+self.dirResult+fichier+" "+self.dirResult+"testEstCRF"+addStr+"_Wapiti.txt"
        #print(command)        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
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
        
        
    def runTestBibl(self, directory, fichier, modelname, addStr="") :
        dependencyDir = os.path.join(self.rootDir, 'dependencies')
        command = dependencyDir+"/wapiti-1.4.0/wapiti label -m "+directory+modelname+" "+self.dirResult+fichier+" "+self.dirResult+"testEstCRF"+addStr+"_Wapiti.txt"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        fafter = open(self.dirResult+"testEstCRF"+addStr+"2.txt", 'w', encoding='utf8')
        for line in open(self.dirResult+"testEstCRF"+addStr+"_Wapiti2.txt", 'r', encoding='utf8') :
            line = line.split()
            if len(line) > 0 :
                fafter.write(str(line[len(line)-1]))
                fafter.write("\n")
            else : fafter.write("\n")
        fafter.close()
        if addStr == "" :
            self.generateXml.simpleComp(self.dirResult+"testdata_CRF2.txt", self.dirResult+'testEstCRF2.txt', 2, self.dirResult+'testEstCRF2.xml')
        return

    def postProcessTest(self, fnameCRFresult, fnameCRFtoAdd, refsAfterSVM):
        fbefore = open(self.dirResult+fnameCRFresult, 'r')
        fafter = open(self.dirResult+fnameCRFtoAdd, 'w')
        
        for reference in refsAfterSVM :
            #print(reference.affiche())
            if reference.train != -1 :
                print('*********')
                print(reference.affiche())
                line = fbefore.readline()
                while (len(line.split()) > 0) :
                    fafter.write(str(line))
                    line = fbefore.readline()
                    #print('****'+line)
                fafter.write("\n")
            elif len(reference.getWord()) > 0 :
                #print(reference.getWord())
                line = fbefore.readline()
                #print('-------'+line)
                while (len(line.split()) > 0) :
                    fafter.write("nonbibl \n")
                    line = fbefore.readline()
                fafter.write("\n")
        fafter.close()
        fbefore.close()
        
        self.generateXml.simpleComp(self.dirResult+"testdata_CRF.txt", self.dirResult+fnameCRFtoAdd, 2, self.dirResult+'testEstCRF.xml')
        return
        
    def postProcessTestP(self, fnameCRFresult, fnameCRFtoAdd, refsAfterSVM):
        fbefore = open(self.dirResult+fnameCRFresult, 'r')
        fafter = open(self.dirResult+fnameCRFtoAdd, 'w')
        
        for reference in refsAfterSVM :
            if reference.train != -1 :
                line = fbefore.readline()
                while (len(line.split()) > 0) :
                    fafter.write(str(line))
                    line = fbefore.readline()
                fafter.write("\n")
            elif len(reference.getWord()) > 0 :
                line = fbefore.readline()
                while (len(line.split()) > 0) :
                    fafter.write("nonbibl \n")
                    line = fbefore.readline()
                fafter.write("\n")
        fafter.close()
        fbefore.close()
        
        self.generateXml.simpleComp(self.dirResult+"testdata_CRF2.txt", self.dirResult+fnameCRFtoAdd, 2, self.dirResult+'testEstCRF2.xml')
        return
