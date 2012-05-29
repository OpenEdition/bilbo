'''
Created on 18 avr. 2012

@author: jade
'''


class Reference(object):
	'''
	classdocs
	'''

	'''
	Constructor
	word
	'''
	def __init__(self, word, num):
		self.word = word
		self.num = num
		self.train = 0
		self.bibl = 0
		
	def affiche(self):
		print "reference numero : ",self.num,
		for key in self.word:
			key.affiche()
		print "\n"
		
	'''
	nbword: retourne le nombre de word que contient la reference
	'''
	def nbWord(self):
		return len(self.word)
	'''
	permet d'ajouter un word a l'indice donne
	'''
	def addWord(self, indice, word):
		self.word.insert(indice,word)
	
	'''
	isTrain permet d'indiquer si la reference fait partie du train
	return 0 si train et 1 si test
	'''	
	def isTrain(self):
		return self.train
	
	'''
	modifIsTrain permet d'indiquer que la reference fait partie du train donc = 1
	'''	
	def modifyIsTrain(self):
		self.train = 1
	
		'''
	modifIsTest permet d'indiquer que la reference fait partie du test donc = 0
	'''	
	def modifyIsTest(self):
		self.train = 0
	
	'''
	retourne tous les word de la reference
	'''
	def getWord(self):
		return self.word
	
	'''
	retourne le word qui se trouve a l'indice i
	'''
	def getWordIndice(self, i):
		return self.word[i]
	
	def __str__(self):
		ref = ""
		for word in self.word:
			ref += " "+word.nom
		return ref
	