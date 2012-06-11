#!/usr/bin/env python
# encoding: utf-8
"""

positive_indices.py

Created by Young-Min Kim on 2011-11-02.
Modified by Young-Min Kim on 2012-02-13.
From all_indices_C2_train.txt, svm_revues_predition(test data), svm_revues_predition2(training data),
train_indices.txt (CRF indices without classification)extract positive_indices.txt, which includes 
all positive note indices estimated SVM classifier. 


"""

import sys
import os
import string
import random


def extractorIndices(svmprediction_trainfile, listRef):
	nbRef = listRef.nbReference()
	
	svm_train = []
	for line in open (svmprediction_trainfile, 'r') :
		line = line.split()
		svm_train.append(float(line[0]))	

	positive_indices = range(nbRef)
	
	n=0 #for all
	j=0	#for train
	for n in range(nbRef) :
		if svm_train[j] > 0 :
			positive_indices[n] = 1
		else :
			positive_indices[n] = 0
		j += 1
	
	
	n=0
	for ref in listRef.getReferences() :
		if positive_indices[n] == 0 : # instance NOT OK donc attribut train = -1
			ref.train =  -1 
		n += 1
	
	return
	
	
def extractor4new(svmprediction_newfile, listRef):
	i = 0
	
	for line in open (svmprediction_newfile, 'r') :
		line = line.split()
		if float(line[0]) > 0 :
			listRef.getReferencesIndice(i).train = 0
		else :
			listRef.getReferencesIndice(i).train = -1
		i += 1
	return


def main():
	if len (sys.argv) != 5 and len (sys.argv) != 2:
		print 'python positive_indices.py (ind_svmtrainfile) (svmprediction_testfile) (svmprediction_trainfile) (ind_crftrainfile)'
		print 'or'
		print 'python positive_indices.py (svmprediction_newfile)'
		##python positive_indices.py all_indices_C2_train.txt svm_revues_predition svm_revues_predition2 train_indices.txt > positive_indices.txt
		sys.exit (1)

	if len (sys.argv) == 5 :
		extractorIndices(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
	elif len (sys.argv) == 2 :
		extractor4new(str(sys.argv[1]))

if __name__ == '__main__':
	main()



