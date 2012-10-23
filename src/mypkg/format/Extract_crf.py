# -*- coding: utf-8 -*-
'''
Created on 11 juin 2012

@author: Young-Min Kim, Jade Tavernier
'''
from mypkg.format.Extract import Extract

class Extract_crf(Extract):
	'''
	A class to extract training and test data for CRF
	Sub class of Extract
	'''

	def __init__(self):
		Extract.__init__(self)
		

	def extractor (self, typeCorpus, ndocs, fileRes, listRef, tr=-1, extOption=-1) :
		'''
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
		'''	
		self.titleCK = 0
		self.titleAttr = ''
		self.relatItm = 0
			
		i = 0
		check = -5
		nonbiblck = 1
		
		listReferences = listRef.getReferences()
		tmp_nonbiblck = 0
		
		for reference in listReferences:
			#This is an indicator if the reference has been classified in the negative class by SVM
			if reference.train == -1 : 
				pass # HERE You should eliminate reference.... or Eliminate at the printing moment
			
			
			for mot in reference.getWord():

				
				if mot.ignoreWord == 0:
					if mot.item == 1: self.relatItm = 1
					
					if tr == 1 : check = 1
					else : check = 0
					
					
					'''
					reference.train is a note indicator to see if it is classified nonbibl from SVM classification
					'''
					if reference.train == -1:
						mot.delAllTag()
						mot.addTag("nonbibl")
						pass
					
					elif reference.train == check:

						#label check
						self._updateTag(mot)
						
						#nobibl check,
						tmp_nonbiblck = 0
						for tmp in mot.getAllTag() :

							if tmp.nom == "nonbibl" :
								tmp_nonbiblck = 1
							elif tmp.nom == 'c' and typeCorpus == 2 and extOption==-1 :
								if nonbiblck == 1:
									tmp_nonbiblck = 1
									
						if tmp_nonbiblck == 1 : 
							#if (extOption!=-1) :
							mot.delAllTag()
							mot.addTag("nonbibl")
	
						if tr == 0 :
							mot.delAllTag() # It is not really necessary because in Printing, we check the 'tr'
					
						'delete all features out of the "features" list'
						supp = []
						'si c est de la ponctuation on enleve toutes les caracteristiques'
						balise = mot.getLastTag()
						if balise != -1:
							if balise.nom == "c" :
								if typeCorpus == 2 and extOption==-1 : # in case of SVM data, add PUNC
									mot.delAllFeature()
									mot.addFeature("PUNC")
								else :
									mot.delAllFeature()
						
						for carac in mot.getAllFeature():
							if not self.features.has_key(carac.nom.lower()):
								supp.append(carac.nom)
								
						for nomMot in supp:
							mot.delFeature(nomMot)
							
						if tmp_nonbiblck == 0 : nonbiblck = 0
				
						# finding just a label which is not in the nonLabels list
						self._checkNonLabels(mot)
				
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
		
		if extOption == 1 or extOption == 2 :
			if tr != -2 :
				self._addlayout(listRef)					####### add layout features ### 2012-02-01 ###
				if tr != 1 :
					self._printdata(fileRes, listRef, tr)
				else :
					self._printdata(fileRes+"Original", listRef, tr)
					self._printdata(fileRes, listRef, tr, "deleteNegatives")
			else:
				self._printOnlyLabel(fileRes, listRef)
			
		elif extOption == 3 or extOption == 4 or extOption == 5 or extOption == 6:
			self._printmoreFeatures(extOption) # !!!!! not yet coded !!!!!
		
		if typeCorpus == 2:
			'''if tr == 1:
				self._print_alldata(fileRes, listRef)
			else :'''
			
			self._print_parallel(fileRes, listRef)
				
		return