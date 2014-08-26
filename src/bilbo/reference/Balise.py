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
		print type(self.nom)
		print "\t\t",self.nom
		

	def nameIs(self, nom):
		"""
		Check the tag name
		"""
		print nom + " == " + self.nom
		if nom == self.nom:
			print "oui"
			return 1
		return -1
	
	