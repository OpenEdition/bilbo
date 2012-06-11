# encoding: utf-8
'''
Created on 19 avr. 2012

@author: jade
'''

import random
import re
import codecs
from mypkg.extra.Name import Name
from mypkg.extra.Place import Place
from mypkg.extra.Properlist import Properlist

class Extract(object):

	def __init__(self):
		self.cooccurs = {'0000': 0}
		self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0}
		self.nonLabels = {}
		self.features = {}
		self.regles = {}
		
		'''
		charge les nonLabels et les features se trouvant dans le fichier features
		'''
		try:
			'flag = 1 : features, flag = 2 : nonLabels, flag = 3 : bookindicator'
			flag = 0 
			nameRegle = ""	
			for line in open("KB/config/features.txt"):
				lineSplit = re.split("\s", line)
				if lineSplit[0] == "#":
					nameRegle = lineSplit[1]
					flag += 1
				elif flag == 1:
					'features'
					self.features[lineSplit[0]] = 0
				elif flag == 2:
					'nonLabels'
					self.nonLabels[lineSplit[0]] = lineSplit[1]
				else:
					'bookindicator'
					if not self.regles.has_key(nameRegle):
						self.regles[nameRegle] = {}
					self.regles[nameRegle][lineSplit[0]] = 0
		except:
			pass
			print "le fichier features est introuvable : config/features.txt \n"
		
		
		'charge la correspondance des balises fichier balise.txt'
		self.configTag = {}
		
		try:
			for line in open("KB/config/balise.txt", "r"):
				lineSplit = re.split("\s", line)
				self.configTag[lineSplit[0]] = lineSplit[1].split("\n")[0]
		except:
			pass
			print "le fichier balise.txt est introuvable : config.txt \n"
			
		'load lexique name et place'
		self.nameObj = Name("KB/config/externalList/auteurs_revuesorg2.txt")
		self.placeObj = Place("KB/config/externalList/list_pays.txt")
		self.properObj = Properlist("KB/config/externalList/LargeCities.txt", "PLACELIST")
		
	
	'''
	randomgengenerate the indicators for the training and test documents
		 num : number of references
		indice : 1 regenerer les indices, 0: charger les indices en fonction du fichier
	'''
	def randomgen(self, listRef, tr) :
		nbRef = listRef.nbReference()
		
		for i in range(nbRef) :
			if tr == 1 : 
				listRef.modifyTrainIndiceRef(i)
			else : 
				listRef.modifyTestIndiceRef(i)

		return
	
	'''
	loadIndices: permet de charger les indices qui se trouvent dans le fichier
	'''
	def loadIndices(self, fichier):
		indices = []
		
		for line in open(fichier):
			indices.append(line)
			
		return indices
	
	'''
	extractor : extract training and test data
		ndocs : number of references
		typeCorpus : 1, 2 ou 3
		tr : indicator check, it gives the valid instance indices 
		extr : 
		fichierRes = nom du fichier sortie du resultat
	'''
	def extractor (self, typeCorpus, ndocs, fichierRes, listRef, tr=-1, extr=-1) :
		self.titleCK = 0
		self.titleAttr = ''
		self.relatItm = 0
			
		i = 0
		check = -5
		nonbiblck = 1
		
		listReferences = listRef.getReferences()
		tmp_nonbiblck = 0
		for reference in listReferences:
			
			for mot in reference.getWord():
				if mot.ignoreWord == 0:
					if mot.item == 1: self.relatItm = 1
					
					if tr == 1 : check = 1
					else : check = 0
					
					if reference.train == -1:
						mot.delAllTag()
						mot.addTag("nonbibl")
					elif reference.train == check:
												
						# finding just a label which is not in the nonLabels list
						self._checkNonLabels(mot)
						
						#label check
						self._updateTag(mot)
						
						#nobibl check,
						tmp_nonbiblck = 0
						for tmp in mot.getAllTag() :
							if tmp.nom == 'nonbibl' :
								tmp_nonbiblck = 1
							elif tmp.nom == 'c':
								if nonbiblck == 1:
									tmp_nonbiblck = 1

							
						if tr == 0 :
							mot.delAllTag()
					
						'del toutes ls caracteristique qui ne sont pas presente dans le tableau features'
						supp = []
						'si c est de la ponctuation on enleve toutes les caracteristiques'
						balise = mot.getLastTag()
						if balise != -1:
							if balise.nom == "c":
								mot.delAllFeature()
								mot.addFeature("PUNC")
								'sinon on enleve que celle non presente dans les features'
								
						
						for carac in mot.getAllFeature():
							if not self.features.has_key(carac.nom.lower()):
								supp.append(carac.nom)
								
						for nomMot in supp:
							mot.delFeature(nomMot)
							
						if tmp_nonbiblck == 0 : nonbiblck = 0
				
				
			i += 1
			self.titleCK = 0
			self.titleAttr = ''
			self.relatItm = 0
			
			if nonbiblck == 1 :
				reference.bibl = -1
			else : 
				reference.bibl = 1
			nonbiblck = 1
			
		
		if tr != -2 :
			self.nameObj.searchName(listRef, tr)
			self.placeObj.searchPlace(listRef, tr)
			self.properObj.searchProper(listRef, tr, 'place')
		
		if extr == 1 or extr == 2 :
			if tr != -2 :
				self._addlayout(listRef)					####### add layout features ### 2012-02-01 ###
				self._printdata(fichierRes, listRef, tr)
			else:
				self._printOnlyLabel(fichierRes, listRef)
			
		elif extr == 3 or extr == 4 or extr == 5 or extr == 6:
			self._printmoreFeatures(extr)
		
		if typeCorpus == 2:
			'''if tr == 1:
				self._print_alldata(fichierRes, listRef)
			else :'''
			self._print_parallel(fichierRes, listRef)
				
		return

	'''
	_printdata: permet de creer un fichier avec les mots, balises ... pour le crf
	'''
	def _printdata(self, fichier, listRef, tr) :
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			for mot in reference.getWord():
				if mot.ignoreWord == 0:
					try:
						fich.write(unicode(mot.nom,"utf-8"))
					except TypeError:
						fich.write(mot.nom)
					nbCarac = mot.nbFeatures()
					cpt = 0
					if nbCarac > 0:
						caracteristique = mot.getFeatureIndice(nbCarac-1)
						fich.write(" "+caracteristique.nom.upper())
						while cpt < nbCarac-1:
							caracteristique = mot.getFeatureIndice(cpt)
							fich.write(" "+caracteristique.nom.upper())
							cpt += 1
					if tr != 0:
						for balise in mot.getAllTag():
							fich.write(" "+balise.nom)
					fich.write("\n")
			fich.write("\n")
				
		fich.close()
		return
	
	'''
	_printonlyLabel: permet de creer un fichier avec les mots, balises ... pour le crf
	'''
	def _printOnlyLabel(self, fichier, listRef) :
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			for mot in reference.getWord():

				for balise in mot.getAllTag():
					fich.write(balise.nom)
				fich.write("\n")
			fich.write("\n")
				
		fich.close()
		return
		
	def _print_alldata(self, fichier, listRef) :
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			for mot in reference.getWord():
				try:
					fich.write(unicode(mot.nom,"utf-8"))
				except TypeError:
					fich.write(mot.nom)

			fich.write("\n")
				
		fich.close()
		return

	
	#printing result in parallel lines
	def _print_parallel(self, fichier, listRef) :
		phrase = ""
		feature = ""
		cpt = 0;
		
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			cpt=0
			for mot in reference.getWord():
				for feat in mot.listNomFeature():
					feature += feat.upper()+" "
					if cpt == 0 and (feat.lower() == "initial"):
						feature += "STARTINITIAL "
					
				if re.search("NUMBERS", feature) != 0 and re.search("ALLNUMBERS", feature) != 0:	
					phrase += " "+mot.nom
				
				cpt+=1
			
			fich.write(str(reference.bibl))
			fich.write(phrase+"\n")
			fich.write(feature+"\n")
			fich.write("\n")
			
			feature = ""
			phrase = ""
			cpt+=1
				
		fich.close()
		return
	
	
	'''
	addLayout : permet d'adder les caracteristiques : BIBL_START..
	'''
	def _addlayout(self, listRef) :
		
		for reference in listRef.getReferences():
			i = 0
			tmp_length = float(reference.nbWord())
			range_middle = int(tmp_length/3.)
			range_end = int(tmp_length/3.*2.)
			for mot in reference.getWord():

				layout_feature = ''
				if i < range_middle :
					layout_feature = 'BIBL_START'
				elif i < range_end :
					layout_feature = 'BIBL_IN'
				elif i < tmp_length :
					layout_feature = 'BIBL_END'
					
				if layout_feature != '' : 
					mot.addFeature(layout_feature)
					
				i += 1
		return
						
		
			

	def _extract_title(self, mot, relatItm, titleCK, titleAttr) :
		flagU = 0
		
		for caracteristique in mot.getAllFeature():
			if caracteristique.nom == 'a' :
				titleAttr = caracteristique.nom
				mot.delFeature('a')
			elif caracteristique.nom == 'j' or caracteristique.nom == 's' : 
				if titleCK == 1 and titleAttr != caracteristique.nom : 
					balise = mot.getTag("title")
					balise.nom = 'booktitle'
				else : 
					titleAttr = caracteristique.nom
				mot.delFeature('j')
				mot.delFeature('s')
			elif caracteristique.nom == 'm' or caracteristique.nom == 'u' :
				if relatItm == 1 and titleCK == 1 :
					balise = mot.getTag("title")
					balise.nom = 'booktitle'
				else : 
					titleAttr = caracteristique.nom
				mot.delFeature('m')
				mot.delFeature('u')
				
				if caracteristique.nom == "u":
					flagU = 1
			
		############# for thesis ####### 2012-01-19 ###
		namefeature = mot.listNomFeature()
		if flagU == 1 and 'sub' in  namefeature :
				balise = mot.getTag("title")
				balise.nom = 'booktitle'
				mot.delFeature('sub')
				flagU = 0
				
		return titleAttr
		
	'''
	verifTag permet de modifyier les balises en fonction du fichier de configurations balise.txt
	'''
	def _checkTag(self, mot):
		balises = mot.getAllTag()
		
		for balise in balises:
			if self.configTag.has_key(balise.nom):
				balise.nom = self.configTag[balise.nom]
		
	'''
	updateTag permet de modifyier le nom des balise en fonction des fichier de configurations et des regles
	'''
	def _updateTag(self, mot):
		balise = mot.getLastTag()
		if balise != -1:
			nameTag = balise.nom
			self._checkTag(mot)
					
			if nameTag == 'title':
				self.titleAttr = self._extract_title(mot, self.relatItm, self.titleCK, self.titleAttr)
				if mot.getLastTag().nom == 'title' : self.titleCK = 1
	
			'si la balise est noLabel et que le mot est dans le lexique un des lexiques alors on adde la balise correspondante'
			for nameRegle in self.regles:
				if nameTag == 'nolabel' and  (self.regles[nameRegle].has_key(mot.nom.lower())) :
					mot.delAllTag()
					mot.addTag(nameRegle)
			
			#check <date> label for newly updated "publicationDate" attribute
			if nameTag == 'biblscope' :
				if mot.getFeature('publicationDate') != -1:
					mot.delAllTag()
					mot.addTag('date')
				
	'''
	verifNonLabels : permt de garder la meilleur balise du mot et verifier si elle appartient ou non au tableau nonLabels
	'''
	def _checkNonLabels(self, mot):
		j = mot.nbTag() - 2
		if mot.getLastTag() == -1:
			return
		
		'if : si la balise appartient aux tableau nonLabels'
		if self.nonLabels.has_key(mot.getLastTag().nom) :
			try :
				'on parcourt tant que les balise se trouve dans nonLabels st = a la premiere balise qui n est pas dans nonLabel'
				while self.nonLabels.has_key(mot.getTagIndice(j).nom) :
					j -= 1
				saveNom = mot.getTagIndice(j).nom
				mot.delAllTag()
				mot.addTag(saveNom)

				'except: si toutes les balises du mot appartienne a nonLabels'
			except :
				pass
				flag = 0 # if all the labels are one of nonLabels, check if there is abbr and take it as label
				nbTag = mot.nbTag()
				for tag in reversed(range(nbTag)) :
					try:
						nomTag = mot.getTagIndice(tag).nom
						if self.nonLabels[nomTag] == "1":
							flag = 1
							mot.delAllTag()
							mot.addTag(nomTag)
					except:
						pass
				
				if flag == 0:
					mot.delAllTag()
					mot.addTag('nolabel')
				'''
				for jj in reversed(range(j+1)) :
					for nonLabel in self.nonLabels:
						if self.nonLabels[nonLabel] == 1:
							if mot.getTagIndice(jj).nom == nonLabel:
								mot.delAllTag()
								mot.addTag(nonLabel)
								flag = 1
					if flag == 0:
						mot.delAllTag()
						mot.addTag('nolabel')'''

		else:
			saveNom = mot.getLastTag().nom
			mot.delAllTag()
			mot.addTag(saveNom)	
		
