'''
Created on 18 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''

class ListReferences(object):
	'''
	classdocs
	'''


	def __init__(self, references, corpus):
		'''
		Constructor
		'''
		self.listReferences = references
		self.corpus = corpus

	'''
	affiche permet d'afficher le detail des references : mots, balises, caracteristiques
	'''
	def affiche(self):
		for key in self.listReferences:
			key.affiche()
			
	'''
	nbReference retourne le nombre de reference qu'il contient
	'''
	def nbReference(self):
		return len(self.listReferences)
	
	'''
	modifyTestIndiceRef permet d'indiquer que toutes les references sont du test
	'''
	def modifyTestIndice(self, numRef):
		for ref in self.listReferences:
			ref.modifyIsTest()
		
	'''
	modifyTrainIndice permet d'indiquer que toutes les references sont train
	'''
	def modifyTrainIndice(self, numRef):
		for ref in self.listReferences:
			ref.modifyIsTrain()
		
	'''
	modifyTestIndiceRef permet d'indiquer que la reference numRef fait parti du test
	'''
	def modifyTestIndiceRef(self, numRef):
		self.listReferences[numRef].modifyIsTest()
		
	'''
	modifyTrainIndiceRef permet d'indiquer que la reference numRef fait parti du train
	'''
	def modifyTrainIndiceRef(self, numRef):
		self.listReferences[numRef].modifyIsTrain()
		
	'''
	getTrainIndiceRef permet de recuperer l'indice du train
	'''
	def getTrainIndiceRef(self, numRef):
		return self.listReferences[numRef].train
		

	def getReferences(self):
		return self.listReferences
	
	def getReferencesIndice(self, indice):
		return self.listReferences[indice]
	