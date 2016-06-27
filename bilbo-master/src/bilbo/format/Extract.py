# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 19, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.extra.Name import Name
from bilbo.extra.Place import Place
from bilbo.extra.Properlist import Properlist
import sys, os
import re
from codecs import open

class Extract(object):
	"""
	A class to extract training and test data according to a set of predefined criteria
	Base class of Extract_crf and Extract_svm
	"""

	def __init__(self, options={}):
		"""
		Attributes
		----------
		nonLabels : dict
			tags that should be ignored
		features : dict
			features that should be taken finally
		regles : dict
			several rules to be considered
		configTag : dict
			tag matching rules
		nameObj : Name
		placeObj : Place
		properObj :	Properlist
		"""
		self.options = options
		self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0}
		self.nonLabels = {}
		self.features = {}
		self.regles = {}
		
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-4])
		
		'Fill "nonLabels" and "features" that are in the file "feature.txt"'
		
		try:
			'flag = 1 : features, flag = 2 : nonLabels, flag = 3 : bookindicator'
			flag = 0
			nameRegle = ""
			
			for line in open(os.path.join(self.rootDir, "KB/config/features.txt"), encoding='utf8'):
				lineSplit = re.split("\s", line, flags=re.UNICODE)
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
		except IOError:
			print "Cannot open the file \"KB/config/features.txt\" \n"
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		
		
		'Load the tag matching rules in "balise.txt"'
		self.configTag = {}
		
		if self.options.i == "tei" :
			try:
				for line in open(os.path.join(self.rootDir, "KB/config/balise.txt"), "r", encoding='utf8'):
					lineSplit = re.split("\s", line, flags=re.UNICODE)
					self.configTag[lineSplit[0]] = lineSplit[1].split("\n")[0]
				if self.options.g == "detail" :
					del self.configTag['meeting']
			except IOError:
				print "Cannot open the file \"KB/config/balise.txt\" \n"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				raise
			
		'Load people name and place'
		self.nameObj = Name(os.path.join(self.rootDir, "KB/config/externalList/auteurs_revuesorg2.txt")) #SURNAMELIST, FORENAMELIST
		self.placeObj = Place(os.path.join(self.rootDir, "KB/config/externalList/list_pays.txt")) #PLACELIST
		self.cityObj = Properlist(os.path.join(self.rootDir, "KB/config/externalList/LargeCities.txt"), "PLACELIST") #PLCAELIST
		self.journalObj = Properlist(os.path.join(self.rootDir, "KB/config/externalList/journalAll.txt"), "JOURNALLIST") #PLCAELIST


	def extract(self):
		"""
		To be defined in a sub class
		"""
		return


	def randomgen(self, listRef, tr) :
		"""
		Generate indicators for the training and test documents
		
		Parameters
		----------
		listRef : listReferences
		tr : int, {1, 0, -1, -2}
			check if training or test data
		"""
		nbRef = listRef.nbReference()
		
		for i in range(nbRef) :
			if tr == 1 : #if training data indicator for training (1)
				listRef.modifyTrainIndiceRef(i)
			else : #if not, indicator for test (0)
				listRef.modifyTestIndiceRef(i)

		return


	def loadIndices(self, fichier):
		"""
		Load the indices of the File object
		"""
		indices = []
		for line in open(fichier, encoding='utf8'):
			indices.append(line)
			
		return indices


	def _printdata(self, fichier, listRef, tr, opt="saveNegatives") : #default value of 'opt' is "saveNegatives"
		"""
		Print training or test data for Mallet CRF
		"""
		fich = open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			if (not (opt=="deleteNegatives" and reference.train == -1)) and (not (opt=="deletePositives" and reference.train != -1)) :
			
				for mot in reference.getWord():
					if mot.ignoreWord == 0:
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
							balise = mot.getLastTag()
							fich.write(" "+balise.nom)
						fich.write("\n")
				fich.write("\n")
			#--------
		fich.close()
		return


	def _printdataWapiti(self, fichier, listRef, tr, opt="saveNegatives") : #default value of 'opt' is "saveNegatives"
		"""
		Print training or test data for Wapiti CRF
		"""
		features = [['ALLNUMBERS', 'NUMBERS'],	#1
					['DASH'],					#2
					['ALLCAP', 'ALLSMALL', 'FIRSTCAP', 'NONIMPCAP'],	#3
					['BIBL_START', 'BIBL_IN', 'BIBL_END'],				#4
					['INITIAL'],	#5
					['WEBLINK'],	#6
					['ITALIC'],		#7
					['POSSEDITOR'],	#8
					['POSSPAGE'],	#9
					['POSSMONTH'],	#10POSSMONTH
					['SURNAMELIST'],	#11
					['FORENAMELIST'],	#12
					['PLACELIST'],		#13
					['JOURNALLIST']]	#14
		if self.options.u : features.append(['PUNC', 'COMMA', 'POINT', 'LEADINGQUOTES', 'ENDINGQUOTES', 'LINK','PAIREDBRACES'])

		fich = open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			if (not (opt=="deleteNegatives" and reference.train == -1)) and (not (opt=="deletePositives" and reference.train != -1)):
			
				for mot in reference.getWord():
					tmp_features = ['NONUMBERS', 'NODASH', 'NONIMPCAP', 'NULL', 'NOINITIAL',
									'NOWEBLINK', 'NOITALIC', 'NOEDITOR', 'NOPAGE', 'NOMONTH', 'NOSURLIST',
									'NOFORELIST', 'NOPLACELIST', 'NOJOURLIST']#, 'NOPUNC']#, 'NOJOURLIST']
					if self.options.u : tmp_features.append('NOPUNC')
					if mot.ignoreWord == 0:
						fich.write(mot.nom)
						nbCarac = mot.nbFeatures()
						cpt = 0
						if nbCarac > 0:
							total_features = ""
							caracteristique = mot.getFeatureIndice(nbCarac-1)
							cur_feature = ""
							cur_feature = caracteristique.nom.upper()
							total_features += cur_feature+" "
							
							while cpt < nbCarac-1:
								caracteristique = mot.getFeatureIndice(cpt)
								cur_feature = caracteristique.nom.upper()
								total_features += cur_feature+" "
								cpt += 1
							
							for i in range(len(features)) :
								cur_feature = ''
								for j in range(len(features[i])) :
									if total_features.count(features[i][j]) > 0 :
										cur_feature = features[i][j]
								if cur_feature != '' :
									tmp_features[i] = cur_feature
							
							string_features = ""
							for ftr in tmp_features :
								string_features += ftr+" "
							fich.write(" "+string_features)
							
						if tr != 0:
							balise = mot.getLastTag()
							fich.write(" "+balise.nom)
						fich.write("\n")
				fich.write("\n")
			#--------
		fich.close()
		return


	def _printOnlyLabel(self, fichier, listRef) :
		"""
		Print training or test data for CRF (only labels)
		"""
		fich = open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			for mot in reference.getWord():

				for balise in mot.getAllTag():
					fich.write(balise.nom)
				fich.write("\n")
			fich.write("\n")
				
		fich.close()
		return


	def _print_alldata(self, fichier, listRef) :
		"""
		Print all data for SVM
		"""
		fich = open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			for mot in reference.getWord():
				fich.write(mot.nom)

			fich.write("\n")
				
		fich.close()
		return


	def _print_parallel(self, fichier, listRef) :
		"""
		Print result in parallel lines for SVM
		"""
		phrase = ""
		feature = ""
		cpt = 0;
		
		fich = open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			cpt=0
			for mot in reference.getWord():
				#mot.nom = self.convertToUnicode(mot.nom)
				if mot.ignoreWord == 0:
					for feat in mot.listNomFeature():
						feature += feat.upper()+" "
						if cpt == 0 and (feat.lower() == "initial"):
							feature += "STARTINITIAL "
					if re.search("NUMBERS", feature, flags=re.UNICODE) != 0 and re.search("ALLNUMBERS", feature, flags=re.UNICODE) != 0:
						phrase += " "+mot.nom
					cpt+=1

			fich.write(unicode(reference.bibl))
			fich.write(phrase+"\n")

			fich.write(feature+"\n")
			
			fich.write("\n")
			
			feature = ""
			phrase = ""
			cpt+=1
				
		fich.close()
		return


	def _addlayout(self, listRef) :
		"""
		Add layout features
		"""
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
		"""
		Title tag rearrangement. by checking the attribute, re-tag the word as "title" or "booktitle"
		
		Parameters
		----------
		mot : Word
			current word
		relatItm : int
		titleCK : int
			indicates if there is another title string before this
		titleAttr : char
			attribute
				according to TEI guidelines,
				a - (analytic) analytic title (article, poem, or other item published as part of a larger item)
				m - (monographic) monographic title (book, collection, or other item published as a distinct item, including single volumes of multi-volume works)
				j - (journal) journal title
				s - (series) series title
				u -	(unpublished) title of unpublished material (including theses and dissertations unless published by a commercial press)
		"""
		flagU = 0
		
		for caracteristique in mot.getAllFeature():
			if caracteristique.nom == 'a' :
				titleAttr = caracteristique.nom
				mot.delFeature('a')
			elif caracteristique.nom == 'j' or caracteristique.nom == 's' or caracteristique.nom == 'm':
				if titleCK == 1 and titleAttr != caracteristique.nom :
					balise = mot.getTag("title")
					if balise > 0 : balise.nom = 'booktitle'
				else :
					titleAttr = caracteristique.nom
				mot.delFeature('j')
				mot.delFeature('s')
			if caracteristique.nom == 'm' or caracteristique.nom == 'u' :
				if relatItm == 1 and titleCK == 1 :
					balise = mot.getTag("title")
					if balise > 0 : balise.nom = 'booktitle'
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


	def _extract_title_alter(self, mot, relatItm, titleCK, titleAttr) :
		"""
		Alternative title tag extraction. Separate all types of title.
		
		Parameters
		----------
		mot : Word
			current word
		relatItm : int
		titleCK : int
			indicates if there is another title string before this
		titleAttr : char
			attribute
				according to TEI guidelines,
				a - (analytic) analytic title (article, poem, or other item published as part of a larger item)
				m - (monographic) monographic title (book, collection, or other item published as a distinct item, including single volumes of multi-volume works)
				j - (journal) journal title
				s - (series) series title
				u -	(unpublished) title of unpublished material (including theses and dissertations unless published by a commercial press)
		"""
		for caracteristique in mot.getAllFeature():
			if caracteristique.nom == "a" :
				balise = mot.getTag("title")
				if balise != -1 : balise.nom = "title_a"
			elif caracteristique.nom == "m" or caracteristique.nom == "volume_title" :
				balise = mot.getTag("title")
				if balise != -1  : balise.nom = "title_m"
			elif caracteristique.nom == "j" :
				balise = mot.getTag("title")
				if balise != -1  : balise.nom = "title_j"
			elif caracteristique.nom == "s" :
				balise = mot.getTag("title")
				if balise != -1 : balise.nom = "title_s"
			elif caracteristique.nom == "u" :
				balise = mot.getTag("title")
				if balise != -1 : balise.nom = "title_u"
			elif caracteristique.nom == "translated_title" :
				balise = mot.getTag("title")
				if balise != -1 : balise.nom = "title_t"
			elif caracteristique.nom == "research_programm" :
				balise = mot.getTag("title")
				if balise != -1 : balise.nom = "title_r"
		
		return titleAttr


	def _extract_biblscope(self, mot):
		for caracteristique in mot.getAllFeature():
			if caracteristique.nom == "vol" :
				balise = mot.getTag("biblscope")
				if balise != -1 : balise.nom = "biblscope_v"
			elif caracteristique.nom == "issue" :
				balise = mot.getTag("biblscope")
				if balise != -1  : balise.nom = "biblscope_i"
			elif caracteristique.nom == "pp" :
				balise = mot.getTag("biblscope")
				if balise != -1  : balise.nom = "biblscope_pp"
			elif caracteristique.nom == "chap" :
				balise = mot.getTag("biblscope")
				if balise != -1 : balise.nom = "biblscope_c"
			elif caracteristique.nom == "part" :
				balise = mot.getTag("biblscope")
				if balise != -1 : balise.nom = "biblscope_pa"
		#print "***AFTER"
		
		return


	def _checkTag(self, mot):
		"""
		Modify tags according to the configuration in the file "balise.txt"
		"""
		balises = mot.getAllTag()
		
		for balise in balises:
			if self.configTag.has_key(balise.nom):
				balise.nom = self.configTag[balise.nom]
		
		return


	def _updateTag(self, mot):
		"""
		Modify tags according to the configuration and rules
		"""
		balise = mot.getLastTag()
		
		if balise != -1:
			nameTag = balise.nom
			self._checkTag(mot)
					
			if nameTag == 'title' or mot.getTag("title") != -1 :
				if self.options.g == 'simple' :
					self.titleAttr = self._extract_title(mot, self.relatItm, self.titleCK, self.titleAttr)
				elif self.options.g == 'detail' :
					self.titleAttr = self._extract_title_alter(mot, self.relatItm, self.titleCK, self.titleAttr)
				if mot.getLastTag().nom == 'title' : self.titleCK = 1
	
			#bookindicator
			'if the tag is one of noLabel and the word is one of regles, add the corresponding nameRegle tag(bookindicator)'
			for nameRegle in self.regles:
				if nameTag == 'nolabel' and  (self.regles[nameRegle].has_key(mot.nom.lower())) :
					mot.delAllTag()
					mot.addTag(nameRegle)
			
			#check <date> label for newly updated "publicationDate" attribute
			if nameTag == 'biblscope' :
				if self.options.g == 'detail' : self._extract_biblscope(mot)
				if mot.getFeature('publicationDate') != -1:
					mot.delAllTag()
					mot.addTag('date')


	def _checkNonLabels(self, mot):
		"""
		Keep the best tag of the word and verify if it appears in nonLabels
		"""
		j = mot.nbTag() - 2
		if mot.getLastTag() == -1:
			return
		
		'if a tag appears in nonLabels'
		if self.nonLabels.has_key(mot.getLastTag().nom) :
			try :
				'we repeat while the tags are in nonLabels and extract upper tag if it is not in nonLabels'
				while self.nonLabels.has_key(mot.getTagIndice(j).nom) :
					j -= 1
				saveNom = mot.getTagIndice(j).nom
				mot.delAllTag()
				mot.addTag(saveNom)

				'if all tags are in a nonLabels'
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

		else:
			saveNom = mot.getLastTag().nom
			mot.delAllTag()
			mot.addTag(saveNom)


	def extractIndices(self, svmprediction_trainfile, listRef):
		"""
		Extract indices for nonbibls from SVM classification result
		then modify 'train' attribute of each reference
		
		Parameters
		----------
		svmprediction_trainfile : string
			SVM classification result for training data
		listRef : list
			reference list
		"""
		nbRef = listRef.nbReference()
		
		svm_train = []
		for line in open (svmprediction_trainfile, 'r', encoding='utf8') :
			line = line.split()
			svm_train.append(float(line[0]))
	
		positive_indices = range(nbRef)
		
		n=0 #for all
		j=0	#for train
		for n in range(nbRef) :
			if svm_train[j] > 0 :
				positive_indices[n] = 1
			else :
				positive_indices[n] = 0
			j += 1
		
		n=0
		for ref in listRef.getReferences() :
			if positive_indices[n] == 0 : # instance NOT OK so attribute train = -1
				ref.train =  -1
			n += 1
		
		return


	def extractIndices4new(self, svmprediction_newfile, listRef):
		"""
		Extract indices for nonbibls from SVM classification result
		then modify 'train' attribute of each reference
		
		Parameters
		----------
		svmprediction_newfile : string
			SVM classification result for test data
		listRef : list
			reference list
		"""
		i = 0
		
		for line in open (svmprediction_newfile, 'r', encoding='utf8') :
			line = line.split()
			if float(line[0]) > 0 :
				listRef.getReferencesIndice(i).train = 0
			else :
				listRef.getReferencesIndice(i).train = -1
			i += 1
		return
