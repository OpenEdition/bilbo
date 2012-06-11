#!/usr/bin/env python
# encoding: utf-8
"""
runSVM.py

Created by Young-Min Kim on 2012-02-16.

This code learns a SVM model for note classification. Classified result is recorded in a file.
The result files are
<svm_revues_predition> <svm_revues_predition2>

With this result and SVM learning index file <all_indices_C2_train.txt>,
also CRF learning index file already prepared for non-classified notes, <train_indices.txt>,
call the file <positive_indices.py>
genrate <positive_indices.txt>


$ svm_light/svm_learn ../Project/trainingdata.txt ../Project/svm_revues_model
$ svm_light/svm_classify ../Project/testdata.txt ../Project/svm_revues_model ../Project/svm_revues_predictions
$ svm_light/svm_classify ../Project/trainingdata.txt ../Project/svm_revues_model ../Project/svm_revues_predictions2


CRF data extraction

$ python positive_indices.py all_indices_C2_train.txt svm_revues_predition svm_revues_predition2 train_indices.txt > positive_indices.txt
$ mv positive_indices.txt train_indices.txt
$ 
"""

import sys
import os
import subprocess



def run(svmdirname, crfdirname, crfcodedir, indicator) :

	
	# SVM learning and prediction
	
	if indicator == 10 or indicator == 20 :
		print 'SVM learning\n'
		command = '/Users/young-minkim/Applications/svm_light/svm_learn '+svmdirname+'/trainingdata.txt '+svmdirname+'/svm_revues_model'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()

	if indicator != 2 and indicator != 4 :
		print 'SVM prediction for testdata\n'
		command = '/Users/young-minkim/Applications/svm_light/svm_classify '+svmdirname+'/testdata.txt '+svmdirname+'/svm_revues_model '+svmdirname+'/svm_revues_predictions'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()	
	
		print 'SVM prediction for trainingdata\n'
		command = '/Users/young-minkim/Applications/svm_light/svm_classify '+svmdirname+'/trainingdata.txt '+svmdirname+'/svm_revues_model '+svmdirname+'/svm_revues_predictions2'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()
		
	else :	
		print 'SVM prediction for newdata\n'
		command = '/Users/young-minkim/Applications/svm_light/svm_classify '+svmdirname+'/newdata.txt '+svmdirname+'/svm_revues_model '+svmdirname+'/svm_revues_predictions_new'
		process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
		process.wait()

		
	#CRF data generation
	sd = svmdirname
	if indicator != 2 and indicator != 4:
		print 'Start extracting CRF training and/or test data... '
		var = raw_input('If you want to generate a new list of training/test data indicator file, enter y. If not, just enter : ')
		command = ''
		if len(var) > 0 :
			command = 'python '+crfcodedir+'/extractor.py '+sd+'/tmp_result2.txt 100 1 > train_indices.txt'  
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			print 'training indices are regenerated.\n'
	
		command = 'python '+sd+'/positive_indices.py '+sd+'/all_indices_C2_train.txt '+sd+'/svm_revues_predictions '+sd+'/svm_revues_predictions2 '+sd+'/train_indices.txt > positive_indices.txt'
		#print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		process = subprocess.Popen('mv train_indices.txt all_train_indices.txt', shell=True, stdout=subprocess.PIPE)
		process.wait()
		process = subprocess.Popen('mv positive_indices.txt train_indices.txt', shell=True, stdout=subprocess.PIPE)
		process.wait()
		
	else :
		command = 'python '+sd+'/positive_indices.py '+sd+'/svm_revues_predictions_new > train_indices.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
	if indicator != 2 and indicator != 4:
	
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt 1 1 > '+crfdirname+'/trainingdata_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()	
		
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt 0 1 > '+crfdirname+'/testdata_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -1 1 > '+crfdirname+'/testdatawithlabel_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -2 1 > '+crfdirname+'/testdataonlylabel_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		
		if indicator == 20 :
			command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt 1 4 > '+crfdirname+'/trainingdata_rich_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()	
			command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -1 3 > '+crfdirname+'/testdata_rich_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -1 4 > '+crfdirname+'/testdatawithlabel_rich_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
	
		process = subprocess.Popen('cp all_train_indices.txt '+crfdirname+'/', shell=True, stdout=subprocess.PIPE)
		process.wait()
		process = subprocess.Popen('mv train_indices.txt '+crfdirname+'/', shell=True, stdout=subprocess.PIPE)
		process.wait()

	else :
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt 0 1 > '+crfdirname+'/newdata_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -1 1 > '+crfdirname+'/newdatawithlabel_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -2 1 > '+crfdirname+'/newdataonlylabel_CRF.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		
		if indicator == 4 :
			command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -1 5 > '+crfdirname+'/newdata_rich_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			command = 'python '+crfcodedir+'/extractor.py '+svmdirname+'/tmp_result2.txt -1 6 > '+crfdirname+'/newdatawithlabel_rich_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()	
			

	print 'end of CRF data extraction.'
	
	#process = subprocess.Popen('rm tmp.txt tmp_notefile ', shell=True, stdout=subprocess.PIPE)
	#process.wait()
	
	return



def main() :
	if sys.argv[1] == "1":
		run("src/mypkg/format/note/", "./", "src/mypkg/format/note/", 1)
	else:
		if len(sys.argv) != 5 :
			print '** SVM learning and CRF data extraction (training/test) **'
			print 'python runSVM.py (dirname including SVM training and/or test data) (dirname for CRF output) (dirname for CRF codes) (10:svm train/test both, 20:all data including rich data, 2:new data, 4:all new data including rich data)'
			sys.exit(1)
			
		svmdirname = str(sys.argv[1])
		crfdirname = str(sys.argv[2])
		crfcodedir = str(sys.argv[3])	
		indicator = int(sys.argv[4])
			
		run(svmdirname, crfdirname, crfcodedir, indicator)


if __name__ == '__main__':
	main()
