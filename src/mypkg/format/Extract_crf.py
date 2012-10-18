# -*- coding: utf-8 -*-
'''
Created on 11 juin 2012

@author: Young-Min Kim, Jade Tavernier
'''
from mypkg.format.Extract import Extract

class Extract_crf(Extract):
	'''
	classdocs
	'''

	def __init__(self):
		Extract.__init__(self)
		
	'''
	extractor : extract training and test data
		ndocs : number of references
		typeCorpus : 1, 2 ou 3
		tr : indicator check, it gives the valid instance indices 
		extr : 
		fileRes = nom du fichier sortie du resultat
	'''
	def extractor (self, typeCorpus, ndocs, fileRes, listRef, tr=-1, extOption=-1) :
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
					A PROBLEM !!!!!!!!!! IF train == -1 we should delete the reference in training. In test also....
					ANYWAY we need to CHANGE TAG for XML construction
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
								if typeCorpus == 2 and extOption==-1 :
									mot.delAllFeature()
									mot.addFeature("PUNC")
									'sinon on enleve que celle non presente dans les features'
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
				self._printdata(fileRes, listRef, tr)
				#self._printdata(fileRes+"Original", listRef, tr)
				#self._printdata(fileRes, listRef, tr, "deleteNegatives")
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