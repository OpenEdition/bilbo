# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''
from bs4 import BeautifulSoup, NavigableString
from mypkg.format.Clean import Clean
from mypkg.format.CleanCorpus1 import CleanCorpus1
from mypkg.format.CleanCorpus2 import CleanCorpus2
from mypkg.format.Rule import Rule
from mypkg.reference.ListReferences import ListReferences
from mypkg.output.identifier import *
import re
import sys

prePunc =  {'.':0, ',':0, ')':0, ':':0, ';':0, '-':0, '”':0, '}':0, ']':0, '!':0, '?':0, '/':0}
postPunc = {'(':0, '-':0, '“':0, '{':0, '[':0}


class File(object):
	'''
	A file class containing all references in a file
	'''

	def __init__(self, fname):
		'''
		Attributes
		----------
		nom : string
			target file name
		corpus : dictionary of reference list
			 references in the file
		'''
		self.nom = fname
		self.corpus = {}
	


	def extract(self, typeCorpus, tag, external):
		'''
		Extract references
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		tag : string, {"bibl", "note"}
			tag name defining reference types
			"bibl" : corpus 1, "note" : corpus 2
		external : int, {1, 0}
			1 : if the references are external data except CLEO, 0 : if that of CLEO
			it is used to decide whether Bilbo learn call a SVM classification or not.			
		'''	
		clean = Clean()
		if typeCorpus == 1:
			clean = CleanCorpus1()
		elif typeCorpus == 2:
			clean = CleanCorpus2()
			
		references = clean.processing(self.nom, tag, external)
		if len(references) >= 1:
			self.corpus[typeCorpus] = ListReferences(references, typeCorpus)
			
			rule = Rule()
			rule.reorganizing(self.corpus[typeCorpus])
			
			

	def getListReferences(self, typeCorpus):
		'''
		Return reference list
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		'''
		try:
			return self.corpus[typeCorpus]
		except :
			return -1
		

	def nbReference(self, typeCorpus):
		'''
		count the number of references
		'''
		try:
			return self.corpus[typeCorpus].nbReference()
			
		except :
			return 0		
	
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

	

	def buildReferences(self, references, tagTypeCorpus, typeCorpus, dirResult):
		'''
		Construct final xml output file, called from Corpus::addTagReferences
		Check if there are some ignored tags in the original file and if yes, put them in a new result
		Also eliminate <c> tags for punctuation marks and attach the marks to their previous or next token
		
		Parameters
		----------
		references : list 
			automatically annotated references by system
		tagTypeCorpus : string, {"bibl", "note"}
			tag name defining reference types
			"bibl" : corpus 1, "note" : corpus 2
				typeCorpus : int, {1, 2, 3}
		type of corpus
			1 : corpus 1, 2 : corpus 2...
		tagTypeList : string, "listbibl"
			tag name wrapping all references
		'''
		cptWord = 0		#word counter
		cptRef = 0		#reference counter
		cptItem = 0		
		tmp_str = ""
		flagItem = 0
		balise = ""
		baliseBefore = ""
		ref_finale = ""
		flagNonLabel = 0
		ref_ori = []
		
		'Read the source file to check the initial contents of references'
		for line in open (self.nom, 'r') :
			tmp_str = tmp_str + line
				
		soup = BeautifulSoup (tmp_str)
		
		'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		'!!! NOW, PROBLEM IN PROCESSING RELATED ITEMS'
		'!!! In case of new data having no manual annotation, it is OKAY because they do not have <bibl> in <bibl>'
		'!!! When note annotation, anyway it is OKAY because the <bibl>s are found in a note'
		'!!! But when related item appears more than once, we do not extract well the whole <bibl>'
		'!!! In this case already we have a problem'
		'!!! And moreover, in this new building we do not consider the existence of related item'
		'!!! when extract the original references again'
		'!!! SO TO BE MODIFIED'
		s = soup.findAll (tagTypeCorpus) #!!!!!!!!!!!!
	
	
		'Reconstruct references with the ignored tags, ex) tag hi'
		for ref in references:
			balise = ""
			baliseBefore = ""
			flagItem = 0
			ref_finale = ""
			ref_tmp = ""
			cptWord = 0	#word counter
			allTag = ref.findAll(True)
			wordInRefBeforenom = ""

			for tag in allTag:
				content = tag.contents
				words = re.split("\s", content[0])
				for word in words:
					if word != "":
						wordInRef = self.corpus[typeCorpus].getReferencesIndice(cptRef).getWordIndice(cptWord)
						if cptWord > 0 : 
							wordInRefBefore = self.corpus[typeCorpus].getReferencesIndice(cptRef).getWordIndice(cptWord-1)
							wordInRefBeforenom = wordInRefBefore.nom
						
						'convert to unicode'
						wordInRef.nom = self.convertToUnicode(wordInRef.nom)
						tag.name = self.convertToUnicode(tag.name)
						
						'Check if the word should be ignored or not : ignored = considered as having nonLabel tag for the final xml file'
						while wordInRef.ignoreWord == 1:
							if baliseBefore != "" and balise != "c":
								baliseBefore = ""
							if balise != "c" and balise != "":
								ref_finale += "</"+balise+">"
								balise = ""
							ref_finale += wordInRef.nom
							cptWord += 1
							wordInRef = self.corpus[typeCorpus].getReferencesIndice(cptRef).getWordIndice(cptWord)
							balise = ""
							wordInRef.nom = self.convertToUnicode(wordInRef.nom)
							
							
						'If there is a sub reference '
						if wordInRef.item == 1 and flagItem == 0:
							flagItem = 1
							if baliseBefore != "" and balise != "c":
								ref_finale += "</"+baliseBefore+">"
								baliseBefore = ""
							if balise != "c" and balise != "":
								ref_finale += "</"+balise+">"
								balise = ""
							ref_finale += "<relatedItem type=\"in\">"
							balise = ""								


						if balise == tag.name: #balise : until now, that is the previous tag
							if (tag.name == 'c' or tag.name == 'nonbibl') and prePunc.has_key(wordInRef.nom) :
								ref_finale += wordInRef.nom
							elif (balise == 'c' or balise == 'nonbibl') and postPunc.has_key(wordInRefBeforenom) :
								ref_finale += wordInRef.nom
							else :
								ref_finale += " "+wordInRef.nom
								
						elif balise == "":
							if tag.name != "c":
								ref_finale += " <"+tag.name+">"+wordInRef.nom
							else: #if tag.name == "c"
								ref_finale += wordInRef.nom
							balise = tag.name
						else:
							if balise != "c" and tag.name != "c":
								ref_finale += "</"+balise+">"+" <"+tag.name+">"+wordInRef.nom
							elif balise == "c" and tag.name != "c":
								if baliseBefore == tag.name: # before before of current
									ref_finale = ref_tmp
									if (postPunc.has_key(wordInRef.nom)) : ref_finale += wordInRef.nom
									else : ref_finale += ' '+wordInRef.nom
								else: # before before of current tag is different
									if (postPunc.has_key(wordInRefBeforenom)):
										ref_finale += "<"+tag.name+">"+wordInRef.nom
									else:
										ref_finale += " <"+tag.name+">"+wordInRef.nom
									baliseBefore = ""
							elif balise != "c" and tag.name == "c":
								ref_tmp = ""
								if (postPunc.has_key(wordInRef.nom)) : 
									ref_tmp = ref_finale + ' '+wordInRef.nom
									ref_finale += "</"+balise+"> "+wordInRef.nom
								else : 
									ref_tmp = ref_finale + wordInRef.nom
									ref_finale += "</"+balise+">"+wordInRef.nom
								baliseBefore = balise
							else:
								ref_finale += wordInRef.nom
							balise = tag.name

						cptWord += 1

			if balise != "c":	
				ref_finale += "</"+balise+">"
				
			'If there is a sub reference, we add a closing tag'
			if flagItem == 1:
				cptItem += 1
				if baliseBefore != "":
					ref_finale += "</"+baliseBefore+">"
					baliseBefore = ""
				else:
					ref_finale += "</"+balise+">"
				ref_finale += "</relatedItem>"	
			cptRef += 1	
			ref_ori.append(ref_finale)
			
		'delete final references that were considered as items <------ WHY??'
		while cptItem > 0:
			s.pop()
			cptItem -= 1
		
		
		try:
			cpt = 0
			listRef = soup.findAll(tagTypeCorpus)
			for ref in listRef:
				contentString ="" # TO CHECK IF THE REFERENCE or NOTE HAS NO CONTENTS
				for rf in ref.contents :
					if rf == rf.string : contentString += rf
						
				for tag in ref.findAll(True) :
						if len(tag.findAll(True)) == 0 and len(tag.contents) > 0 :
							for con in tag.contents :
								contentString += con
				#print contentString
				#print len(contentString.split())
				if len(contentString.split()) > 0 :	
					ref.contents = []
					texte = NavigableString(ref_ori[cpt])
					text4doi = "<bibl>"+texte+"</bibl>"
					doistring = extractId(text4doi) #UNDO here if you don't want to extract a DOI
					if doistring != '' : texte += "<doi>"+doistring+"</doi>"
					ref.insert(0,texte)

				cpt += 1
			
		except :
			pass
		
		fich = open(dirResult+self._getName(), "w")
		fich.write(str(soup.encode(formatter=None)))
		fich.close()
		return
	


	def _getName(self):
		'''
		Return the file name without the complete path
		'''
		chemin = self.nom.split("/")
		return chemin.pop()
	

	def convertToUnicode(self, chaine):
		'''
		Convert a string to unicode
		'''
		try:
			if isinstance(chaine, str):
				chaine = unicode(chaine, sys.stdin.encoding)
		except:
			chaine = unicode(chaine, 'ascii')
		return chaine

	