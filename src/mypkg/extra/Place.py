# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''

class Place(object):

	def __init__(self, fname):
		self.placelist = {'0000': 0}
		
		'''
		load fichier lexique
		'''
		for line in open (fname, 'r') :
			line = line.split('\n')[0]
			self.placelist[line] = 1
	

	
	'''
	searchPlace: 
	listReference objet ListReference
	'''
	def searchPlace(self, listReference, tr) :

		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
	
		for reference in listReference.getReferences():
			for mot in reference.getWord():
				if self.placelist.has_key(mot.nom.upper()):
					mot.addFeature('PLACELIST')
		