# -*- coding: utf-8 -*-
'''
Created on 4 juin 2012

@author: Young-Min Kim, Jade Tavernier
'''
import subprocess
from mypkg.format.Extract_svm import Extract_svm

class SVM(object):
    '''
    classdocs
    '''


    def __init__(self, dirResult):
        '''
        Constructor
        '''
        self.dirResult = dirResult
       
    '''
    prepareTrain : prepare les fichier pour SVM
    '''
    def prepareTrain(self, corpus):
        nbRef = corpus.nbReference(2) #corpus type = 2
        extractor = Extract_svm()
        
        extractor.extractor(self.dirResult+"data04SVM_ori.txt", nbRef, 1, self.dirResult+"data04SVM_ori.txt", self.dirResult+"trainingdata_SVM.txt")
      
    '''
    prepareTest : prepare les fichier pour SVM
    '''
    def prepareTest(self, corpus):
        nbRef = corpus.nbReference(2) #corpus type = 2
        extractor = Extract_svm()
        
        extractor.extractor(self.dirResult+"data04SVM_ori.txt", nbRef, 0, self.dirResult+"data04SVM_ori.txt", self.dirResult+"newdata.txt")
            
    '''
    runTrain : lance SVM pour l'apprentissage
    '''
    def runTrain(self, directoryModel):
        command = 'dependencies/svm_light/svm_learn '+self.dirResult+'trainingdata_SVM.txt '+directoryModel+'svm_revues_model'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        command = 'dependencies/svm_light/svm_classify '+self.dirResult+'trainingdata_SVM.txt '+directoryModel+'svm_revues_model '+directoryModel+'svm_revues_predictions_training'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()
        
    def runTest(self, directoryModel):
        command = 'dependencies/svm_light/svm_classify '+self.dirResult+'newdata.txt '+directoryModel+'svm_revues_model '+directoryModel+'svm_revues_predictions_new'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()