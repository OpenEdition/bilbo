# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
"""

class Balise(object):
	"""
	classdocs
	"""


	def __init__(self, nom):
		"""
		Constructor
		"""
		self.nom = nom
		
	def affiche(self):
		print "\t\t", self.nom.encode('utf8')
		

	def nameIs(self, nom):
		"""
		Check the tag name
		"""
		if nom == self.nom:
			return 1
		return -1
	
	