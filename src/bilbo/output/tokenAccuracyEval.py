#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tokenAccuracyEval.py

Created by Young-Min Kim on 2011-05-27.
Modified for the excluded labels on 2011-02-13

Evaluate the accuracies of all the predicted labels
and each type of labels

"""

import sys
import os
import string

excluded = {'nonbibl': 0, 'c':0} #label exclue sauf pour le calcul de la micro

cnt = {'0000': 0}# nombre de token étiqueté par label dans le test (ce que l'on souhaite avoir)
acc = {'0000': 0} # nombre d'étiquette correct par label
cnt_d = {'0000': 0}# nombre de token étiqueté par label dans la référence (ce qu'il faut avoir)
errors = {'0000':{'000':0}} #{desired:{predicted:count}}

def evaluate(srcfile, dsrfile):
	
	src = []
	i = 0
	for line in open (srcfile, 'r') :
		line = string.split(line)
		if len(line) != 0 :
			currstr = line[len(line)-1]
			src.append(currstr)
			i += 1
			if cnt.has_key(currstr) :
				cnt[currstr] += 1
			else :
				cnt[currstr] = 1
				acc[currstr] = 0
	del cnt['0000']

	j = 0 # nombre total de token étiqueté
	c = 0 #nombre total d'étiquette correct prédite
	for line in open (dsrfile, 'r') :
		line = string.split(line)
		if len(line) != 0 :
			currstr = line[len(line)-1]
			if cnt_d.has_key(currstr) :
				cnt_d[currstr] += 1
			else :
				cnt_d[currstr] = 1			
			if (src[j] == currstr) : #predicted==desired
				c += 1
				acc[currstr] += 1
			else :
				if errors.has_key(currstr) :
					if errors[currstr].has_key(src[j]) :
						errors[currstr][src[j]] += 1
					else :
						errors[currstr][src[j]] = 1
				else :
					errors[currstr] = {'000':0}
					errors[currstr][src[j]] = 1
				
			j += 1
	del acc['0000']
	del cnt_d['0000']
	
	print '\nTotal accuracy (Micro Averaged Precision)'
	print '#', c, j, float(c)/float(j)*100
	
	for key in excluded.keys() :
		if cnt_d.has_key(key) :
			print '\n-',key
			apr = float(c - acc[key])/float(j - cnt[key])*100 #c-acc[key] est le nombre d'étiquette prédite moins le nombre d'étiquette correct prédite pour le label exclu divisé par le nombre d'étiquette moins le nombre d'étiquette exclue
			are = float(c - acc[key])/float(j - cnt_d[key])*100
			print '(Averaged micro Precision) exclu ', key, (c - acc[key]), (j - cnt[key]), apr
			print '(Averaged micro Recall)', key, (c - acc[key]), (j - cnt_d[key]), are
			print '(micro F-measure) exclu ', key, 2*apr*are/(apr+are)
		
	print '\n***** Precision *****'
	
	for key, value in sorted(cnt_d.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		if acc.has_key(key) :
			print key, acc[key], cnt[key], float(acc[key])/float(cnt[key])*100
		
	
	#print '\n***** Precision *****'
	#for k in acc.keys() :
	#	print k, acc[k], cnt[k], float(acc[k])/float(cnt[k])*100
	
	print '\n***** Recall *****'
	for key, value in sorted(cnt_d.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		if acc.has_key(key) :
			print key, acc[key], value, float(acc[key])/float(value)*100
		else :
			print key, 0, cnt_d[key], 0.0
	print
	
	#print '\n***** Recall *****'
	#for k in cnt_d.keys() :
	#	if acc.has_key(k) :
	#		print k, acc[k], cnt_d[k], float(acc[k])/float(cnt_d[k])*100
	#	else :
	#		print k, 0, cnt_d[k], 0.0
	#print
	
	
	tes = 0
	bes = 0
	ts = 0
	bs = 0
	for target, value in sorted(errors.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		if target != '0000' :
			del errors[target]['000']
			print target,'',
			if acc.has_key(target) : print cnt_d[target] - acc[target],'\t',
			else : print cnt_d[target],'',
			s=0
			for k in sorted(value, key=value.get,reverse=True) :
				print k,'',value[k],'',
				if target.find('title') >= 0 :
					ts += value[k]
					if k.find('title') < 0 and k.find('meeting') < 0:
						s += value[k]
						tes += value[k]
				elif target.find('biblscope') >= 0 :
					bs += value[k]
					if k.find('biblscope') < 0 :
						s += value[k]
						bes += value[k]
			if s > 0 : print '*obvious error :', s,
			print 
	print '*Total obvious error :', 'title:',tes, 'biblscope:',bes
	print '*Total error :', 'title:',ts, 'biblscope:',bs
	
	return
	

def main():

	if len (sys.argv) != 3 :
		print 'python tokenAccuracyEval.py (file to be evaluated) (correct label file)'
		sys.exit (1)

	evaluate(str(sys.argv[1]), str(sys.argv[2]))


if __name__ == '__main__':
	main()

