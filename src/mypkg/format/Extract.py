# encoding: utf-8
'''
Created on 19 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''
from mypkg.extra.Name import Name
from mypkg.extra.Place import Place
from mypkg.extra.Properlist import Properlist
import sys
import re
import codecs

class Extract(object):
	'''
	A class to extract training and test data according to a set of predefined criteria
	Base class of Extract_crf and Extract_svm
	'''

	def __init__(self):
		'''
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
		'''
		self.cooccurs = {'0000': 0}
		self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0}
		self.nonLabels = {}
		self.features = {}
		self.regles = {}
		
		'''
		Fill "nonLabels" and "features" that are in the file "feature.txt"
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
			print "Cannot open the file \"KB/config/features.txt\" \n"
		
		
		'Load the tag matching rules in "balise.txt"'
		self.configTag = {}
		
		try:
			for line in open("KB/config/balise.txt", "r"):
				lineSplit = re.split("\s", line)
				self.configTag[lineSplit[0]] = lineSplit[1].split("\n")[0]
		except:
			pass
			print "Cannot open the file \"KB/config/balise.txt\" \n"
			
		'Load people name and place'
		self.nameObj = Name("KB/config/externalList/auteurs_revuesorg2.txt")
		self.placeObj = Place("KB/config/externalList/list_pays.txt")
		self.properObj = Properlist("KB/config/externalList/LargeCities.txt", "PLACELIST")
		
	
	
	def extractor(self):
		'''
		To be defined in a sub class
		'''	
		return



	def randomgen(self, listRef, tr) :
		'''
		Generate indicators for the training and test documents
		
		Parameters
		----------
		listRef : listReferences
		tr : int, {1, 0, -1, -2}
			check if training or test data
		'''
		nbRef = listRef.nbReference()
		
		for i in range(nbRef) :
			if tr == 1 : #if training data indicator for training (1)
				listRef.modifyTrainIndiceRef(i)
			else : #if not, indicator for test (0)
				listRef.modifyTestIndiceRef(i)

		return
	


	def loadIndices(self, fichier):
		'''
		Load the indices of the File object
		'''
		indices = []
		for line in open(fichier):
			indices.append(line)
			
		return indices
	


	def _printdata(self, fichier, listRef, tr, opt="saveNegatives") : #default value of 'opt' is "saveNegatives"
		'''
		Print training or test data for CRF
		'''
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			if not (opt=="deleteNegatives" and reference.train == -1) :
			
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
							try:
								fich.write(" "+unicode(caracteristique.nom.upper(), "utf-8"))
							except TypeError:
								fich.write(" "+caracteristique.nom.upper())
						
							while cpt < nbCarac-1:
								caracteristique = mot.getFeatureIndice(cpt)
								try:
									fich.write(" "+caracteristique.nom.upper())
								except:
									fich.write(" "+unicode(caracteristique.nom.upper(), "utf-8"))
								cpt += 1
						if tr != 0:
							for balise in mot.getAllTag():
								try:
									fich.write(" "+unicode(balise.nom, "utf-8"))
								except:
									fich.write(" "+balise.nom)
						fich.write("\n")
				fich.write("\n")
			#--------
		fich.close()
		return
	


	def _printOnlyLabel(self, fichier, listRef) :
		'''
		Print training or test data for CRF (only labels)
		'''
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			for mot in reference.getWord():

				for balise in mot.getAllTag():
					try:
						fich.write(unicode(balise.nom, "utf-8"))
					except:
						fich.write(balise.nom)
				fich.write("\n")
			fich.write("\n")
				
		fich.close()
		return
		
		
	def _print_alldata(self, fichier, listRef) :
		'''
		Print all data for SVM
		'''
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

	
	def _print_parallel(self, fichier, listRef) :
		'''
		Print result in parallel lines for SVM
		'''
		phrase = ""
		feature = ""
		cpt = 0;
		
		fich = codecs.open(fichier, "w", encoding="utf-8")
		for reference in listRef.getReferences():
			cpt=0
			for mot in reference.getWord():
				#mot.nom = self.convertToUnicode(mot.nom)

				
				for feat in mot.listNomFeature():

					feature += feat.upper()+" "
					if cpt == 0 and (feat.lower() == "initial"):
						feature += "STARTINITIAL "

				if re.search("NUMBERS", feature) != 0 and re.search("ALLNUMBERS", feature) != 0:	
					try:
						phrase += " "+unicode(mot.nom,"utf-8")
					except:
						phrase += " "+mot.nom
				cpt+=1

			print fich.write(str(reference.bibl))
			try:
				print fich.write(unicode(phrase,"utf-8")+"\n")
			except:
				print fich.write(phrase+"\n")

			try:
				print fich.write(unicode(feature,"utf-8")+"\n")
			except:
				print fich.write(feature+"\n")
			
			fich.write("\n")
			
			feature = ""
			phrase = ""
			cpt+=1
				
		fich.close()
		return
	
	

	def _addlayout(self, listRef) :
		'''
		Add layout features
		'''	
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
		'''
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
		'''	
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
		

	def _checkTag(self, mot):
		'''
		Modify tags according to the configuration in the file "balise.txt"
		'''	
		balises = mot.getAllTag()
		
		for balise in balises:
			if self.configTag.has_key(balise.nom):
				balise.nom = self.configTag[balise.nom]
		return
		

	def _updateTag(self, mot):
		'''
		Modify tags according to the configuration and rules
		'''
		balise = mot.getLastTag()
		if balise != -1:
			nameTag = balise.nom
			self._checkTag(mot)
					
			if nameTag == 'title':
				self.titleAttr = self._extract_title(mot, self.relatItm, self.titleCK, self.titleAttr)
				if mot.getLastTag().nom == 'title' : self.titleCK = 1
	
			#bookindicator
			'if the tag is one of noLabel and the word is one of regles, add the corresponding nameRegle tag(bookindicator)'
			for nameRegle in self.regles:
				if nameTag == 'nolabel' and  (self.regles[nameRegle].has_key(mot.nom.lower())) :
					mot.delAllTag()
					mot.addTag(nameRegle)
			
			#check <date> label for newly updated "publicationDate" attribute
			if nameTag == 'biblscope' :
				if mot.getFeature('publicationDate') != -1:
					mot.delAllTag()
					mot.addTag('date')
				

	def _checkNonLabels(self, mot):
		'''
		Keep the best tag of the word and verify if it appears in nonLabels
		'''
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
			
			

	def extractorIndices(self, svmprediction_trainfile, listRef):
		'''
		Extract indices for nonbibls from SVM classification result
		then modify 'train' attribute of each reference
		
		Parameters
		----------
		svmprediction_trainfile : string
			SVM classification result for training data
		listRef : list
			reference list
		'''
		nbRef = listRef.nbReference()
		
		svm_train = []
		for line in open (svmprediction_trainfile, 'r') :
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
	

	def extractorIndices4new(self, svmprediction_newfile, listRef):
		'''
		Extract indices for nonbibls from SVM classification result
		then modify 'train' attribute of each reference
		
		Parameters
		----------
		svmprediction_newfile : string
			SVM classification result for test data
		listRef : list
			reference list
		'''
		i = 0
		
		for line in open (svmprediction_newfile, 'r') :
			line = line.split()
			if float(line[0]) > 0 :
				listRef.getReferencesIndice(i).train = 0
			else :
				listRef.getReferencesIndice(i).train = -1
			i += 1
		return


	def convertToUnicode(self, chaine):
		'''
		Convert a string to unicode
		'''
		try:
			if isinstance(chaine, str):
				chaine = unicode(chaine, sys.stdin.encoding)
		except:
			try:
				chaine = unicode(chaine, 'ascii')
			except:
				pass

		return chaine
