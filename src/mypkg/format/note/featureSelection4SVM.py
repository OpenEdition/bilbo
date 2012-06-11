#!/usr/bin/env python
# encoding: utf-8
"""
featureSelection4SVM.py

Created by Young-Min Kim on 2011-08-16.

After extracting useful data with extractor4SVM, we arrage data and select features.

"""


import sys
import os
import re
import string
import random

from mypkg.ressources.BeautifulSoup import *

tokens = []		# tokens[k] : TOKEN STRING with token id 'k'
idf = []		# idf[k] : documnet frequency of token id 'k'
features = []	# features[k] : FEATURE STRING with feature id 'k'
doc_tokens = {'0000':0}		# tmp document represented by token strings and thier counts
doc_features = {'0000':0}	# tmp document represented by feature strings and thier counts

valid_features = {'nopunc':0, 'onepunc':0, 'nonumbers':0, 'noinitial':0, 'startinitial':0, 'posspage':0, 'weblink':0, 'posseditor':0, 'italic':0}
#valid_features = {'posspage':0, 'weblink':0, 'posseditor':0}

# extract the number of documents separated with blocks
def extNumDocs (filename) :
	i = 0
	for line in open (filename, 'r') :
		line = string.split(line)
		if len(line) != 0 :
			pass
		else :
			i += 1
	return i

# generate the indicators for the training and test documents
def randomgen(numb) :
	
	numbers = range(numb)
	for i in range(numb) :
		numbers[i] = i+1
	random.shuffle(numbers)
	
	# count of training data 
	num_train = int(numb*0.7) #for example, int(716*0.7) = 501
	index_train = numbers[0:num_train]
	index_test = numbers[num_train:numb]
	
	index_train.sort()
	index_test.sort()
	
	indices = range(numb)
	for i in range(numb) :
		indices[i] = 0
	
	for c in index_train :
		indices[int(c-1)] = 1
	
	# a line corresponds to a document 
	# printed value is 1 : training data
	# printed value is 0 : test data
	for c in indices :
		print c
	
	return
	
#extract training and test data
def selector (filename, ndocs, tr, filename_ori, file_out) :
	
	i = 0
	indices = range(ndocs)
	flagEndRef = 0
	
	if tr != 2 :
		for i in range(len(indices)) :
			indices[i] = 1
		'''for line in open("./all_indices_C2_train.txt", 'r') :
			indices[i] = int(line.split()[0])
			i += 1'''
	else : ###### when extracting new data,  
		for i in range(len(indices)) :
			indices[i] = 2
	
	token_data = []		# TOTAL DATA for tokens, token_data[i] = i_th document DICT containing token ids and token counts
	feature_data = []	# TOTAL DATA for features, feature_data[i] = i_th document DICT containing feature ids and feature counts
	bibls = range(int(ndocs*1.0))
	
	i = 0
	start = 0

	for line in open (filename, 'r') :
		line = line.split()
		
		
		if len(line) != 0:
			
			if line[0] == '1' or line[0] == '-1' : #input tokens
				fill_data(line[1:], tokens, token_data)
				bibls[i] = line[0]
				
			else :	# local features
				flagEndRef += 1
				fill_data(line, features, feature_data)
				pass

		else : # end of a block, a note		
			if flagEndRef == 1:
				i += 1
				flagEndRef = 0
			else:
				features.append({})
				feature_data.append({})
				#fill_data(line, features, feature_data)
				flagEndRef += 1
	
	insert_lineFeatures(feature_data)
	print_output(token_data, feature_data, bibls, tr, indices, file_out)
	load_original(filename_ori, indices)
	
	return


def fill_data(line, input, data) : # line[1:], tokens, token_data / line, features, feature_data

	doc_tokens.clear()
	for n in line :
		#attribute token id, compute the base of idf
		if input.count(n.lower()) == 0 :
			input.append(n.lower())
			#idf.append(1)
			doc_tokens[n.lower()] = 1
		else :
			id = input.index(n.lower())
			if not doc_tokens.has_key(n.lower()) :
				#idf[id] += 1
				doc_tokens[n.lower()] = 1
			else :
				doc_tokens[n.lower()] += 1
				
	data.append([])
	data[len(data)-1] = {-1:-1}
	for key in doc_tokens.keys() :
		id = input.index(key)
		data[len(data)-1][id] = doc_tokens[key]
	del data[len(data)-1][-1]
	
	return


#insert new FEATURES related with total text characters / NOPUNC, ONEPUNC, NONUMBERS, NOINITIAL, 
def insert_lineFeatures(feature_data) :

	#existing features = ['allcap', 'initial', 'startinitial', 'firstcap', 'allsmall',
	#					  'punc', 'nonimpcap', 'italic', 'allnumbers', 'posspage',
	#					  'numbers', 'dash', 'posseditor', 'weblink']

	#extended featues
	features.extend(['nopunc', 'onepunc', 'nonumbers', 'noinitial'])
	
	
	for i in range(len(feature_data)) :
		new_features = [] # list for newly added features for the corresponding document
		
		#puncutation marks check
		id = features.index('punc')
		if id in feature_data[i] :
			puncnt = feature_data[i][id]
			if puncnt == 1 : new_features.append('onepunc')
		else : 
			puncnt == 0
			new_features.append('nopunc')

		try:
			#'numbers', 'allnumbers', 'initial' check 
			if not feature_data[i].has_key(features.index('numbers')) and not feature_data[i].has_key(features.index('allnumbers')) :
				new_features.append('nonumbers')
			if not feature_data[i].has_key(features.index('initial')) : 
				new_features.append('noinitial')

		
			#we can also append some important featues to the new_features list for weighting them 
			new_features.append('startinitial')
			
			#now update features representation of the document with previously found features
			for nf in new_features :
				id = features.index(nf)
				feature_data[i][id] = 1#*len(feature_data[i]) # !!!!!!! VALIDE CONSIDERATION OF VECTOR SIZE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
		except ValueError:
			pass
		#if indices[i] == tr : print feature_data[i]
		


def print_output(token_data, feature_data, bibls, tr, indices, fileOut) :
	fich = codecs.open(fileOut, "w", encoding="utf-8")
	
	i = 0
	adding = adding_fId(len(tokens), feature_data)
	#adding = len(tokens) + 1
	
	for i in range(len(token_data)) :
		keylist = token_data[i].keys()
		keylist.sort()
		
		if indices[i] == tr :
			fich.write( bibls[i]+" ")

		for key in keylist:
			if indices[i] == tr :
				fich.write( str(key+1)+':'+str(token_data[i][key])+" ")
		
		if len(feature_data) > 0 :
			keylist = feature_data[i].keys()
			keylist.sort()
			for key in keylist:
				if indices[i] == tr :
				##################
					if valid_features.has_key(features[key]) :
						#print str(key+adding+1)+':'+str(feature_data[i][key]),
						fich.write( str(key+adding+1)+':1'+" ")
		
		if indices[i] == tr :
			fich.write("\n")

	return
	

#for the counting of input tokens
def adding_fId(tokens_len, feature_data) :
	
	i = 10
	while i < tokens_len :
		i = i*10
		
	return i

#create files having original text form for the varification
def load_original(filename_ori, indices) :
	flagEndRef = 0
	fouttr = open("Result/original_train.txt", "w")
	fouttst = open("Result/original_test.txt", "w")
	
	i = 0
	j=0
	for line in open(filename_ori, 'r') :
		if len(line.split()) != 0 :
			if indices[i] == 1 :
				if j == 0 : fouttr.write(line.split('\n')[0])
				else : fouttr.write(line)
			else :
				flagEndRef += 1
				if j == 0 : fouttst.write(line.split('\n')[0])
				else : fouttst.write(line)
			j += 1
		else : 
			if flagEndRef == 1:
				i += 1
				j=0
			else:
				flagEndRef = 0
	
	fouttr.close()
	fouttst.close()

	return
	

#save input(token) id list and feature id list for new data
def save_ID() :

	f = open('./inputID.txt', 'w')
	for k in tokens :
		f.write(str(k))
		f.write('\n')
	f.close()
	
	f = open('./featureID.txt', 'w')
	for k in features :
		f.write(str(k))
		f.write('\n')
	f.close()
	
	return
	

#load input(token) id list and feature id list for new data
def load_ID() :

	#load input(token) id list for new data
	del tokens[:]
	for line in open('./inputID.txt', 'r') :
		n = line.split('\n')
		tokens.append(n[0])
		
	#load feature id list for new data
	del features[:]
	for line in open('./featureID.txt', 'r') :
		n = line.split('\n')
		features.append(n[0])
	
	return



def main() :

	if len (sys.argv) != 4 :
		print 'python featureSelection4SVM.py (source data filename) (indicator for training or test; 1:training, 0:test, 2:new data, 100:train_indices.txt generation) (original data filename)'
		sys.exit (1)
	
	ndocs = extNumDocs (str(sys.argv[1]))
	if int(sys.argv[2]) > 2 :
		randomgen(ndocs)	#if "all_indices_C2_train.txt" is not prepared, run this function	
	else :
		if int(sys.argv[2]) == 2 : load_ID()
		selector(str(sys.argv[1]), ndocs, int(sys.argv[2]), str(sys.argv[3]))
		if int(sys.argv[2]) != 2 : save_ID()

if __name__ == '__main__':
	main()
	
	

