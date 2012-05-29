'''
Created on 25 avr. 2012

@author: jade
'''
from mypkg.format.CleanCorpus1 import CleanCorpus1
from mypkg.format.CleanCorpus2 import CleanCorpus2
from mypkg.format.Rule import Rule
from mypkg.reference.ListReferences import ListReferences
from mypkg.ressources.BeautifulSoup import *
import re

class File(object):
	'''
	classdocs
	'''


	def __init__(self, fname):
		'''
		Constructor
		'''
		self.nom = fname
		self.corpus = {}
	
	'''
	extraireCorpus1 : extrait les references du fichier correspondant au corpus 1
	'''
	def extractCorpus1(self):
		clean = CleanCorpus1()
		references = clean.processing(self.nom, "bibl")
		if len(references) >= 1:
			self.corpus[1] = ListReferences(references, 1)
			
			rule = Rule()
			rule.reorganizing(self.corpus[1])
		
		
	'''
	extraireCorpus2 : extrait les references du fichier correspondant au corpus 1
	'''
	def extractCorpus2(self):
		clean = CleanCorpus2()
		references = clean.processing(self.nom, "note")#, "bibl")
		if len(references) >= 1:
			self.corpus[2] = ListReferences(references, 2)
			
			rule = Rule()
			rule.reorganizing(self.corpus[2])
		
	'''
	getListReferences : permet de recuperer la liste entiere des references du corpus 1
	typeCorpus : int numero du corpus
	'''
	def getListReferences(self, typeCorpus):
		try:
			return self.corpus[typeCorpus]
			
		except :
			return -1
		
	'''
	calcul le nombre de reference
	'''
	def nbReference(self, typeCorpus):
		try:
			return self.corpus[typeCorpus].nbReference()
			
		except :
			return 0
	
	'''
	construit le fichier entier annote
	'''	
	def buildAnnotateFile(self, typeCorus, tagTypeCorpus):#, dirOut):
		tmp_str_ori = ""
		tmp_str = ""
		ref_item = ""
		nbItem = 0
		
		for line in open (self.nom, 'r') :
			tmp_str_ori = tmp_str_ori + ' ' + line
			line = line.replace('&amp;', '&')
			tmp_str = tmp_str + ' ' + line
				
		tmp_str = tmp_str.decode('utf8')
		tmp_str = self._html2unicode(tmp_str)
		soup = BeautifulSoup (tmp_str)
		soup_ori = BeautifulSoup (tmp_str_ori)
		
		
		s = soup.findAll (tagTypeCorpus)
		s_ori = soup.findAll (tagTypeCorpus)
		
		i = 0
		for ref_ori in s_ori:
			if i == 642:
				pass
			try:
				if i < len(s_ori):
					if ref_ori["type"] != "head":
						ref = s[i]
						
						ref_annote = self.getListReferences(typeCorus).getReferences()[i-nbItem]
						if ref.find('relateditem') :
							i += 1
							nbItem += 1
							
						self.modifTagInRef(ref, ref_annote, soup)
					i += 1
			except KeyError:
				ref = s[i]
				
				ref_annote = self.getListReferences(typeCorus).getReferences()[i-nbItem]
				
				if ref.find('relateditem') :
					i += 1
					nbItem += 1
				
				self.modifTagInRef(ref, ref_annote, soup)
				i += 1
		
		fich = open("Result/res.xml", "w")
		fich.write(soup.prettify())
	'''
	modiftagInRef : ajoute au fichier final les balises pour chaque mots
	'''		
	def modifTagInRef(self, ref, ref_annote, soup):
		ref_annote_end = ""
		ref.contents = []
		flagItem = 0
		
		balise = ""
		chaine = ""

		cptWord = 0
		cptTag = 0
		for word in ref_annote.getWord():
			'if il y a une sous reference'
			if word.item == 1:
				flagItem = 1
				ref.append("<relatedItem type=\"in\">")
			'if le mot ne fait pas partie d une balise du fichier original'
			if ref_annote.getWordIndice(cptWord).ignoreWord == 0:
				if balise == ref_annote.getWordIndice(cptWord).getTagIndice(0).nom:
					chaine += " "+word.nom
				elif balise == "":
					balise = ref_annote.getWordIndice(cptWord).getTagIndice(0).nom
					chaine = word.nom
					cptTag += 1
				else:
					refTag = Tag(soup, balise)
					chaine = chaine.replace('&amp;', '&')
					text = NavigableString(chaine)
					refTag.insert(0,text)
					ref.append(refTag)
					
					balise = ref_annote.getWordIndice(cptWord).getTagIndice(0).nom
					chaine = word.nom
					cptTag += 1
					#ref.contents.newTag(balise, chaine)
			else:
				if balise != "":
					refTag = Tag(soup, balise)
					chaine = chaine.replace('&amp;', '&')
					text = NavigableString(chaine)
					refTag.insert(0,text)
					ref.append(refTag)
					
					balise = ""
					chaine = ""
					cptTag += 1
					
					ref.append(word.nom)
				else:
					ref.append(word.nom)	
			cptWord += 1
			
		'ajoute la derniere balise et chaine '
		if chaine != "":
			refTag = Tag(soup, balise)
			chaine = chaine.replace('&amp;', '&')
			text = NavigableString(chaine)
			refTag.insert(0,text)
			ref.append(refTag)	
			
		if flagItem == 1:
			ref.append("</relatedItem>")
		'''
		balise = ""
		chaine = ""
		cptWord = 0
		'verifier si il y a un item'
		if ref_item != "":
			ref.append("<relatedItem type=\"in\">")
			for word in ref_annote.getWord():
				'if le mot ne fait pas partie d une balise du fichier original'
				if ref_annote.getWordIndice(cptWord).ignoreWord == 0:
					if balise == ref_annote.getWordIndice(cptWord).getTagIndice(0).nom:
						chaine += " "+word.nom
					elif balise == "":
						balise = ref_annote.getWordIndice(cptWord).getTagIndice(0).nom
						chaine = word.nom
						cptTag += 1
					else:
						refTag = Tag(soup, balise)
						chaine = chaine.replace('&amp;', '&')
						text = NavigableString(chaine)
						refTag.insert(0,text)
						ref.append(refTag)
						
						balise = ref_annote.getWordIndice(cptWord).getTagIndice(0).nom
						chaine = word.nom
						cptTag += 1
						#ref.contents.newTag(balise, chaine)
				else:
					if balise != "":
						refTag = Tag(soup, balise)
						chaine = chaine.replace('&amp;', '&')
						text = NavigableString(chaine)
						refTag.insert(0,text)
						ref.append(refTag)
						
						balise = ""
						chaine = ""
						cptTag += 1
						
						ref.append(word.nom)
					else:
						ref.append(word.nom)	
				cptWord += 1
			
			'ajoute la derniere balise et chaine '
			if chaine != "":
				refTag = Tag(soup, balise)
				chaine = chaine.replace('&amp;', '&')
				text = NavigableString(chaine)
				refTag.insert(0,text)
				ref.append(refTag)	
			ref.append("</relatedItem>")
		'''
					
	def _html2unicode(self, tmp_str) :
		#for numerical codes
		matches = re.findall("&#\d+;", tmp_str)
		if len(matches) > 0 :
			hits = set(matches)
			for hit in hits :
				name = hit[2:-1]
				try :
					entnum = int(name)
					tmp_str = tmp_str.replace(hit, unichr(entnum))
				except ValueError:
					pass
	
		#for hex codes
		matches = re.findall("&#[xX][0-9a-fA-F]+;", tmp_str)
		if len(matches) > 0 :
			hits = set(matches)
			for hit in hits :
				hex = hit[3:-1]
				try :
					entnum = int(hex, 16)
					tmp_str = tmp_str.replace(hit, unichr(entnum))
				except ValueError:
					pass
		
		tmp_str = tmp_str.replace('&','&amp;')
		
		return tmp_str

	'''
	addTagReferences : ajoute aux objets reference les balises trouve par Bilbo
	'''
	def addTagReferences(self, references):
		cptWord = 0
		cptRef = 0
		for ref in references:
			cptWord = 0
			allTag = ref.findAll(True)
			
			for tag in allTag:
				content = tag.contents
				words = re.split("\s", content[0])
				for word in words:
					if word != "":
						while self.corpus[1].getReferencesIndice(cptRef).getWordIndice(cptWord).ignoreWord == 1:
							cptWord += 1
						self.corpus[1].getReferencesIndice(cptRef).getWordIndice(cptWord).addTag(tag.name)
						cptWord += 1
						
			cptRef += 1	
			
		return
	'''
	getName : retourne le nom du fichier sns le chemin complte
	'''
	'''def _getName(self):
		'''