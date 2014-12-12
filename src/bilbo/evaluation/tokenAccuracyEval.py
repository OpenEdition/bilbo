#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
tokenAccuracyEval.py

Created by Young-Min Kim on 2011-05-27.
Modified for the excluded labels on 2011-02-13

Evaluate the accuracies of all the predicted labels
and each type of labels

"""

import sys
if __name__ == '__main__':
	sys.path.append('src/')
import os
import string
from codecs import open

class TokenAccuracyEval():
	
	@staticmethod
	def evaluate(srcfile, dsrfile):
		returnLabels = []
		returnValues = []
		
		excluded = {'nonbibl': 0, 'c':0} #label exclue sauf pour le calcul de la micro
		cnt = {'0000': 0, 'c':0}# nombre de token étiqueté par label dans le test (ce que l'on souhaite avoir)
		acc = {'0000': 0, 'c':0} # nombre d'étiquette correct par label
		cnt_d = {'0000': 0, 'c':0}# nombre de token étiqueté par label dans la référence (ce qu'il faut avoir)
		errors = {'0000':{'000':0}} #{desired:{predicted:count}}
		tab_precision = []
		tab_recall = []
		tab_mainElmt_precision = []
		tab_mainElmt_recall = []
		
		evaluation = ''

		src = []
		i = 0
		for line in srcfile.split("\n"):
			line = string.split(line)
			if len(line) != 0 :
				currstr = line[0]
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
		for line in dsrfile.split("\n"):
			line = string.split(line)
			if len(line) != 0 :
				currstr = line[0]
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

		evaluation += 'Total accuracy (Micro Averaged Precision)\n'
		evaluation += '# {:d} {:d} {:f}'.format(c, j, float(c)/float(j)*100) + "\n"
		
		for key in excluded.keys() :
			if cnt_d.has_key(key) :
				evaluation += '\n- {:s}'.format(key) + "\n"
				#c-acc[key] est le nombre d'étiquette prédite moins le nombre d'étiquette correct prédite pour le label exclu divisé par le nombre d'étiquette moins le nombre d'étiquette exclue
				apr = float(c - acc[key])/float(j - cnt[key])*100 
				returnLabels.append('avg Micro Precision');
				returnValues.append(apr)
				evaluation += '(Averaged micro Precision) exclu {:s} {:f} {: >4d} {: >4d}'.format(key, apr, (c - acc[key]), (j - cnt[key]))  + "\n"

				are = float(c - acc[key])/float(j - cnt_d[key])*100
				returnLabels.append('avg Micro Recall')
				returnValues.append(are)
				evaluation += '(Averaged micro Recall)          {:s} {:f} {: >4d} {: >4d}'.format(key, are, (c - acc[key]), (j - cnt_d[key])) + "\n"
			
				mfm = 2*apr*are/(apr+are)
				returnLabels.append('micro F-measure')
				returnValues.append(mfm)
				evaluation += '(micro F-measure) exclu          {:s} {:f}'.format(key, mfm) + "\n"

		evaluation += '\n***** Precision *****\n'
		
		for key, value in sorted(cnt_d.iteritems(), key=lambda (k,v): (v,k), reverse=True):
			if acc.has_key(key) and cnt[key]>0 :
				result_key = float(acc[key])/float(cnt[key])*100
				tab_precision.append(result_key)
				evaluation += "{: <15s} {: >3d} {: >3d} {: >10f}".format(key, acc[key], cnt[key], result_key) + "\n"
			'''
			if key == 'title':
				tab_mainElmt_precision.append(float(acc[key])/float(cnt[key])*100)
			if key == 'surname':
				tab_mainElmt_precision.append(float(acc[key])/float(cnt[key])*100)
			if key == 'forename':
				tab_mainElmt_precision.append(float(acc[key])/float(cnt[key])*100)
			'''
		
		#print '\n***** Precision *****'
		#for k in acc.keys() :
		#	print k, acc[k], cnt[k], float(acc[k])/float(cnt[k])*100
		
		evaluation += '\n***** Recall *****\n'
		for key, value in sorted(cnt_d.iteritems(), key=lambda (k,v): (v,k), reverse=True):
			if acc.has_key(key) and cnt[key]>0 :
				result_key = float(acc[key])/float(value)*100
				tab_recall.append(result_key)
				evaluation += "{: <15s} {: >3d} {: >3d} {: >10f}".format(key, acc[key], value, result_key) + "\n"
			else :
				evaluation += "{: <15s} {: >3d} {: >3d} {: >10f}".format(key, 0, cnt_d[key], 0.0) + "\n"
			'''
			if key == 'title':
				tab_mainElmt_recall.append(float(acc[key])/float(value)*100)
			if key == 'surname':
				tab_mainElmt_recall.append(float(acc[key])/float(value)*100)
			if key == 'forename':
				tab_mainElmt_recall.append(float(acc[key])/float(value)*100)
			'''
		evaluation += "\n"
		
		#print '\n***** Recall *****'
		#for k in cnt_d.keys() :
		#	if acc.has_key(k) :
		#		print k, acc[k], cnt_d[k], float(acc[k])/float(cnt_d[k])*100
		#	else :
		#		print k, 0, cnt_d[k], 0.0
		#print

		evaluation += '\n***** Macro Precision/Recall *****\n'
		
		macro_precision = sum(tab_precision)/len(tab_precision)
		returnLabels.append('Macro Precision all');
		returnValues.append(macro_precision)
		evaluation += '(macro precision all elements)   {:f}'.format(macro_precision) + "\n"
		
		macro_recall = sum(tab_recall)/len(tab_recall)
		returnLabels.append('Macro Rappel all');
		returnValues.append(macro_recall)
		evaluation += '(macro rappel all elements)      {:f}'.format(macro_recall) + "\n"
		
		macro_fmesure = (2*(macro_precision*macro_recall))/(macro_precision+macro_recall)
		returnLabels.append('Macro F-mesure all');
		returnValues.append(macro_fmesure)
		evaluation += '(macro F-mesure all elements)    {:f}'.format(macro_fmesure) + "\n\n"
		'''
		macro_precision_mainElmt = sum(tab_mainElmt_precision)/len(tab_mainElmt_precision)
		returnLabels.append('Macro Precision of 3');
		returnValues.append(macro_precision_mainElmt)
		evaluation += '(macro precision three elements) {:f}'.format(macro_precision_mainElmt) + "\n"
		
		macro_recall_mainElmt =	sum(tab_mainElmt_recall)/len(tab_mainElmt_recall)
		returnLabels.append('Macro Rappel of 3');
		returnValues.append(macro_recall_mainElmt)
		evaluation += '(macro rappel three elements)    {:f}'.format(macro_recall_mainElmt) + "\n"
		
		macro_fmesure_mainElmt = (2*(macro_precision_mainElmt*macro_recall_mainElmt))/(macro_precision_mainElmt+macro_recall_mainElmt)
		returnLabels.append('Macro F-mesure of 3');
		returnValues.append(macro_fmesure_mainElmt)
		evaluation += '(macro F-mesure three elements)  {:f}'.format(macro_fmesure_mainElmt) + "\n\n"
		'''
		tes = 0
		bes = 0
		ts = 0
		bs = 0
		for target, value in sorted(errors.iteritems(), key=lambda (k,v): (v,k), reverse=True):
			if target != '0000' :
				del errors[target]['000']
				evaluation += "{: <10s}".format(target)
				if acc.has_key(target):
					evaluation += " {: >3d}\t".format(cnt_d[target] - acc[target])
				else:
					evaluation += " {: >3d}\t".format(cnt_d[target])
				s=0
				for k in sorted(value, key=value.get,reverse=True) :
					evaluation += " {:s} {:d}".format(k, value[k])
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
				if s > 0:
					evaluation += ' *obvious error : {:d}'.format(s)
				evaluation += "\n" 
		evaluation += '*Total obvious errors : title: {: >3d} - biblscope: {: >3d}\n'.format(tes, bes)
		evaluation += '*Total errors         : title: {: >3d} - biblscope: {: >3d}\n'.format(ts, bs)
		
		return evaluation, returnLabels, returnValues


if __name__ == '__main__':
	if len (sys.argv) != 3 :
		print 'python tokenAccuracyEval.py (file to be evaluated) (correct label file)'
		sys.exit (1)
	
	def getfile(fileName):
		with open(fileName, 'r', encoding='utf-8') as content_file:
			content = content_file.read()
		return content

	annotated = getfile(str(sys.argv[1]))
	desired = getfile(str(sys.argv[2]))
	
	evaluation = TokenAccuracyEval.evaluate(annotated, desired)
	print evaluation.encode('utf-8'),
