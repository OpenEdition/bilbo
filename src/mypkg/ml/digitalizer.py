#!/usr/bin/env python
# encoding: utf-8
"""
digitalizer.py

Created by Young-Min Kim on 2012-01-20.

Convert text data to digital data for imputation with a SVM classifier.
With the converted data, we construct a SVM for each proper noun type,
that classifies tokens into two categories. (positive/negative to have
the proper noun feature). 

We can produce two different files (learning/test(new)).

* When producing LEARNING DATA, an id file is also created to save the 
input id list for test(new) data. 
* When producing TEST(NEW) DATA, the existing input id list is loaded
to match tokens and thier features to specific id. For non-existing 
tokens or features, we ignore them.

At the end, creat a list of valid tokens (1/0) cause there are empty
lines to separate references (for both learning and test data) and some
tokens having only non-existing value and features (for test(new) data)
in the input id list.  

"""


import sys
import os
import string

input = ['000NULL000']		# input_id[k] : INPUT and FEATURE STRING with id 'k'
instances = {'0000':0}		# tmp line instance represented by a token, features and thier counts(existences)
data = []					# digitalized data to be printed
labels = []					# true label of corresponding token


dropFeatList = ['ALLNUMBERS', 'NUMBERS']
dropLabelList = ['c']


def fill_data(line, tr) : 

	if (len(line) > 0) :
		instances.clear()
		for n in line[:len(line)-1] :
			if input.count(n.lower()) == 0 :
				if tr == 1 :
					input.append(n.lower())
					instances[n.lower()] = 1
			else :
				id = input.index(n.lower())
				if not instances.has_key(n.lower()) :
					instances[n.lower()] = 1
				else :
					instances[n.lower()] += 1
		data.append([])
		data[len(data)-1] = {-1:-1}
		for key in instances.keys() :
			id = input.index(key)
			data[len(data)-1][id] = instances[key]
		del data[len(data)-1][-1]
		
		labels.append(line[len(line)-1])
		
	else :
		data.append([])
		labels.append('EOR')
	
	return



def drop() :	# drop several tokens, which are obviously non-proper nouns in advance 

	for i in range(len(data)) :
		dr_ck = 0
		if len(data[i]) > 0 :
			for key in data[i].keys() :
				if input[key].upper() in dropFeatList or labels[i] == 'c' : dr_ck = 1
				
		if dr_ck == 1 :
			data[i].clear()
			data[i] = []


def print_output(tr, targetLabel, ndir) :

	fname = ''
	if tr == 1 :
		fname = ndir+'/trainsvmdata_'+targetLabel+'.txt'
	else :
		fname = ndir+'/testsvmdata_'+targetLabel+'.txt'
	f = open(fname, 'w')
	
	targetCk = range(len(data)) # To filter out zero-lenth data
	
	for i in range(len(data)) :
		if len(data[i]) > 0 :
			if targetLabel == labels[i] :
				f.write('1 ')
				#print '1',
			else :
				f.write('-1 ')
				#print '-1',
			
			keylist = data[i].keys()
			keylist.sort()
			for key in keylist :
				tstr = str(key)+':'+str(data[i][key])+' '	
				f.write(tstr)
				#print str(key)+':'+str(data[i][key]),
			f.write('\n')
			#print
			targetCk[i] = 1
		else : 
			#if labels[i] == 'EOR' :	print labels[i]
			#else :	print 'DROP'
			targetCk[i] = 0
	
	fname = ''
	if tr == 1 : fname = ndir+'/targetListTR.txt'
	else : fname = ndir+'/targetListTST.txt'
	
	f = open(fname, 'w')
	
	for k in targetCk :
		f.write(str(k))
		f.write('\n')
	f.close()
	
	
	return


#save input id list for new data
def save_inputID(ndir) :

	f = open(ndir+'/inputID.txt', 'w')
	for k in input :
		f.write(str(k))
		f.write('\n')
	f.close()

	return

#load input id list for new data
def load_inputID(ndir) :

	del input[:]
	for line in open(ndir+'/inputID.txt', 'r') :
		n = line.split('\n')
		input.append(n[0])
	
	return


#insert proper noun features to the classified token
def reconvert(orifile, resultfile, featurename) :

	oridata = []
	resultdata = []
	
	#estimation result
	for line in open(resultfile, 'r') :
		resultfile.append[line.split('\n')[0]]
	
	i = 0
	#original crf data file to be modified
	for line in open(orifile, 'r') :
		line = line.split('\n')
		newline = ''
		if len(line[0]) > 0 :
			if resultdata[i] > 0 :
				tmpline = line.split()
				if not featurename in tmpline :
					for l in tmpline[:len(tmpline-1)] :
						newline = newline+l+' '
					newline = newline+featurename+' '+tmpline[len(tmpline-1)]
				else :
					newline = line
			else : newline = line
			i += 1
		else : pass
		
		print newline
	
	return


def digitConvert(targetLabel, fname, tr, ndir) :

	if tr != 1 : load_inputID(ndir)
	
	i=1
	for line in open(fname, 'r') :
		line = line.split()
		print '****',i,'****', line
		fill_data(line, tr)
		i+=1
	
	#drop() ############
	targetLabels = targetLabel.split()
	numTargets = len(targetLabels)
	for taget in targetLabels :
		print_output(tr, taget, ndir)
		
	if tr == 1 : save_inputID(ndir)

	return
	



def main() :

	if len (sys.argv) != 5 :
		print 'python digitalizer.py (target labels wrapped by \'\') (source data filename) (train:1, test:0, new:2) (inout dir name)'
		sys.exit (1)
	
	targetLabel = str(sys.argv[1])
	fname = str(sys.argv[2])
	tr = int(sys.argv[3])
	ndir = str(sys.argv[4])
	
	digitConvert(targetLabel, fname, tr, ndir)
	

if __name__ == '__main__':
	main()
	
	

