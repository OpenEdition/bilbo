# -*- coding: utf-8 -*-
"""
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
"""

class ListReferences(object):
	"""
	A class containing a list of reference objects and corpus type information. 
	"""


	def __init__(self, references, typeCorpus):
		"""
		Constructor
		"""
		self.listReferences = references
		self.typeCorpus = typeCorpus


	def affiche(self):
		"""
		Show the reference information : words, tags, features
		"""
		for key in self.listReferences:
			key.affiche()
			
			
	def nbReference(self):
		"""
		Return the number of references in the list
		"""
		return len(self.listReferences)
	

	def modifyTestIndice(self, numRef):
		"""
		Modify the value of an indicator, which tells if a reference is training data or test data
		Set all the value of all the references as test
		"""
		for ref in self.listReferences:
			ref.modifyIsTest()
		

	def modifyTrainIndice(self, numRef):
		"""
		Modify the value of an indicator, which tells if a reference is training data or test data
		Set the value of all the references as train
		"""
		for ref in self.listReferences:
			ref.modifyIsTrain()
		

	def modifyTestIndiceRef(self, numRef):
		"""
		Set the above value as test for a reference
		"""
		self.listReferences[numRef].modifyIsTest()
		

	def modifyTrainIndiceRef(self, numRef):
		"""
		Set the above value as test for a reference
		"""
		self.listReferences[numRef].modifyIsTrain()
		

	def getTrainIndiceRef(self, numRef):
		"""
		Return the above value of a reference given the number of the reference
		"""			
		return self.listReferences[numRef].train
		

	def getReferences(self):
		return self.listReferences
	
	
	def getReferencesIndice(self, indice):
		return self.listReferences[indice]
	
	