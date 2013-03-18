# -*- coding: utf-8 -*-
"""
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
"""

class Place(object):

	def __init__(self, fname):
		self.placelist = {'0000': 0}
		
		'Load the place list file and save the contents in the list'
		for line in open (fname, 'r') :
			line = line.split('\n')[0]
			self.placelist[line] = 1
	

	def searchPlace(self, listReference, tr) :
		"""
		Add PLACELIST feature if the corresponding word is in the list
		"""
		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
	
		for reference in listReference.getReferences():
			for mot in reference.getWord():
				if self.placelist.has_key(mot.nom.upper()):
					mot.addFeature('PLACELIST')

		