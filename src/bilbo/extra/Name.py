# -*- coding: utf-8 -*-
"""
Created on 25 avr. 2012

@author: Young-min Kim, Jade Tavernier
"""
import re
import string

class Name(object):

	def __init__(self, fname):
		"""
		variables
		"""
		self.namelist = {'0000': {'000': 0}}
		self.multi_namelist = {'0000': {'0000': 0}} #when surname is more than a word
		self.forenamelist = {'0000': 0}
		
		'Load the name list file and save the contents in the lists'
		for line in open (fname, 'r') :
			line = re.sub(' ', ' ', line)
			line = string.replace(line, '-','-')
			#line = string.replace(nline, '.','')
			line = line.split('/')
			fname = line[0].split()
			sname = line[1].split()
			f_st = ''
			if len(fname) > 0 :
				for n in fname : f_st = f_st+n+' '
				f_st = f_st[:len(f_st)-1]	
		
			s_st = ''
			if len(sname) > 0 :
				for n in sname : s_st = s_st+n+' '
				s_st = s_st[:len(s_st)-1]
				
			if self.namelist.has_key(s_st) :
				self.namelist[s_st][f_st] = 1
			else :
				self.namelist[s_st] = {f_st:1}
			
			if len(s_st.split()) > 1 :
				start_sname = s_st.split()[0]
				if self.multi_namelist.has_key(start_sname) :
					self.multi_namelist[start_sname][s_st] = 1
				else :
					self.multi_namelist[start_sname] = {s_st:1}
				
			self.forenamelist[f_st] = 1
			

	def searchName(self, listReference, tr) :
		"""
		Add SURNAMELIST and FORENAMELIST features according to the rules
		"""
	
		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
			
		cpt = 0
		for reference in listReference.getReferences():
			cpt = 0
			for mot in reference.getWord():

				first = mot.nom
				first0 = first
				first2 = first[0]+ first[1:len(first)].lower()
				
				if not self.namelist.has_key(first) :
					if self.namelist.has_key(first2) :
						first = first2
						
				if self.namelist.has_key(first) : # current token is surname
					####### At first, check the cases of [surname , forename] or [surname forename]
					j=cpt+1
					if reference.nbWord() > cpt+1 :
						if reference.getWordIndice(cpt+1).nom != ',' : ####### Modification : instead of 'c' in label, check ',' ### 2012-01-22 ###
							j = cpt+1 # second token id
						else : 
							j = cpt+2	# second token id
					
					if reference.nbWord() > j and ( self.forenamelist.has_key(reference.getWordIndice(j).nom) or  self._has_initial(reference.getWordIndice(j)) == 1): # second token is forename
							#insert NAMELIST in the feature part of the list
							### B. separation between SURNAMELIST and FORENAMELIST
							mot.addFeature('SURNAMELIST')
							motSuivant = reference.getWordIndice(j)
							motSuivant.addFeature('FORENAMELIST')

					###### if the first cases don't work, check the case of [forname surname]
					if cpt > 0 :
						j = cpt-1
						if self.forenamelist.has_key(reference.getWordIndice(j).nom) or  self._has_initial(reference.getWordIndice(j)) == 1 :
							### B. separation between SURNAMELIST and FORENAMELIST
							mot.addFeature('SURNAMELIST')
							motSuivant = reference.getWordIndice(j)
							motSuivant.addFeature('FORENAMELIST')

				cpt += 1
		

	def _has_initial(self, mot) :
		"""
		Check if the word has initial
		"""		
		ck = 0
		feature = mot.getAllFeature()
		for t in feature :
			if t.nom.upper() == 'INITIAL' :
				ck = 1
		return ck
