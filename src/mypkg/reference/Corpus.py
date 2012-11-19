# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''
from mypkg.reference.File import File
from bs4 import BeautifulSoup
import os.path
import commands

class Corpus(object):
	'''
	A corpus containing a set of training (or test) references.
	Creation of File objects
	'''

	def __init__(self, directory):
		'''
		Attributes
		----------
		directory : string
			directory where the corpus data is (xml files)
		fichiers : list
			list of File objects containing corpus data
		'''
		self.directory = directory
		self.fichiers = []
		
		

	def getFiles(self):
		'''
		Extract file names from the directory
		'''
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
	
	

	def extract(self, type, tag, nomFichiers="", external=0):
		'''
		Extract references for each file 
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		tag : string, {"bibl", "note"}
			tag name defining reference types
			"bibl" : corpus 1, "note" : corpus 2
		nomFichier : string
			target file name for extraction
		'''
		if nomFichiers == "":
			nomFichiers = self.getFiles()
			
		for nomFichier in nomFichiers:
			fichObj = File(self.directory+"/"+nomFichier)
			fichObj.extract(type, tag, external)
			self.fichiers.append(fichObj)
			
	

	def getListReferences(self, typeCorpus):
		'''
		Return reference list in the corpus
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		'''
		allReferences = []
			
		for fichier in self.fichiers:
			listRef = fichier.getListReferences(typeCorpus)
					
			if listRef != -1:
				allReferences.extend(listRef.getReferences())
		return allReferences
		
	
	def nbReference(self, typeCorpus):
		'''
		Return number of references in the corpus
		'''
		nb = 0
		
		for fichier in self.fichiers:
				nb += fichier.nbReference(typeCorpus)
		
		return nb



	def addTagReferences(self, dirResult, fname, tagDelimRef, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
		'''
		Add ignored tags from initial file
		Check the SVM classification result of reference to give <nonbibl> tag at the final construction
		Call File::buildReferences for the modification and punctuation management then print the result
		
		Parameters
		----------
		dirResult : string
			directory for output files
		fname : string
			output filename
		tagDelimRef : 
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		refsAfterSVM : list
		'''
		tmp_str = ""
		reference = []
		fileRes = dirResult+fname
		for line in open (fileRes, 'r') :
			tmp_str = tmp_str + ' ' + line
				
		soup = BeautifulSoup (tmp_str)
		s = soup.findAll ("bibl")
		
		cpt = 0
		for fichier in self.fichiers: # Original data
			nbRefFile = fichier.nbReference(typeCorpus)
			reference[:] = []
			cptRef = 0
						
			for ref in s:
				if cptRef < nbRefFile:
					
					if len(refsAfterSVM) > 0 and refsAfterSVM[cpt].train == -1 :	#if the note (now tagged as <bibl>) is classified non-bibl
							for tag in (s[cpt]).findAll(True) :
								tag.replaceWith(tag.renderContents())

							s2 = BeautifulSoup()	#prepare tag sets <bibl><nonbibl></nonbibl></bibl>
							tag1 = s2.new_tag("bibl")
							tag2 = s2.new_tag("nonbibl")
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
			
			fichier.buildReferences(reference, tagDelimRef, typeCorpus, dirResult) #new result printing
		
		
		return
	
	
	def deleteAllFiles(self):
		'''
		delete all files in File object
		'''
		self.fichiers[:] = []
		