#!/usr/bin/env python
# encoding: utf-8
"""
extractor4SVM.py

Created by Young-Min Kim on 2011-08-12.

The first version of extractor4SVM.py
This code provides all types of features on both <bibl> and 
<nonbibl> notes for the svm classification.

In this version, we extract three different types of features.
Type 1 : input tokens
Type 2 : local features
Type 3 : special phrases indicating reference (refSign)
		 special phrases indicating previously cited reference (precitSign)

For the moment, we use 11 local features extracted by extractorV5.py.

----------
2011-10-20



"""


import sys
import os
import re
import string
import random


from mypkg.ressources.BeautifulSoup import BeautifulSoup
from mypkg.ressources.BeautifulSoup import Tag


nonLabels = {'hi':0, 'abbr':1, 'lb':0, 'pb':0, 'ptr':0, 'emph':0}
features = {'initial':0, 'allnumbers':0, 'dash':0, 'numbers':0, 'posspage':0,
			'allcap':0, 'allsmall':0, 'nonimpcap':0, 'firstcap':0, 'weblink':0, 'italic':0, 'posseditor':0}
			#'guillemot_left':0, 'guillemot_right':0, 'quote_left':0, 'quote_right':0}
			#'onedigit':0, 'twodigit':0, 'threedigit':0, 'fourdigit':0}

tokens = []
idf = []
doc_tokens = {'0000':0}



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

	
#extract training and test data
def extractor (filename, ndocs, outtype) :
	
	data_list = []
	all_data = []
	bibls = range(ndocs)
	
	i = 0

	start = 0
	nonbiblck = 1
	relatItm = 0 #realteditem tag indicator
	titleCK = 0  #title tag indicator 
	titleAttr = ''  #previous title attribute	
	for line in open (filename, 'r') :
		line = line.split('++')
		
		
		if len(line[0].split()) != 0 :
			token = line[0].split()[0]
			if token != '********in********' and token != '!NONE!' and token != ' ' :
				#finding labels
				tmp_strs = (line[len(line)-1].split('\n')[0]).split()
				
				# finding just a label which is not in the nonLabels list
				tmp_strs.reverse()
				st = tmp_strs[0]
				j = 1
				if nonLabels.has_key(st) :
					try :
						while nonLabels.has_key(tmp_strs[j]) :
							j += 1
						st = tmp_strs[j]
					except :
						pass
						sw = 0 # if all the labels are one of nonLabels, check if there is abbr and take it as label
						for jj in range(j) :
							if tmp_strs[jj] == 'abbr' :
								sw = 1
						if sw == 1 :
							st = 'abbr'
						else : 
							st = 'nolabel'
							
				#nobibl check, if all tokens are nonbibl, the note is nonbibl
				#also <c> check, if c, punc_ck = 1
				tmp_nonbiblck = 0
				punc_ck = 0
				for tmp in tmp_strs :
					if tmp == 'nonbibl' :
						tmp_nonbiblck = 1
						######### all punc in nonbibl become nonbibl ### 2011-10-20 ###
						#st = 'nonbibl' ##!!!!!##
					if tmp == 'c' :
						punc_ck = 1
						######### all punc in nonbibl become c ### 2011-10-20 ###
						st = 'c' ##!!!!!##
						
								
				#label check
				if st == 'title':
					[st, titleAttr] = extract_title(line[1], relatItm, titleCK, titleAttr)
					if st == 'title' : titleCK = 1
				elif st == 'editor' :
					st = 'name'
				elif st == 'meeting' :
					st = 'booktitle'
				elif st == 'pubplace' or st == 'settlement' or st == 'country' :
					st = 'place'
				elif st == 'sponsor' or st == 'distributor' :
					st = 'publisher'
					
				if st == 'nolabel' and  (token.lower() == 'in' or token.lower() == 'in ' or token.lower() == 'dans' or token.lower() == 'dans ' or token.lower() == 'en' or token.lower() == 'en ') : ######### added dans, en 2011-12-06 ###
					st = 'bookindicator'
					
					
				pun_attr = ''
				#punctuation check
				if punc_ck == 1 :
					pun_attr = 'PUNC '
					
					#if token == '.' : pun_attr = 'POINT '
					#elif token == ',' : pun_attr = 'COMMA '
					#else : pun_attr = 'PUNC '
				
				#check <date> label for newly updated "publicationDate" attribute
				if st == 'biblscope' :
					ck = check_att(line[1], 'publicationDate')
					if ck == 1 :
						st = 'date'
				
				# extract attributes
				attrs = ''
				attrs = extract_attrs(line[1])
				tmp_str = ''
				if len(attrs) > 0 :
					tmp_str = token+' '+attrs
				else :
					tmp_str = token+' '
				
				#fill data_list

				data_str = tmp_str+pun_attr+st
				data_list.append(data_str)

				if tmp_nonbiblck == 0 : nonbiblck = 0
				
				#attribute token id, compute the base of idf
				if tokens.count(token.lower()) == 0 :
					tokens.append(token.lower())
					idf.append(1)
					doc_tokens[token.lower()] = 1
				else :
					id = tokens.index(token.lower())
					if not doc_tokens.has_key(token.lower()) :
						idf[id] += 1
				
			else :
				if token == '********in********' : relatItm = 1

		else : # end of a block, a note
			data_list.append('')
			
			if nonbiblck == 1 :
				bibls[i] = -1
			else : bibls[i] = 1
			
			relatItm = 0
			titleCK = 0
			nonbiblck = 1
			doc_tokens.clear()
			
			i += 1
	
	all_data.append([])
	for data in data_list :
		#print data
		if len(data) != 0 :
			all_data[len(all_data)-1].append(data)
		else : 
			all_data.append([])
	
	all_data = all_data[:len(all_data)-1]
	
	
	############
	## OUTPUT ##
	############
	if outtype == 1 :
		print_alldata(all_data)
	else :
		print_parallel(all_data, bibls, outtype)
	
	return



def extract_attrs(attstr) :
	tmpstr = attstr.split()
	retrnstr = ''
	for att in tmpstr :
		if features.has_key(att) :
			retrnstr = retrnstr + att.upper()+' '	
	return retrnstr


def check_att(attstr, attrname) :
	tmpstr = attstr.split()
	ck = 0
	for att in tmpstr :
		if att == attrname :
			ck = 1	
	return ck


def extract_title(attstr, relatItm, titleCK, titleAttr) :
	tmpstr = attstr.split()
	retrnstr ='title'
	for att in tmpstr :
		if att == 'a' :
			retrnstr = 'title'
			titleAttr = att
		elif att == 'j' or att == 's' : 
			if titleCK == 1 and titleAttr != att : 
				retrnstr = 'booktitle'
			else : 
				retrnstr = 'title'
				titleAttr = att
		elif att == 'm' or att == 'u' :
			if relatItm == 1 and titleCK == 1 :
				retrnstr = 'booktitle'
			else : 
				retrnstr = 'title'
				titleAttr = att
	return retrnstr, titleAttr
	

def print_alldata(all_data) :
	for data in all_data :
		for d in data :
			print d
		print
	return

#printing result in parallel lines
def print_parallel(all_data, bibls, outtype) :
	i = 0
	for data in all_data :
		token_line = ''
		feature_line = ''
		#special_line = ''
		
		k=0
		for d in data :
			d = d.split()
			invalide_token = 0
			for j in range(1,len(d)-1) :
				feature_line = feature_line + d[j] + ' '
				id = tokens.index((d[0]).lower())
				if outtype == 3 and (d[j] == 'ALLNUMBERS' or d[j] == 'NUMBERS' or idf[id] == 1) : invalide_token = 1
				if k == 0 and d[j] == 'INITIAL' : feature_line = feature_line + 'STARTINITIAL '
				
			#if invalide_token == 0 and d[len(d)-1] != 'c' : token_line = token_line + d[0] + ' '
			if invalide_token == 0 : token_line = token_line + d[0] + ' '
			k += 1
		
		#printout BIBL indicator, TOKENS, then in the next line local FEATURES
		#a document is separated as a block
		print bibls[i], token_line
		print feature_line
		print
		i += 1
	
	return

def count_bibls(bibls) :
	count = 0
	for n in bibls :
		count += n
	print len(bibls), count
	return



def main() :

	if len (sys.argv) != 3 :
		print 'python extractor4SVM.py (source data filename) (indicator for output types; 1: all data sequence, 2: all data in parallel, 3: valid tokens in parallel)'
		sys.exit (1)
	
	ndocs = extNumDocs (str(sys.argv[1]))
	extractor(str(sys.argv[1]), ndocs, int(sys.argv[2]))


if __name__ == '__main__':
	main()
	
	

