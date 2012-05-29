#!/usr/bin/env python
# encoding: utf-8
"""
preparerSVM.py

Created by Young-Min Kim on 2011-09-09.

This code calls the excutable files for the corpus 2.


noteExtractorC2.py
python noteExtractorC2.py Data/Corpus2/alldata/ Data/Corpus2/filename2all > Data/Corpus2/resultCor2_allNotes.xml

dataGeneratorV3C2.py 
python dataGeneratorV3C2.py Data/Corpus2/ filenames2.txt > resultCor2_today.txt

puncOrganizer.py
python puncOrganizer.py resultCor2_today.txt > resultCor2_today2.txt

extractor4SVM.py
python extractor4SVM.py resultCor2_today2.txt 2 > data04SVM_ori.txt
python extractor4SVM.py resultCor2_today2.txt 3 > data04SVM.txt

featureSelection4SVM.py
python featureSelection4SVM.py data04SVM.txt 0 data04SVM_ori.txt > all_indices_C2_train.txt
python featureSelection4SVM.py data04SVM.txt 1 data04SVM_ori.txt > trainingdata.txt
python featureSelection4SVM.py data04SVM.txt 0 data04SVM_ori.txt > testdata.txt


- noteExtractorC2.py : extraction of notes from annotated xml files.
- dataGeneratorV3C2.py : generation of the primary data from annotated xml files.
- puncOrganizer.py : reorganization of the primary data generated with previous code.
- extractor4SVM.py : extraction of useful data for SVM learning.
- featureSelection4SVM.py : data arragement and feature selection for learning and test data.





Finally the training and test sets are extracted.

"""

import sys
import os
import subprocess



def run(codedirname, dirname, indicator) :
 
	process = subprocess.Popen('ls '+dirname+' > tmp.txt', shell=True, stdout=subprocess.PIPE)
	process.wait()
	
	print 'Start extracting note data from xml files...'
	command = 'python '+str(codedirname)+'noteExtractorC2.py '+dirname+' tmp.txt > tmp_allNotes.xml'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'end of note extraction.\n'
	
	fout = open("tmp_notefile", "w")
	fout.write('tmp_allNotes.xml\n')
	fout.close()
	
	
	
	print 'Start generating the primary data from note data...'
	command = 'python '+str(codedirname)+'dataGeneratorC2.py ./ tmp_notefile > tmp_result.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'end of generation.\n'
	
	
	print 'Start reorganizing the primary data...'
	command = 'python '+str(codedirname)+'puncOrganizer.py tmp_result.txt > tmp_result2.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'end of reorganization.\n'
	
	print 'Start printing all data with labels...'
	command = 'python '+str(codedirname)+'extractor4SVM.py tmp_result2.txt 2 > data04SVM_ori.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	command = 'python '+str(codedirname)+'extractor4SVM.py tmp_result2.txt 3 > data04SVM.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'end of printing'
	
	
	if indicator != 2 :
		var = raw_input('If you want to generate a new list of training/test data indicator file, enter y. If not, just enter : ')
	
		command = ''
		if len(var) > 0 :
			command = 'python '+str(codedirname)+'featureSelection4SVM.py data04SVM.txt 100 data04SVM_ori.txt > all_indices_C2_train.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			print 'training indices are regenerated.\n'
		
	if indicator == 10 :
		command = 'python '+str(codedirname)+'featureSelection4SVM.py data04SVM.txt 1 data04SVM_ori.txt > trainingdata.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+str(codedirname)+'featureSelection4SVM.py data04SVM.txt 0 data04SVM_ori.txt > testdata.txt'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	else :
		if indicator == 1 :
			command = 'python '+str(codedirname)+'featureSelection4SVM.py data04SVM.txt 1 data04SVM_ori.txt > trainingdata.txt'
		elif indicator == 0 :
			command = 'python '+str(codedirname)+'featureSelection4SVM.py data04SVM.txt 0 data04SVM_ori.txt > testdata.txt'
		elif indicator == 2 :
			command = 'python '+str(codedirname)+'featureSelection4SVM.py data04SVM.txt 2 data04SVM_ori.txt > newdata.txt'
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
	print 'end of extraction.'
	
		
	process = subprocess.Popen('rm tmp.txt tmp_notefile ', shell=True, stdout=subprocess.PIPE)
	#process = subprocess.Popen('rm tmp.txt tmp_result.txt tmp_result2.txt', shell=True, stdout=subprocess.PIPE)
	process.wait()
	
	return



def main() :

	if len(sys.argv) != 4 :
		print '** Extraction of training/test data files for SVM from the annotated xml files **'
		print 'python preparerSVM.py (dirname including codes) (dirname including xml files) (1:training, 0:test, 10:both, 2:new data)'
		sys.exit(1)
		
	codedirname = str(sys.argv[1])
	dirname = str(sys.argv[2])
	indicator = int(sys.argv[3])
		
	run(codedirname, dirname, indicator)


if __name__ == '__main__':
	main()
