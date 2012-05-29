# encoding: utf-8
'''
Created on 19 avr. 2012

@author: jade
'''
import re
from mypkg.reference.Word import Word

class Rule(object):
	'''
	classdocs
	'''	
	
	def __init__(self):
		'''
		Constructor
		'''
		self.special =  {'«':0, '»':0, '“':0, '”':0, '"':0, '–':0}
		self.paren = {'(':0, '{':0, '[':0, ')':0, '}':0, ']':0, '«':0, '“':0, '»':0, '”':0}
		self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0}
		
		'charge le lexique'
		self.regles = {}
		expression = "^#"
			
		'lis toutes les lignes du fichier'
		try:
			fichier = open("KB/config/lexique.txt", "r")
			lines = fichier.readlines()
			fichier.close()
			
			'creation du dictionnaire du lexique'
			for line in lines:
				if re.match(expression, line):
					lineSplit = line.split()
					self.regles[lineSplit[1]] = {}
					self.regles[lineSplit[1]]["caracteristique"] = []
					self.regles[lineSplit[1]]["regle"] = []
					
					'adde les caracteristique de cette regle'
					cpt = 2
					while cpt < (len(lineSplit)):
						self.regles[lineSplit[1]]["caracteristique"].append(lineSplit[cpt])
						cpt += 1
				else:
					self.regles[lineSplit[1]]["regle"].append(line.split())
		except:
			print "erreur ouverture fichier lxique.txt Rule.py"
		
		
			
	'''
	reorganizing separe la ponctuation adde des balises ou des caracteristiques en fonction des regles
	'''			
	def reorganizing(self, listReference) :
		cpt = 0
		flagAjoutWord = 0 	#'flag pour savoir le nombre de mot adde'
		flagPoncDebut = 0 	#'flag pour savoir si il y a une ponctuation en premiere position'
		cptIgnoreWord = 0

		for reference in listReference.getReferences() :
			cpt = 0

			for mot in reference.word :
				if mot.ignoreWord == 0:
					flagPoncDebut = 0
					if flagAjoutWord == 0:
						if mot.nom.split() != 0 :
							if mot.nom.split()[0] != '!NONE!':
								
								input_str = mot.nom.split()[0]
								
								new_str = self._checkLexique(mot, input_str)
								if new_str != '': input_str = ''
								
								#tokenization
								for c in input_str :
									if c in  ".,():{}[]!?#$%\*+/<=>@^_|~" :# not including "-"
										if new_str != '' :
											feat_str = ''
											feat_str = self._featureCheck(new_str)
											if mot.getFeature("initial") != -1: feat_str = ''
											#special char check added 
											
											if self.special.has_key(new_str) :#####added 190911
												if flagAjoutWord != 0  or flagPoncDebut == 1:
													nomTag = mot.listNomTag()
													refWord = Word(c,nomTag)
													reference.addWord(cpt+1+flagAjoutWord+cptIgnoreWord,refWord)
													flagAjoutWord += 1
												else:
													mot.nom = new_str
													mot.addTag("c")
													mot.delAllFeature()
											else :####added 190911
												if flagAjoutWord != 0 or flagPoncDebut == 1:
													nomTag = mot.listNomTag()
													refWord = Word(new_str,nomTag, feat_str.split(" "))
													reference.addWord(cpt+1+flagAjoutWord+cptIgnoreWord,refWord)
													flagAjoutWord += 1
												else:
													mot.nom = new_str
													mot.addFeature(feat_str.split(" "))
											nomTag = mot.listNomTag()
											nomTag.append("c")
											refWord = Word(c,nomTag)
											reference.addWord(cpt+1+flagAjoutWord+cptIgnoreWord,refWord)
											flagAjoutWord += 1
										else:
											if flagAjoutWord != 0:
												nomTag = mot.listNomTag()
												refWord = Word(c,nomTag)
												refWord.addTag("c")
												reference.addWord(cpt+1+flagAjoutWord+cptIgnoreWord,refWord)
												flagAjoutWord += 1
											else:
												mot.nom = c
												mot.addTag("c")
												flagPoncDebut = 1
										new_str = ''
									else :
										new_str = new_str+c
								
								if not new_str == '' :
									feat_str = ''
									feat_str = self._featureCheck(new_str)
									
									if self.special.has_key(new_str) :
										if flagPoncDebut == 1:
													refWord = Word(new_str,"c")
													reference.addWord(cpt+1+flagAjoutWord+cptIgnoreWord,refWord)
													flagAjoutWord += 1
										else:
											mot.nom = new_str
											mot.addTag("c")
											mot.delAllFeature()
									else :
										if flagPoncDebut == 1:
											nomTag = mot.listNomTag()
											refWord = Word(new_str,nomTag, feat_str.split(" "))
											reference.addWord(cpt+1+flagAjoutWord+cptIgnoreWord,refWord)
											flagAjoutWord += 1
										else:
											mot.nom = new_str
											mot.addFeature(feat_str.split(" "))
	
					else:
						flagAjoutWord -= 1
					cpt += 1
				else:
					cptIgnoreWord += 1
		return
	
	
	def _initCheck(self, input_str) :
		init1 = re.compile('^[A-Z]?[a-z]?\.-?[A-Z]?[a-z]?\.?')
		init2 = re.compile('^[A-Z]?[a-z]?-[A-Z]?[a-z]?\.?')
		p1 = init1.findall(input_str)
		p2 = init2.findall(input_str)
		
		retrn_str = ''
		if p1 : 
			#print '################',p1[0]
			retrn_str = p1[len(p1)-1]
		elif p2 : 
			#print '################',p2[0]
			retrn_str = p2[len(p1)-1]
			
		return retrn_str
	
	
	def _refCheck(self, input_str) :
		ref1 = re.compile('^http')
		ref2 = re.compile('^www.')
		ref3 = re.compile('^url')
		p1 = ref1.findall(input_str)
		p2 = ref2.findall(input_str)
		p3 = ref3.findall(input_str)
		
		retrn_str = ''
		if p1 or p2 or p3 :
			retrn_str = 'positive'
		
		return retrn_str
	
	def _featureCheck(self, new_str) :
	
		retrn_str = ''
	
		#number
		numbers = re.compile('\d+')
		if (numbers.search(new_str)) :
			retrn_str = 'numbers'
			
		num = numbers.findall(new_str)
		if len(num) == 1 and num[0] == new_str :
			retrn_str = 'allnumbers'
			if len(num[0]) == 4 : 
				retrn_str = 'allnumbers fourdigit'
			elif len(num[0]) == 3 : 
				retrn_str = 'allnumbers threedigit'
			elif len(num[0]) == 2 : 
				retrn_str = 'allnumbers twodigit'
			elif len(num[0]) == 1 : 
				retrn_str = 'allnumbers onedigit'
			else : retrn_str = 'allnumbers'
			
		elif len(num) > 1 :
			if (re.compile('-')).search(new_str) :
				retrn_str = retrn_str+' dash'
			digitck = 0
			for nn in num :
				if len(nn) == 4 :  digitck += 1
			if digitck == len(num) :
				retrn_str = retrn_str+' fourdigit'
		
		#allcapital
		allnum = re.compile('^allnumbers')
		num = re.compile('^numbers')
		if not allnum.findall(retrn_str) :
			if not num.findall(retrn_str) :		#if retrn_str != 'numbers' and retrn_str != 'numbers dash' :
				if new_str.upper() == new_str :
					retrn_str = retrn_str+' allcap'
				elif new_str[0].upper() == new_str[0] :
					retrn_str = retrn_str+' firstcap'
				elif new_str.lower() == new_str :
					retrn_str = retrn_str+' allsmall'
				else : retrn_str = retrn_str+' nonimpcap'
				
		#guillemot check
		if new_str.find('«') >= 0 : retrn_str = ' guillemot_left'		# eliminate previously detected features
		if new_str.find('»') >= 0 : retrn_str = ' guillemot_right'
		
		#quote check
		if new_str.find('“') >= 0 : retrn_str = ' quote_left'
		if new_str.find('”') >= 0 : retrn_str = ' quote_right'
	
		
		return retrn_str

			
	'''
	_checkLexique permet de add des caracteristiques si on retrouve les regles presentes dans le fichier regle
	'''
	def _checkLexique(self, mot, input_str):
		new_str = '' 
		retrn_str = ''
		
		
		'regarde si les regles sont presentes dans la chaine'
		for regle in self.regles:
			for chaine in self.regles[regle]["regle"]:
				if chaine[0] == input_str.lower():
					if regle == "editor":
						mot.delAllFeature()
						mot.addFeature(self.regles[regle]["caracteristique"])
						retrn_str = input_str
						new_str = input_str
					if regle == "page":
						mot.addFeature(self.regles[regle]["caracteristique"])
						retrn_str = input_str
						new_str = input_str
									
		if retrn_str == '':
			retrn_str = self._initCheck(input_str)
			if not retrn_str == '' :
				new_str = retrn_str
				input_str = re.sub(retrn_str, '', input_str)
				mot.addFeature('initial')
				
		'verifie les references html'
		retrn_str = self._refCheck(input_str)
		if not retrn_str == '' :
			new_str = input_str
			input_str = ''
			mot.addFeature('weblink')

		return new_str
				
				
				
		
