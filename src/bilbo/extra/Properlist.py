# -*- coding: utf-8 -*-
"""
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
"""
import unicodedata

class Properlist(object):

	def __init__(self, fname, nameFeature):

		self.targetfeature = nameFeature
		self.properlist = {'0000': 0} #other proper nouns than person names considering whitespaces
		self.m_properlist = {'0000': {'0000': 0}}
	
		self.targetlist = self.properlist
		self.m_targetlist = self.m_properlist
		
		for line in open (fname, 'r') :
			line = line.split('\n')
			line = line[0].split('(')
			line = line[0].split(',')
			line = line[0].split('\t')
			
			st = ''
			for l in line[0].split() :
				st = st+l[0].upper()+l[1:len(l)].lower()+' '
			st = st[:len(st)-1]
			key = st.split()[0]
			
			if key == st :
				self.targetlist[key] = 1
			else :
				if not self.m_targetlist.has_key(key) :
					self.m_targetlist[key] = {st:1}
				else :
					self.m_targetlist[key][st] = 1


	def searchProper(self, listReference, tr) :
		"""
		Add the target feature if the corresponding word is in the list according to the rules
		"""
		
		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
		
		self.targetlist = self.properlist
		self.m_targetlist = self.m_properlist		
		
		for reference in listReference.getReferences():
			cpt = 0
			for mot in reference.getWord():
				
				token = mot.nom
				token0 = token
				token2 = token[0]+ token[1:len(token)].lower()
				
				if token != token2 : token = token2
				
				if self.targetlist.has_key(token) :
					mot.addFeature(self.targetfeature)

				if self.m_targetlist.has_key(token) :
					full_str = ''
					for j in range(cpt,reference.nbWord()) :
						try:
							full_str = full_str + reference.getWordIndice(j).nom + ' '
						except UnicodeDecodeError:
							pass
					
					tokens = ''
					full_str = full_str.title()
					full_str = self.strip_accents(full_str)
					for key in sorted(self.m_targetlist[token], key=len, reverse=True):
						try:
							if full_str.find(key) >= 0 :
								tokens = key
						except UnicodeDecodeError:
							pass
						
					if len(tokens) > 0:
						tokens = tokens.split() 
						for j in range(cpt,cpt+len(tokens)) :
							curr = reference.getWordIndice(j)
							if (tokens[j-cpt]).title() == (self.strip_accents(curr.nom)).title() :
								curr.addFeature(self.targetfeature)
								#print "found", self.targetfeature
				cpt += 1


	def strip_accents(self, input_str):
		nkfd_form = unicodedata.normalize('NFKD', unicode(input_str, 'utf8'))
		return (u"".join([c for c in nkfd_form if not unicodedata.combining(c)])).title()

