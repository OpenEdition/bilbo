# -*- coding: utf-8 -*-
'''
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
'''

class Reference(object):
	'''
	classdocs
	'''

	'''
	Constructor
	word
	'''
	def __init__(self, words, num):
		self.words = words
		self.num = num
		self.train = 0 # 1:train, 0:test, -1:classified as negative for SVM note classification
		self.bibl = 0
		
	def affiche(self):
		print "reference number : ",self.num,
		for key in self.words:
			key.affiche()
		print "\n"


	def nbWord(self):
		'''
		Return the number of words in the reference
		'''
		return len(self.words)


	def addWord(self, index, word):
		'''
		Add a word at the given index
		'''
		self.words.insert(index,word)
	

	def isTrain(self):
		'''
		Indicate if the reference is for training or test
		return 0 if train and 1 test
		'''			
		return self.train
	

	def modifyIsTrain(self):
		'''
		Modify the value of an indicator, which tells if a reference is training data or test data
		Set the value as train
		'''
		self.train = 1
	

	def modifyIsTest(self):
		'''
		Modify the value of an indicator, which tells if a reference is training data or test data
		Set the value as test
		'''		
		self.train = 0
	

	def getWord(self):
		'''
		Return all the words of the reference
		'''		
		return self.words
	

	def getWordIndice(self, i):
		'''
		Return the word at the index i
		'''
		return self.words[i]
	
	
	def __str__(self):
		ref = ""
		for word in self.words:
			ref += " "+word.nom
		return ref 
	
	
	def replaceReference(self, words, num):
		self.words = words
		self.num = num
		
		return
	
		
	