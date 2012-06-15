# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''
from mypkg.format.CleanCorpus1 import CleanCorpus1
from mypkg.format.CleanCorpus2 import CleanCorpus2
from mypkg.format.Rule import Rule
from mypkg.reference.ListReferences import ListReferences
from mypkg.ressources.BeautifulSoup import *
import re
import sys

class File(object):
	'''
	classdocs
	'''


	def __init__(self, fname):
		'''
		Constructor
		'''
		self.nom = fname
		self.corpus = {}
	
	'''
	extraireCorpus1 : extrait les references du fichier correspondant au corpus 1
	'''
	def extractCorpus1(self):
		clean = CleanCorpus1()
		references = clean.processing(self.nom, "bibl")
		if len(references) >= 1:
			self.corpus[1] = ListReferences(references, 1)
			
			rule = Rule()
			rule.reorganizing(self.corpus[1])
		
		
	'''
	extraireCorpus2 : extrait les references du fichier correspondant au corpus 1
	'''
	def extractCorpus2(self):
		clean = CleanCorpus2()
		references = clean.processing(self.nom, "note")
		if len(references) >= 1:
			self.corpus[2] = ListReferences(references, 2)
			
			rule = Rule()
			rule.reorganizing(self.corpus[2])
		
	'''
	getListReferences : permet de recuperer la liste entiere des references du corpus 1
	typeCorpus : int numero du corpus
	'''
	def getListReferences(self, typeCorpus):
		try:
			return self.corpus[typeCorpus]
			
		except :
			return -1
		
	'''
	calcul le nombre de reference
	'''
	def nbReference(self, typeCorpus):
		try:
			return self.corpus[typeCorpus].nbReference()
			
		except :
			return 0		
	
	def _html2unicode(self, tmp_str) :
		#for numerical codes
		matches = re.findall("&#\d+;", tmp_str)
		if len(matches) > 0 :
			hits = set(matches)
			for hit in hits :
				name = hit[2:-1]
				try :
					entnum = int(name)
					tmp_str = tmp_str.replace(hit, unichr(entnum))
				except ValueError:
					pass
	
		#for hex codes
		matches = re.findall("&#[xX][0-9a-fA-F]+;", tmp_str)
		if len(matches) > 0 :
			hits = set(matches)
			for hit in hits :
				hex = hit[3:-1]
				try :
					entnum = int(hex, 16)
					tmp_str = tmp_str.replace(hit, unichr(entnum))
				except ValueError:
					pass
		
		tmp_str = tmp_str.replace('&','&amp;')
		
		return tmp_str

	
	'''
	buildReferences : construit le fichier final
		references : reference annote par mallet
		tagTypeCorpus : balise qui entour la reference : corpus 1 = bibl
		tagTypeList : balise qui entoure les references : corpus 1 = listbibl
	'''
	def buildReferences(self, references, tagTypeCorpus, tagTypeList):
		cptWord = 0
		cptRef = 0
		cptItem = 0
		tmp_str = ""
		flagItem = 0
		balise = ""
		baliseBefore = ""
		ref_finale = ""
		flagNonLabel = 0
		
		'lit le fichier resultat de mallet'
		for line in open (self.nom, 'r') :
			tmp_str = tmp_str + ' ' + line
				
		soup = BeautifulSoup (tmp_str)
		
		s = soup.findAll (tagTypeCorpus)
		
		'reconstruit les references avec les mot ignores ex: balise hi'
		for ref in references:
			balise = ""
			baliseBefore = ""
			flagItem = 0
			ref_finale = ""
			ref_ori = s[cptRef]
			ref_ori.contents = []
			cptWord = 0
			allTag = ref.findAll(True)
			
			for tag in allTag:
				content = tag.contents
				words = re.split("\s", content[0])
				for word in words:
					if word != "":
						wordInRef = self.corpus[1].getReferencesIndice(cptRef).getWordIndice(cptWord)
						
						'transforme en unicode'
						wordInRef.nom = self.convertToUnicode(wordInRef.nom)
						tag.name = self.convertToUnicode(tag.name)
						
						'verifie si le mot doit etre ignore ou non: ignore = considere comme balise nonLabel a ajouter au fichier final'
						while wordInRef.ignoreWord == 1:
							if baliseBefore != "":
								ref_finale += "</"+baliseBefore+">"
								baliseBefore = ""
							if balise != "c" and balise != "":
								ref_finale += "</"+balise+">"
								balise = ""
							ref_finale += wordInRef.nom
							cptWord += 1
							wordInRef = self.corpus[1].getReferencesIndice(cptRef).getWordIndice(cptWord)
							balise = ""
							wordInRef.nom = self.convertToUnicode(wordInRef.nom)
							
							
						'if il y a une sous reference'
						if wordInRef.item == 1 and flagItem == 0:
							flagItem = 1
							if baliseBefore != "":
								ref_finale += "</"+baliseBefore+">"
								baliseBefore = ""
							if balise != "c" and balise != "":
								ref_finale += "</"+balise+">"
								balise = ""
							ref_finale += "<relatedItem type=\"in\">"
							balise = ""								

						if balise == tag.name:
							ref_finale += " "+wordInRef.nom
						elif balise == "":
							if tag.name != "c":
								ref_finale += "<"+tag.name+">"+wordInRef.nom
							else:
								ref_finale += wordInRef.nom
							balise = tag.name
						else:
							if balise != "c" and tag.name != "c":
								ref_finale += "</"+balise+">"+"<"+tag.name+">"+wordInRef.nom
							elif balise == "c" and tag.name != "c":
								if baliseBefore == tag.name:
									ref_finale += wordInRef.nom
								else:
									if baliseBefore != "":
										ref_finale += "</"+baliseBefore+">"+"<"+tag.name+">"+wordInRef.nom
									else:
										ref_finale += "<"+tag.name+">"+wordInRef.nom
									baliseBefore = ""
							elif balise != "c" and tag.name == "c":
								ref_finale += wordInRef.nom
								baliseBefore = balise
							else:
								ref_finale += wordInRef.nom
							balise = tag.name

						cptWord += 1

			if balise != "c":	
				ref_finale += "</"+balise+">"
				
			'if il y a une sous reference on ajoute la balise de fin'
			if flagItem == 1:
				cptItem += 1
				if baliseBefore != "":
					ref_finale += "</"+baliseBefore+">"
					baliseBefore = ""
				else:
					ref_finale += "</"+balise+">"
				ref_finale += "</relatedItem>"	
			cptRef += 1	
			ref_ori.append(ref_finale)
			
		'supprime les dernieres references considere comme items..'
		while cptItem > 0:
			s.pop()
			cptItem -= 1
			
		try:
			listBibl = soup.find(tagTypeList)
			listBibl.contents = []
			listBibl.contents = s
		except :
			pass
		
		fich = open("Result/"+self._getName(), "w")
		fich.write(soup.prettify())
		fich.close()
		return
	
	'''
	getName : retourne le nom du fichier sns le chemin complte
	'''
	def _getName(self):
		chemin = self.nom.split("/")
		return chemin.pop()
	
	'''
	convertToUnicode : converti une chaine en unicode
	'''
	def convertToUnicode(self, chaine):
		try:
			if isinstance(chaine, str):
				chaine = unicode(chaine, sys.stdin.encoding)
		except:
			chaine = unicode(chaine, 'ascii')
		return chaine

	