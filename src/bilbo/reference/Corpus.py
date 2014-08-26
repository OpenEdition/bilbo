# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.reference.File import File
from bilbo.output.identifier import teiValidate
from bs4 import BeautifulSoup
from codecs import open
import os.path
import commands

class Corpus(object):
	"""
	A corpus containing a set of training (or test) references.
	Creation of File objects
	"""

	def __init__(self, directory, options):
		"""
		Attributes
		----------
		directory : string
			directory where the corpus data is (xml files)
		fichiers : list
			list of File objects containing corpus data
		"""
		self.directory = directory
		self.fichiers = []
		self.options = options
		
		

	def getFiles(self):
		"""
		Extract file names from the directory
		"""
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
		
		if self.options.v in ['input', 'all'] : listFichiers = self.validateXml(listFichiers)
		return listFichiers
	
	
	def validateXml(self, listFichiers):
		
		newList = []
		for filename in listFichiers :
			try : 
				valide, numErr = teiValidate(os.path.join(self.directory, filename), 'input')
			except Exception, error :
				valide = False
				print filename
				print "Can't even try validation", error
				pass
			if valide : newList.append(filename)
		
		print "valide files"
		for f in newList : print f
		
		return newList
	

	def extract(self, type, tag, nomFichiers="", external=0):
		"""
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
		"""
		if nomFichiers == "":
			nomFichiers = self.getFiles()
			
		for nomFichier in nomFichiers:
			fichObj = File(self.directory+"/"+nomFichier, self.options)
			fichObj.extract(type, tag, external)
			self.fichiers.append(fichObj)
	

	def getListReferences(self, typeCorpus):
		"""
		Return reference list in the corpus
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		"""
		allReferences = []
			
		for fichier in self.fichiers:
			listRef = fichier.getListReferences(typeCorpus)
			if listRef != -1:
				allReferences.extend(listRef.getReferences())
		return allReferences
		
	
	def nbReference(self, typeCorpus):
		"""
		Return number of references in the corpus
		"""
		nb = 0
		for fichier in self.fichiers:
			nb += fichier.nbReference(typeCorpus)
		return nb



	def addTagReferences(self, dirResult, fname, tagTypeCorpus, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
		"""
		Add ignored tags from initial file
		Check the SVM classification result of reference to give <nonbibl> tag at the final construction
		Call File::buildReferences for the modification and punctuation management then print the result
		
		Parameters
		----------
		dirResult : string
			directory for output files
		fname : string
			output filename
		tagTypeCorpus : 
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		refsAfterSVM : list
		"""
		tmp_str = ""
		references = []
		fileRes = dirResult+fname
		for line in open (fileRes, 'r', encoding='utf8') :
			tmp_str = tmp_str + ' ' + line
		
		soup = BeautifulSoup (tmp_str)
		s = soup.findAll ("bibl")
		
		cpt = 0 #total reference count
		for fichier in self.fichiers: # Original data
			nbRefFile = fichier.nbReference(typeCorpus)
			references[:] = []
			cptRef = 0 # reference count in the file
			for ref in s:
				if cptRef < nbRefFile:
					if len(refsAfterSVM) > 0 and refsAfterSVM[cpt].train == -1 : #if the note (now tagged as <bibl>) is classified non-bibl
							for tag in (s[cpt]).findAll(True) :
								tag.replaceWith(tag.renderContents())
							s2 = BeautifulSoup() #prepare tag sets <bibl><nonbibl></nonbibl></bibl>
							tag1 = s2.new_tag("bibl")
							tag2 = s2.new_tag("nonbibl")
							s2.insert(0, tag1)
							tag1.insert(0, tag2)
							tag2.insert(0, s[cpt].renderContents()) #put the unwrapped contents in the middle of above tag sets
							references.append(s2.find("bibl")) #make s2 have found bibl
					else :
						references.append(s[cpt])
				else:
					break
				cptRef += 1
				cpt += 1
			
			'Build references in the original files and save them the root of dirResult'
			dirResultRoot = os.path.abspath(os.path.join(dirResult, os.path.pardir))+'/'
			fichier.buildReferences(references, tagTypeCorpus, dirResultRoot) #new result printing
			
		return
	
	
	def deleteAllFiles(self):
		"""
		delete all files in File object
		"""
		self.fichiers[:] = []
		