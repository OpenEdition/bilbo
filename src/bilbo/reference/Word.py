# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.reference.Balise import  Balise
from bilbo.reference.Feature import  Feature

class Word(object):
	"""
	A class corresponding to a word in a reference. It contains word name, features, tags, etc.
	Word object is first created in CleanCorpus1 and CleanCorpus2.
	"""


	def __init__(self, mot, tags=[], features=[]):
		"""
		nom : word name
		tag : list of Balise objects
		feature : list of Feature objects
		item : indicator of sub-reference (0 : no, 1 : yes)
		"""
		'Generate Tag objects'
		self.nom = mot
		self.core = mot
		self.tag = []
		self.feature = []
		self.ignoreWord = 0
		'item is an indicator showing if the word is in a sub reference'
		self.item = 0
		#print "mot " + str(type(mot))
		if type(mot) is str:
			print mot
		
		for tag in tags:
			'Eliminate the spaces at the beginning and ending'
			tag.lstrip()
			tag.rstrip()
			if tag != "" and self.getTag(tag) == -1:
				self.tag.append(Balise(tag))
			
		'Generate Feature objects'
		for feature in features:
			'Eliminate the spaces at the beginning and ending'
			feature.lstrip()
			feature.rstrip()
			if feature != "" and self.getFeature(feature) == -1:
				self.feature.append(Feature(feature))

	
	def affiche(self):
		print "\nWord : ",self.nom, self.core
		#print type(self.nom)
		if len(self.tag) >= 1:
			print "\tTAG :"
			for key in self.tag:
				key.affiche()
		
		if len(self.feature) >= 1:
			print "\tFEATURE :"
			for key in self.feature:
				key.affiche()
	

	def addFeature(self,feature):
		if isinstance(feature, list):
			for carac in feature:
				'Eliminate the spaces at the beginning and ending'
				carac.lstrip()
				carac.rstrip()
				if carac != "" and self.getFeature(carac) == -1:
					self.feature.append(Feature(carac))
		else:
			'Eliminate the spaces at the beginning and ending'
			feature.lstrip()
			feature.rstrip()
			if self.getFeature(feature) == -1:
				self.feature.append(Feature(feature))
		

	def addTag(self,tag):
		if isinstance(tag, list):
			for bal in tag:
				'Eliminate the spaces at the beginning and ending'
				bal.lstrip()
				bal.rstrip()
				if bal != "" and self.getTag(bal) == -1:
					self.tag.append(Balise(bal))
		else:
			'Eliminate the spaces at the beginning and ending'
			tag.lstrip()
			tag.rstrip()
			if self.getTag(tag) == -1:
				self.tag.append(Balise(tag))
		

	def delFeature(self,feature):
		ref = self.getFeature(feature)
		if ref != -1:
			self.feature.remove(ref)
		return -1
	

	def delTag(self,tag):
		ref = self.getTag(tag)
		if ref != -1:
			self.tag.remove(ref)
		return -1


	def delAllFeature(self):
		del(self.feature[:])
	

	def delAllTag(self):
		del(self.tag[:])


	def getFeature(self,feature):
		for carac in self.feature:
			if carac.nameIs(feature) == 1:
				return carac
		return -1
		

	def getTag(self,tag):
		print "getTag"
		for bal in self.tag:
			if bal.nameIs(tag) == 1:
				return bal
		return -1
	

	def listNomFeature(self):
		carac = []
		for key in self.feature:
			carac.append(key.nom)
		return carac
		

	def listNomTag(self):
		bal = []
		for key in self.tag:
			bal.append(key.nom)
		return bal
	

	def getLastFeature(self):
		"""
		Return the last feature
		"""
		if len(self.feature) == 0:
			return -1
		return self.feature[len(self.feature)-1]
	

	def getLastTag(self):
		"""
		Return the last tag
		"""		
		if len(self.tag) == 0:
			return -1
		if self.tag[len(self.tag)-1].nom == 'hi' and len(self.tag) > 1:
			return self.tag[len(self.tag)-2]
		return self.tag[len(self.tag)-1]
	


	def getFeatureIndice(self, index):
		"""
		Return the feature at the index
		"""
		if index < 0: return -1
		return self.feature[index]
	
	
	def getTagIndice(self, index):
		"""
		Return the tag at the index
		"""
		if index < 0: return -1
		return self.tag[index]
	

	def getAllFeature(self):
		"""
		Return all the features
		"""		
		return self.feature
	

	def getAllTag(self):
		"""
		Return all the tags
		"""		
		return self.tag
	

	def nbTag(self):
		"""
		Return the number of tags
		"""		
		return len(self.tag)


	def nbFeatures(self):
		"""
		Return the number of features
		"""	
		return len(self.feature)
	
	
	def __getattr__(self, nom):
		print("Alert ! There is no attribute {0} here !".format(nom))
		

