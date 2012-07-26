# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''
import subprocess
import os.path
import commands
from mypkg.reference.File import File
from mypkg.ressources.BeautifulSoup import BeautifulSoup, Tag

class Corpus(object):
	'''
	classdocs
	'''


	def __init__(self, repertoire):
		'''
		Constructor
		'''
		self.repertoire = repertoire
		self.fichiers = []
		
	'''
	 : recupere le nom de tous les fichiers present dans le repertoire
	'''
	def getFiles(self):
		'regarde si c est un repertoire ou un fichier seul'
		if os.path.isdir(self.repertoire):
			lsOut = commands.getoutput('ls '+self.repertoire)
			listFichiers = lsOut.split("\n")

		else:
			nomSplit = self.repertoire.split("/")
			listFichiers = []
			listFichiers.append(nomSplit[len(nomSplit)-1])
			del nomSplit[len(nomSplit)-1]
			self.repertoire = "/".join(nomSplit)
		return listFichiers
	
	
	'''
	extract pour chaque fichier les references 
	argument :
		type :			type de corpus : 1 = corpus1, 2 = corpus 2 ...
		tag :			balise delimitant les references : corpus 1 = bibl...
		nomFichier :	nom du fichier que l'on doit annoter
	'''
	def extract(self, type, tag, nomFichiers=""):
		if nomFichiers == "":
			nomFichiers = self.getFiles()
			
		for nomFichier in nomFichiers:
			fichObj = File(self.repertoire+"/"+nomFichier)
			fichObj.extract(type, tag)
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
	addTagReferences : ajoute les balises ignorees du fichier initial
	'''
	def addTagReferences(self, fileRes, tagDelimRef, typeCorpus):
		tmp_str = ""
		reference = []
		for line in open (fileRes, 'r') :
			tmp_str = tmp_str + ' ' + line
				
		soup = BeautifulSoup (tmp_str)		
		s = soup.findAll ("bibl")
		
		cpt = 0
	
		for fichier in self.fichiers:
			nbRefFile = fichier.nbReference(typeCorpus)
			reference[:] = []
			cptRef = 0
			
			for ref in s:
				if cptRef < nbRefFile:
					reference.append(s[cpt])
				else:
					break
				cptRef += 1
				cpt += 1

			#fichier.addTagReferences(reference)
			fichier.buildReferences(reference, tagDelimRef, typeCorpus)
		return
	
	def deleteAllFiles(self):
		self.fichiers[:] = []