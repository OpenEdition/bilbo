#!/usr/bin/env python
# encoding: utf-8
"""
reformatter.py

Created by Young-Min Kim on 2012-02-01.
To test other software than mallet, reformat the data file.

At first, CRF++

"""

import sys

features = [['ALLNUMBERS', 'NUMBERS'],	#1
			['DASH'],					#2
			['ALLCAP', 'ALLSMALL', 'FIRSTCAP', 'NONIMPCAP'],	#3
			['BIBL_START', 'BIBL_IN', 'BIBL_END'],				#4
			['INITIAL'],	#5
			['WEBLINK'],	#6
			['ITALIC'],		#7
			['POSSEDITOR'],	#8
			['SURNAMLIST', 'FORENAMELIST', 'PLACELIST']]	#9
			
			
features2 = ['ALLNUMBERS', 'NUMBERS',	#1 #2
			'DASH',	'ALLCAP',			#3 #4
			'ALLSMALL', 'FIRSTCAP',		#5 #6
			'NONIMPCAP', 'BIBL_START',	#7 #8
			'BIBL_IN', 'BIBL_END',		#9 #10
			'INITIAL', 'WEBLINK',		#11 #12
			'ITALIC', 'POSSEDITOR']		#13 #14
			
			

def formatCRFPP(All_bibls, tr) :

	nAll_bibls = [] 
	ntmp_bibl = []
	
	#print 'formater in'
	for tmp_bibl in All_bibls : 
		ntmp_bibl = []
		for tmp in tmp_bibl : #tmp is temp line in bibl
			tmp_features = ['NONUMBERS', 'NODASH', 'NONIMPCAP', 'NULL', 'NOINITIAL', 'NOWEBLINK', 'NOITALIC', 'NOEDITOR', 'NOLIST']
			for i in range(len(features)) :
				cur_feature = ''
				for j in range(len(features[i])) :
					if tmp[1:].count(features[i][j]) > 0 :
						cur_feature = features[i][j]
				if cur_feature != '' :
					tmp_features[i] = cur_feature
					
			tmp_features.insert(0,tmp[0])
			if tr != 0 : tmp_features.append(tmp[len(tmp)-1])
			ntmp_bibl.append(tmp_features)
			
		nAll_bibls.append(ntmp_bibl)

	return nAll_bibls


### FORMAT, each feature has its own column
def formatAlter(All_bibls, tr) :

	nAll_bibls = [] 
	ntmp_bibl = []
	
	#print 'formater in'
	for tmp_bibl in All_bibls : 
		ntmp_bibl = []
		for tmp in tmp_bibl : #tmp is temp line in bibl
			tmp_features = ['NOALLNUMBERS', 'NONUMBERS', 'NODASH',	'NOALLCAP', 'NOALLSMALL', 'NOFIRSTCAP', 'NONIMPCAP',
							'NOBIBL_START', 'NOBIBL_IN', 'NOBIBL_END', 'NOINITIAL', 'NOWEBLINK', 'NOITALIC', 'NOPOSSEDITOR']
			for i in range(len(features2)) :
				cur_feature = ''
				if tmp[1:].count(features2[i]) > 0 :
						cur_feature = features2[i]
				if cur_feature != '' :
					tmp_features[i] = cur_feature
					
			tmp_features.insert(0,tmp[0])
			if tr != 0 : tmp_features.append(tmp[len(tmp)-1])
			ntmp_bibl.append(tmp_features)
			
		nAll_bibls.append(ntmp_bibl)

	return nAll_bibls
	


def extractLabel(fname) :
	
	for f in open (fname, 'r') :
		f = f.split()
		if len(f) > 0 :
			print f[len(f)-1]
		else : print
		
	return
	

def printingorder(fname) :

	neworder = ['surname', 'forename', 'title', 'booktitle', 'publisher', 'date', 'place', 'biblscope', 'abbr',
				'nolabel', 'edition', 'orgname', 'extent', 'bookindicator', 'namelink', 'genname', 'ref', 'c']
				
	newline_total = ''
	newline_pr = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
	newline_re = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
	
	pr = -1
	for f in open (fname, 'r') :
		ff = f.split()
		
		if len(ff) >0 and ff[0] == '*****' : 
			pr = -1*pr
			
		if pr == 1 and len(ff) > 3 and ff[0] != 'Total' :
			i = neworder.index(str(ff[0])) 
			newline_pr[i] = f
		elif pr == -1 and len(ff) > 3 and ff[0] != 'Total' :
			i = neworder.index(ff[0]) 
			newline_re[i] = f
		elif len(ff) == 3 and ff[0] != '*****' :
			newline_total = f
		
	print 'Total accuracy (Micro Averaged Precision)'
	print newline_total
	
	print '***** Precision *****'
	for line in newline_pr : 
		if line != '' : print line,
	
	print
	print '***** Recall *****'
	for line in newline_re : 
		if line != '' : print line,
	print
	
	return



def main() :

	if len (sys.argv) != 2 :
		print 'python reformatter.py (file name)'
		sys.exit (1)
		
	#extractLabel(str(sys.argv[1]))
	printingorder(str(sys.argv[1]))


if __name__ == '__main__':
	main()

