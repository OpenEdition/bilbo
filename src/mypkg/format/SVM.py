'''
Created on 4 juin 2012

@author: jade
'''
import subprocess
from mypkg.format.note.featureSelection4SVM import *

class SVM(object):
    '''
    classdocs
    '''


    def __init__(self, repResult):
        '''
        Constructor
        '''
        self.repResult = repResult
       
    '''
    prepareTrain : prepare les fichier pour SVM
    '''
    def prepareTrain(self, corpus):
        nbRef = corpus.nbReference(2)
        
        selector(self.repResult+"data04SVM_ori.txt", nbRef, 1, self.repResult+"data04SVM_ori.txt", self.repResult+"trainingdata_SVM.txt")
      
    '''
    prepareTest : prepare les fichier pour SVM
    '''
    def prepareTest(self, corpus):
        nbRef = corpus.nbReference(2)
        
        selector(self.repResult+"data04SVM_ori.txt", nbRef, 2, self.repResult+"data04SVM_ori.txt", self.repResult+"newdata.txt")
         
            
    '''
    runTrain : lance SVM pour l'apprentissage
    '''
    def runTrain(self, repertoireModel):
        command = 'dependencies/svm_light/svm_learn '+self.repResult+'trainingdata_SVM.txt '+repertoireModel+'svm_revues_model'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        command = 'dependencies/svm_light/svm_classify '+self.repResult+'trainingdata_SVM.txt '+repertoireModel+'svm_revues_model '+repertoireModel+'svm_revues_predictions_training'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()
        
    def runTest(self, repertoireModel):
        command = 'dependencies/svm_light/svm_classify '+self.repResult+'newdata.txt '+repertoireModel+'svm_revues_model '+repertoireModel+'svm_revues_predictions_new'
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()