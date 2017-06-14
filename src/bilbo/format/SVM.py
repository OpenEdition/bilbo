# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on June 4, 2012

@author: Young-Min Kim, Jade Tavernier
"""
import subprocess, os
from bilbo.format.Extract_svm import Extract_svm

class SVM(object):
    
    def __init__(self, dirResult, options={}):
        self.dirResult = dirResult
        self.options = options
        main = os.path.realpath(__file__).split('/')
        self.rootDir = "/".join(main[:len(main)-4])


    def prepareTrainNote(self, corpus):
        nbRef = corpus.nbReference(2) #corpus type = 2
        extractor = Extract_svm(self.options)
        extractor.extract(self.dirResult+"data04SVM_ori.txt", nbRef, 1, self.dirResult+"data04SVM_ori.txt", self.dirResult+"trainingdata_SVM.txt")
        
    def prepareTrainP(self, corpus):
        nbRef = corpus.nbReference(3) #corpus type = 3
        extractor = Extract_svm(self.options)
        extractor.extractP(self.dirResult+"data04SVM_ori.txt", nbRef, 1, self.dirResult+"data04SVM_ori.txt", self.dirResult+"trainingdata_SVM.txt")


    def prepareTest(self, corpus):
        nbRef = corpus.nbReference(2) #corpus type = 2
        extractor = Extract_svm(self.options)
        extractor.extract(self.dirResult+"data04SVM_ori.txt", nbRef, 0, self.dirResult+"data04SVM_ori.txt", self.dirResult+"newdata.txt")

    def prepareTestP(self, corpus):
        nbRef = corpus.nbReference(3) #corpus type = 3
        extractor = Extract_svm(self.options)
        extractor.extract(self.dirResult+"data04SVM_ori.txt", nbRef, 0, self.dirResult+"data04SVM_ori.txt", self.dirResult+"newdata.txt")

    def runTrain(self, directoryModel):
        dependencyDir = os.path.join(self.rootDir, 'dependencies')
        command = dependencyDir+'/svm_light/svm_learn '+self.dirResult+'trainingdata_SVM.txt '+directoryModel+'svm_model'
        #print('Train :'+command)
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        command = dependencyDir+'/svm_light/svm_classify '+self.dirResult+'trainingdata_SVM.txt '+directoryModel+'svm_model '+self.dirResult+'svm_predictions_training'
        #print('Annote :'+command)        
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()


    def runTest(self, directoryModel):
        dependencyDir = os.path.join(self.rootDir, 'dependencies')
        command = dependencyDir+'/svm_light/svm_classify '+self.dirResult+'newdata.txt '+directoryModel+'svm_model '+self.dirResult+'svm_predictions_new'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()