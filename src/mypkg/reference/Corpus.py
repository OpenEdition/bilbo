# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''

import os.path
import commands
from mypkg.reference.File import File
from mypkg.ressources.BeautifulSoup import BeautifulSoup, Tag



class Corpus(object):
	'''
	classdocs
	'''


	def __init__(self, directory):
		'''
		Constructor
		'''
		self.directory = directory
		self.fichiers = []
		
		
	'''
	 : Extract file names in the directory
	'''
	def getFiles(self):
		'Verify if it is a directory or a single file'
		if os.path.isdir(self.directory):
			lsOut = commands.getoutput('ls '+self.directory)
			listFichiers = lsOut.split("\n")

		else:
			nomSplit = self.directory.split("/")
			listFichiers = []
			listFichiers.append(nomSplit[len(nomSplit)-1])
			del nomSplit[len(nomSplit)-1]
			self.directory = "/".join(nomSplit)
		return listFichiers
	
	
	'''
	Extract the references for each file 
	argument :
		type :			corpus type : 1 = corpus1, 2 = corpus 2 ...
		tag :			tag name defining the reference types : corpus 1 = bibl...
		nomFichier :	nom du fichier que l'on doit annoter
	'''
	def extract(self, type, tag, nomFichiers="", external=0):
		if nomFichiers == "":
			nomFichiers = self.getFiles()
			
		for nomFichier in nomFichiers:
			fichObj = File(self.directory+"/"+nomFichier)
			fichObj.extract(type, tag, external)
			self.fichiers.append(fichObj)
			
	
	'''
	getListReferences : permet de recuperer la liste entiere des references du corpus 1
	'''
	def getListReferences(self, typeCorpus):
			allReferences = []
			
			for fichier in self.fichiers:
				listRef = fichier.getListReferences(typeCorpus)
					
				if listRef != -1:
					allReferences.extend(listRef.getReferences())
			return allReferences
		
	
	def nbReference(self, typeCorpus):
		nb = 0
		
		for fichier in self.fichiers:
				nb += fichier.nbReference(typeCorpus)
		
		return nb


	'''
	addTagReferences :	Add ignored tags from initial file
						Check the SVM classification result of reference to give <nonbibl> tag at the final construction
						Call 'buildReferences' method of 'File' class for these modifications and punctuation management.
												
	'''
	def addTagReferences(self, fileRes, tagDelimRef, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
		tmp_str = ""
		reference = []
		for line in open (fileRes, 'r') :
			tmp_str = tmp_str + ' ' + line
				
		soup = BeautifulSoup (tmp_str)
		s = soup.findAll ("bibl")
		
		cpt = 0
		for fichier in self.fichiers: # Original data
			nbRefFile = fichier.nbReference(typeCorpus)
			reference[:] = []
			cptRef = 0
			
			#VALID_TAGS = ['bibl']
			VALID_TAGS = []
						
			for ref in s:
				if cptRef < nbRefFile:
					
					if len(refsAfterSVM) > 0 and refsAfterSVM[cpt].train == -1 :	#if the note (now tagged as <bibl>) is classified non-bibl

							for tag in (s[cpt]).findAll(True) :
								if tag.name not in VALID_TAGS :
									tag.replaceWith(tag.renderContents())

							s2 = BeautifulSoup()	#prepare tag sets <bibl><nonbibl></nonbibl></bibl>
							tag1 = Tag(s2, "bibl")
							tag2 = Tag(s2, "nonbibl")
							s2.insert(0, tag1)
							tag1.insert(0, tag2)
							tag2.insert(0, s[cpt].renderContents()) #put the unwrapped contents in the middle of above tag sets

							reference.append(s2.find("bibl")) #make s2 have found bibl
							
					else :
						reference.append(s[cpt])
				else:
					break
				cptRef += 1
				cpt += 1

			fichier.buildReferences(reference, tagDelimRef, typeCorpus) #new result printing
		return
	
	
	def deleteAllFiles(self):
		self.fichiers[:] = []
		