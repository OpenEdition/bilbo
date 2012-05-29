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


def extractor(ind_trainfile, svmprediction_testfile, svmprediction_trainfile, ind_trainCRFfile):
	
	indices_tr = []
	for line in open (ind_trainfile, 'r') :
		line = line.split()
		indices_tr.append(int(line[0]))
		
	svm_test = []
	for line in open (svmprediction_testfile, 'r') :
		line = line.split()
		svm_test.append(float(line[0]))
		
	svm_train = []
	for line in open (svmprediction_trainfile, 'r') :
		line = line.split()
		svm_train.append(float(line[0]))	

	ind_trainCRF = [] 
	for line in open (ind_trainCRFfile, 'r') :# file to be modified, in general, train_indices.txt
		line = line.split()
		ind_trainCRF.append(float(line[0]))	
		
	
	positive_indices = range(len(indices_tr))
	
	n=0 #for all
	i=0	#for test
	j=0	#for train

	for n in range(len(indices_tr)) :
		if indices_tr[n] == 0 : # test data ?
			if svm_test[i] > 0 :
				positive_indices[n] = 1
			else :
				positive_indices[n] = 0
			i += 1
		else : # train datat
			if svm_train[j] > 0 :
				positive_indices[n] = 1
			else :
				positive_indices[n] = 0
			j += 1
	
	
	final_CRFindices = range(len(indices_tr))
	n=0
	for n in range(len(positive_indices)) :
		if positive_indices[n] > 0 : # instance OK for bibliographical reference
			if ind_trainCRF[n] == 1 :
				final_CRFindices[n] = 1
			else :
				final_CRFindices[n] = 0
		else : # instance NOT OK
			final_CRFindices[n] = -1 
			
	for fcrf in final_CRFindices :
		print fcrf	
	
	return
	
	
def extractor4new(svmprediction_newfile):
	for line in open (svmprediction_newfile, 'r') :
		line = line.split()
		if float(line[0]) > 0 :
			print 0
		else :
			print -1
	
	return


def main():
	if len (sys.argv) != 5 and len (sys.argv) != 2:
		print 'python positive_indices.py (ind_svmtrainfile) (svmprediction_testfile) (svmprediction_trainfile) (ind_crftrainfile)'
		print 'or'
		print 'python positive_indices.py (svmprediction_newfile)'
		##python positive_indices.py all_indices_C2_train.txt svm_revues_predition svm_revues_predition2 train_indices.txt > positive_indices.txt
		sys.exit (1)

	if len (sys.argv) == 5 :
		extractor(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
	elif len (sys.argv) == 2 :
		extractor4new(str(sys.argv[1]))

if __name__ == '__main__':
	main()



