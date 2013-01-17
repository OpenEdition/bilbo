# -*- coding: utf-8 -*-
'''
Created on 18 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''

class Balise(object):
	'''
	classdocs
	'''


	def __init__(self, nom):
		'''
		Constructor
		'''
		self.nom = nom
		
	def affiche(self):
		print "\t\t",self.nom
		

	def nameIs(self, nom):
		'''
		Check the tag name
		'''
		if nom == self.nom:
			return 1
		return -1
	
	