#!/usr/bin/env python
# encoding: utf-8
"""
imputation.py

Created by Young-Min Kim on 2012-01-22.

Insert proper noun features to tokens estimated positive by a SVM classifier. 

"""
import sys
import os
import string
import re
import subprocess

sys.path.append("/Users/young-minkim/Applications/svm_light")
sys.path.append("/Users/young-minkim/Project/Codes/ProcessingCorpus1")

svm_path = "/Users/young-minkim/Applications/svm_light/"
code_path = "/Users/young-minkim/Project/Codes/ProcessingCorpus1/"
data_path = "/Users/young-minkim/Project/Data/Corpus1/XML_annotated2/"

targetfeaturenames = ['SURNAMELIST', 'FORENAMELIST', 'PLACELIST']

from extractor import *
from digitalizer import *



#insert proper noun features to the classified token
def insertfeature(orifile, resultfile, featurename, tr, io_path) :

	oridata = []
	resultdata = []
	targetlist = []
	
	#estimation result
	for line in open(resultfile, 'r') :
		resultdata.append(line.split('\n')[0])
		
	#list containing valid target tokens for imputation
	tmpfile = ''
	if tr == 1 : tmpfile = io_path+'/targetListTR.txt'
	else : tmpfile = io_path+'/targetListTST.txt'
	for line in open(tmpfile, 'r') :
		targetlist.append(line.split()[0])
	
	#tmp output file	
	f = open('tmp_output', 'w')
	
	i = 0
	j = 0
	
	#original sequence data file to be modified
	for line in open(io_path+orifile, 'r') :
		line = line.split('\n')[0]
		newline = ''
		if int(targetlist[i]) > 0 :
			if float(resultdata[j]) > 0 :
				tmpline = line.split()
				ck = 1
				for tfn in targetfeaturenames :  
					if tfn in tmpline :
						ck = 0
				if ck == 1 :	#if not 'FORENAMELIST' in tmpline and not 'SURNAMELIST' in tmpline and not 'PLACELIST' in tmpline:
					if tr == 1 or tr == -1 :
						for l in tmpline[:len(tmpline)-1] :
							newline = newline+l+' '
						newline = newline+featurename+' '+tmpline[len(tmpline)-1]
					elif tr == 0 or tr == 2 :
						for l in tmpline :
							newline = newline+l+' '
						newline = newline+featurename
				else :
					newline = line
			else : newline = line
			#print line,'+++++', newline, float(resultdata[j])
			print newline
			f.write(newline)
			f.write('\n')
			j += 1
		elif len(line) > 0 :
			print line
			f.write(line)
			f.write('\n')
		else :
			#print 'eor'
			print
			f.write('\n')
		i+= 1
	
	f.close()
	tmp_orifile = orifile
	if orifile.find('tmplist') < 0 : tmp_orifile = re.sub('_CRF', '_CRF_tmplist', orifile)
	process = subprocess.Popen('cp tmp_output '+io_path+tmp_orifile, shell=True, stdout=subprocess.PIPE)
	process.wait()
	return


#call other excutable programs from the data extraction to imputation
def run(io_path, features, orifile, tr) :
	
	#-------------------------------------
	#rich data extraction (if don't exist)
	#-------------------------------------
	var = raw_input('If you want to extract rich training/test data, enter y. If they alreay exist, just enter : ')
	if len(var) > 0 and var == 'y' :
		command = 'python preparerCRF.py '+code_path+' '+data_path+' 20' # extract all data (training/test - normal/rich) 
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	else : pass
	
	
	#-------------------------------------------------------	
	#convert rich data to digital data, call digitalizer.py
	#since digitConvert distinguishes only train/test, when tr=-1 or 2, should be modified as 0 
	#-------------------------------------------------------
	richfile = re.sub('_CRF', '_rich_CRF', orifile)
	#When test data without label (tr=0), we should enter that with label to get an exact svm test file.
	if tr == 0 : richfile = re.sub('_CRF', 'withlabel_rich_CRF', orifile) 
	
	trr = tr
	if tr == -1 or tr == 2: trr = 0 
	digitConvert(features, io_path+richfile, trr, io_path)
	print 'End of converting data'
	
	#-------------------------------
	#svm learning, when tr = 1 only
	#-------------------------------
	if tr == 1 :
		features_array = features.split()
		for f in features_array :
			svm_learning(io_path, f)
			
	#-------------------------------
	#svm classifying, for all cases
	#-------------------------------
	features_array = features.split()
	tmp_orifile = orifile
	for f in features_array :
		svm_classifying(io_path, f, tr)
		featurename = f+'list'
		featurename = featurename.upper()+'2'
		#imputation
		insertfeature(tmp_orifile, 'svm_predictions', featurename, tr, io_path)
		tmp_orifile = re.sub('_CRF', '_CRF_tmplist', orifile)
	
	
def svm_learning(io_path, feature) :
	command = svm_path+'svm_learn '+io_path+'trainsvmdata_'+feature+'.txt '+io_path+'svm_'+feature+'_model'
	print command
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	
	
def svm_classifying(io_path, feature, tr) :
	command = ''
	if tr == 1 :
		command = svm_path+'svm_classify '+io_path+'/trainsvmdata_'+feature+'.txt '+io_path+'svm_'+feature+'_model'
	elif tr == 0 or tr == -1 or tr == 2 :
		command = svm_path+'svm_classify '+io_path+'/testsvmdata_'+feature+'.txt '+io_path+'svm_'+feature+'_model'
	
	print command
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	


def main() :

	if len (sys.argv) != 5 :
		print 'python imputation.py (feature(s) to insert wrapped by '') (io dirname) (original data filename w/o path)  (train:1, test:0, test with label:-1, new:2)'
		sys.exit (1)
	
	features = str(sys.argv[1])
	io_path = str(sys.argv[2]) 
	orifile = str(sys.argv[3])
	tr = int(sys.argv[4])
	
	
	#featurename = str(sys.argv[1]).upper()+'2'
	#insertfeature(orifile, resultfile, featurename, tr)
	
	run(io_path, features, orifile, tr)
	

if __name__ == '__main__':
	main()
	
	

