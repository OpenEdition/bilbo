'''
Created on 18 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''

class Feature(object):
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
		
	'''
	verifie si le nom est celui passe en parametre
	'''
	def nameIs(self, nom):
		if nom == self.nom:
			return 1
		return -1