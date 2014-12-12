# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on June 11, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.format.Extract import Extract

chPunc =  {'.':0, ',':0, ')':0,'”':0, '}':0, ']':0, '(':0, '“':0, '{':0, '[':0, '«':0, '»':0, '“':0, '”':0, '"':0}
chFeat4title = ["a","m","j","s","u","volume_title", "translated_title", "research_programm" ]

class Extract_crf(Extract):
	"""
	A class to extract training and test data for CRF
	Sub class of Extract
	"""

	def __init__(self, options={}):
		Extract.__init__(self, options)


	def extract (self, typeCorpus, ndocs, fileRes, listRef, tr=-1, extOption=-1) :
		"""
		Extract training and test data

		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		ndocs : int
			number of references
		fileRes : string
			output file name
		listRef : listReferences
			reference list
		tr : int, {1, 0, -1, -2}
			check if training or test data
		extOption : int, {-1, 1, ...} (default -1)
			extra option for crf training/test data format
			check if data is internal data, if yes we'll use a modified index for corpus type 2
			-1 : data format for SVM
			1 : data format for normal CRF training/test data
			2-5 : (not yet provided)
		"""
		self.titleCK = 0
		self.titleAttr = ''
		self.relatItm = 0
			
		i = 0
		nonbiblck = 1
		listReferences = listRef.getReferences()
		tmp_nonbiblck = 0
		
		for reference in listReferences:
			#reference.affiche()
			'This is an indicator if the reference has been classified in the negative class by SVM'
			if reference.train == -1 : # -1 : classified as nonbibl, 1 : normal training data, 0 : normal test data
				pass
			
			for mot in reference.getWord():

				if mot.ignoreWord == 0:
					if mot.item == 1: self.relatItm = 1
					
					"""
					reference.train is a note indicator to see if it has been classified nonbibl from SVM classification
					But to print original tags of test data, we should not change tags as "nonbibl"
					Notes classified as nonbibl will be eliminated at printing
					"""
					#label check
					if self.options.i == 'tei' : self._updateTag(mot)
						
					#nobibl check,
					tmp_nonbiblck = 0
					for tmp in mot.getAllTag() :
						if tmp.nom == "nonbibl" :
							tmp_nonbiblck = 1
						elif tmp.nom == 'c' and typeCorpus == 2 and extOption==-1 :
							if nonbiblck == 1:
								tmp_nonbiblck = 1
									
					if tmp_nonbiblck == 1 :
						mot.delAllTag()
						mot.addTag("nonbibl")
	
					if tr == 0 :
						mot.delAllTag() # It is not really necessary because in Printing, we check the 'tr'
					
					'delete all features out of the "features" list'
					supp = []
					
					if chPunc.has_key(mot.nom) : #Instead of checking tag, check directly word for new document
						if typeCorpus == 2 and extOption==-1 : #in case of SVM data, add PUNC feature
							mot.delAllFeature()
							mot.addFeature("PUNC")
					
					'detailed punctuation feature <- for experiments, not used for the moment'
					if mot.getTag('c') != -1 :
						for carac in mot.getAllFeature():
							if not carac.nom.lower() in ['punc', 'point', 'comma', 'leadingquotes', 'endingquotes', 'link', 'pairedbraces'] :
								mot.delFeature(carac.nom)
					
					for carac in mot.getAllFeature():
						if not self.features.has_key(carac.nom.lower()) :
							if extOption != -1 or not (carac.nom.lower() in chFeat4title) :
								supp.append(carac.nom)
						
					for nomMot in supp :
						mot.delFeature(nomMot)
							
					if tmp_nonbiblck == 0 : nonbiblck = 0
				
					# finding just a label which is not in the nonLabels list
					if self.options.i == 'tei' : self._checkNonLabels(mot)
				
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
			pass
			#self.nameObj.searchName(listRef, tr)
			#self.placeObj.searchPlace(listRef, tr)
			#self.cityObj.searchProper(listRef, tr)
			#self.journalObj.searchProper(listRef, tr)
		
		if extOption == 1 or extOption == 2 :
			if tr != -2 :
				self._addlayout(listRef)	#Layout feature added
				if tr != 1 or not self.options.s:
					self._printdata(fileRes, listRef, tr)
					fileResWapiti = fileRes.replace(".txt", "_Wapiti.txt")
					self._printdataWapiti(fileResWapiti, listRef, tr)
				else :
					if self.options.s : #if svm classification on
						fileResOri = fileRes.replace(".txt", "_Original.txt")
						self._printdata(fileResOri, listRef, tr)
						fileResWapiti = fileRes.replace(".txt", "_OriginalWapiti.txt")
						self._printdataWapiti(fileResWapiti, listRef, tr)
						fileResWapiti = fileRes.replace(".txt", "_Wapiti.txt")
						self._printdataWapiti(fileResWapiti, listRef, tr, "deleteNegatives")
						self._printdata(fileRes, listRef, tr, "deleteNegatives")
			else:
				self._printOnlyLabel(fileRes, listRef)
			
		elif extOption == 3 or extOption == 4 or extOption == 5 or extOption == 6:
			self._printmoreFeatures(extOption) # !!!!! not yet coded !!!!!
		
		if typeCorpus == 2 and extOption==-1 :
			self._print_parallel(fileRes, listRef)
				
		return
