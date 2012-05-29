'''
Created on 25 avr. 2012

@author: jade
'''
import subprocess
import os.path
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
			process = subprocess.Popen('ls '+self.repertoire, shell=True, stdout=subprocess.PIPE)
			process.wait()
			fichiers = process.stdout.read()
			listFichiers = fichiers.split("\n")
			del(listFichiers[len(listFichiers)-1])
		else:
			nomSplit = self.repertoire.split("/")
			listFichiers = []
			listFichiers.append(nomSplit[len(nomSplit)-1])
			del nomSplit[len(nomSplit)-1]
			self.repertoire = "/".join(nomSplit)
		return listFichiers
	
	'''
	extractCorpus1 pour chaque fichier les references du corpus 1
	'''
	def extractCorpus1(self):

		nomFichiers = self.getFiles()
		for nomFichier in nomFichiers:
			fichObj = File(self.repertoire+"/"+nomFichier)
			fichObj.extractCorpus1()
			self.fichiers.append(fichObj)
		
	'''
	extractCorpus2 pour chaque fichier les references du corpus 1
	'''
	def extractCorpus2(self):

		nomFichiers = self.getFiles()
		for nomFichier in nomFichiers:
			fichObj = File(self.repertoire+"/"+nomFichier)
			fichObj.extractCorpus2()
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

	def buildAnnotateFiles(self):
		for fichier in self.fichiers:
			fichier.buildAnnotateFile(1, "bibl")
		return
	
	def addTagReferences(self, fileRes):
		tmp_str = ""
		for line in open (fileRes, 'r') :
			tmp_str = tmp_str + ' ' + line
				
		soup = BeautifulSoup (tmp_str)		
		s = soup.findAll ("bibl")
		
		cpt = 0
	
		for fichier in self.fichiers:
			nbRefFile = fichier.nbReference(1)
			reference = []
			cptRef = cpt
			
			for ref in s:
				if cptRef < nbRefFile:
					reference.append(ref)
				else:
					break
				cptRef += 1

			fichier.addTagReferences(reference)
		return