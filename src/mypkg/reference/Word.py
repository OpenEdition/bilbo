# -*- coding: utf-8 -*-
'''
Created on 18 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''
from mypkg.reference.Balise import  Balise
from mypkg.reference.Feature import  Feature

class Word(object):
	'''
	classdocs
	'''


	def __init__(self, mot, tags=[], features=[]):
		'''
		Constructor
		'''
		'genere les objets Tag'
		self.nom = mot
		self.tag = []
		self.feature = []
		self.ignoreWord = 0
		'item : permet de savoir si le mot fait parti d une sous reference'
		self.item = 0			
		
		for tag in tags:
			'enleve les espaces au debuts et a la fin'
			tag.lstrip()
			tag.rstrip()
			if tag != "" and self.getTag(tag) == -1:
				self.tag.append(Balise(tag))
			
		'genere les objets Feature'
		for feature in features:
			'enleve les espaces au debuts et a la fin'
			feature.lstrip()
			feature.rstrip()
			if feature != "" and self.getFeature(feature) == -1:
				self.feature.append(Feature(feature))

	
	def affiche(self):
		print "\nmot : ",self.nom
		if len(self.tag) >= 1:
			print "\tBALISE :"
			for key in self.tag:
				key.affiche()
		
		if len(self.feature) >= 1:
			print "\tCARACTERISTIQUE :"
			for key in self.feature:
				key.affiche()
	
	'''
	add feature
	'''
	def addFeature(self,feature):
		if isinstance(feature, list):
			for carac in feature:
				'enleve les espaces au debuts et a la fin'
				carac.lstrip()
				carac.rstrip()
				if carac != "" and self.getFeature(carac) == -1:
					self.feature.append(Feature(carac))
		else:
			'enleve les espaces au debuts et a la fin'
			feature.lstrip()
			feature.rstrip()
			if self.getFeature(feature) == -1:
				self.feature.append(Feature(feature))
		
	'''
	add tag
	'''
	def addTag(self,tag):
		if isinstance(tag, list):
			for bal in tag:
				'enleve les espaces au debuts et a la fin'
				bal.lstrip()
				bal.rstrip()
				if bal != "" and self.getTag(bal) == -1:
					self.tag.append(Balise(bal))
		else:
			'enleve les espaces au debuts et a la fin'
			tag.lstrip()
			tag.rstrip()
			if self.getTag(tag) == -1:
				self.tag.append(Balise(tag))
		
	'''
	del feature
	'''
	def delFeature(self,feature):
		ref = self.getFeature(feature)
		if ref != -1:
			self.feature.remove(ref)
		return -1
	
	'''
	del tag
	'''
	def delTag(self,tag):
		ref = self.getTag(tag)
		if ref != -1:
			self.tag.remove(ref)
		return -1
	
	'''
	del toutes les features
	'''
	def delAllFeature(self):
		del(self.feature[:])
	
	'''
	del les toutes tags
	'''
	def delAllTag(self):
		del(self.tag[:])

		
	'''
	recherche feature
	'''
	def getFeature(self,feature):
		for carac in self.feature:
			if carac.nameIs(feature) == 1:
				return carac
		return -1
		
	'''
	recherche tag
	'''
	def getTag(self,tag):
		for bal in self.tag:
			if bal.nameIs(tag) == 1:
				return bal
		return -1
	
	'''
	liste nom des features
	'''
	def listNomFeature(self):
		carac = []
		for key in self.feature:
			carac.append(key.nom)
		return carac
		
	'''
	liste les noms des tags
	'''
	def listNomTag(self):
		bal = []
		for key in self.tag:
			bal.append(key.nom)
		return bal
	
	'''
	getDerniererFeature : retourne la feature adde en dernier
	'''
	def getLastFeature(self):
		if len(self.feature) == 0:
			return -1
		return self.feature[len(self.feature)-1]
	
		'''
	getDerniereTag : retourne la tag adde en dernier
	'''
	def getLastTag(self):
		if len(self.tag) == 0:
			return -1
		return self.tag[len(self.tag)-1]
	
	'''
	getFeatureIndice : retourne la feature a l'indice "indice"
	'''
	def getFeatureIndice(self, indice):
		if indice < 0: return -1
		return self.feature[indice]
	
		'''
	getTagIndice : retourne la tag a l'indice "indice"
	'''
	def getTagIndice(self, indice):
		if indice < 0: return -1
		return self.tag[indice]
	
	'''
	getAllFeature : retourne les features 
	'''
	def getAllFeature(self):
		return self.feature
	
		'''
	getAllTag : retourne les tags
	'''
	def getAllTag(self):
		return self.tag
	
	'''
	nbTags: retourne le nombre de tag 
	'''
	def nbTag(self):
		return len(self.tag)
	
	'''
	nbFeatures: retourne le nombre de features 
	'''
	def nbFeatures(self):
		return len(self.feature)
	
	def __getattr__(self, nom):
		print("Alerte ! Il n'y a pas d'attribut {0} ici !".format(nom))
		
	'''
	buildReference :  permet de construire la reference final
	'''
	'''def buildReference(self):
		self.nom = self.nom.replace('&amp;', '&')
		ref = "<"+self.getLastTag().nom+">"+self.nom+"</"+self.getLastTag().nom+">"
		return ref'''