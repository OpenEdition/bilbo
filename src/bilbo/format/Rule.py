# encoding: utf-8
'''
Created on 19 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''
from bilbo.reference.Word import Word
from bilbo.reference.Reference import Reference
import re

class Rule(object):
	'''
	A class that reorganizes tokens according to the predefined rules.
	Especially the punctuation marks are separated and new Word objects are created.
	Features about initial expression, capitalized token etc. are verified and attached.
	'''
	
	def __init__(self):
		'''
		Constructor
		'''
		self.special =  {'«':0, '»':0, '“':0, '”':0, '"':0, '–':0}
		self.paren = {'(':0, '{':0, '[':0, ')':0, '}':0, ']':0, '«':0, '“':0, '»':0, '”':0}
		self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0}
		
		'Load the lexicon file'
		self.regles = {}
		expression = "^#"
		
		try:
			fichier = open("KB/config/lexique.txt", "r")
			lines = fichier.readlines()
			fichier.close()
			
			
			'Lexicon dictionary creation'
			#regles - {"000":{"000":[]}}, eg) regles["editor"]["caracteristique"][0] : nonimpcap
			#								  regles["editor"]["caracteristique"][1] : posseditor
			#								  regles["editor"]["regle"][0] : ed
			ruleType = ''
			for line in lines:
				if line.split()[0][0] == '[' and line.split()[0][-1] == ']':
					if line.split()[0] == "[including]" : 
						ruleType = "including"
					elif line.split()[0] == "[matching]" : 
						ruleType = "matching"
					self.regles[ruleType] = {}
				else :
					if re.match(expression, line):
						lineSplit = line.split()
						self.regles[ruleType][lineSplit[1]] = {}	#Label name
						self.regles[ruleType][lineSplit[1]]["caracteristique"] = []	#essential features
						self.regles[ruleType][lineSplit[1]]["regle"] = []	#when matching that chars add label
						'append the features of corresponding rule'
						cpt = 2
						while cpt < (len(lineSplit)):
							self.regles[ruleType][lineSplit[1]]["caracteristique"].append(lineSplit[cpt])
							cpt += 1
					else:
						self.regles[ruleType][lineSplit[1]]["regle"].append(line.split())
					
		except:
			print "cannot open file lexique.txt"
		

	def reorganizing(self, listReference) :
		'''
		Separate punctuation marks and add tags or attributes according to predefined rules
		If there is a newly detached token, create a new 'Word' object and append it in the reference
		
		Parameters
		----------
		'''
		for reference in listReference.getReferences() :
			reorgWords =[]
			for word in reference.words :
				frontWords = []
				frontWords = self.sepTotalFrontPunc(word)
				wordSet = frontWords
				
				tmpWord = []
				new_str = ''
				if word.nom != '' :
					'new_str is a string to be saved, input_str is a string to be handled'
					[new_str, input_str] = self._checkLexique(word, word.nom) #lexical matching from front
					frontWords = []
					if new_str != '' : #lexical matching OK
						word.nom = new_str
						if input_str != '' :
							tmpWord.append(Word(input_str, word.listNomTag(), word.listNomFeature()))
							frontWords = self.sepTotalFrontPunc(tmpWord[0])
					else : pass
					
				'arrange'
				endWord = ''
				if new_str != '' : #matching
					wordSet.append(word)
					if input_str != '' :
						wordSet = wordSet + frontWords
						if tmpWord[0].nom != '' : wordSet.append(tmpWord[0])
						endWord = tmpWord[0].nom
				else : #nonmatching
					if word.nom != '' : wordSet.append(word)
					endWord = word.nom
					
				'remained string treatment'
				while endWord != '' :
					#Let's separate back punctuation
					[midWord, tmp_str] = self.sepMidWord(wordSet[len(wordSet)-1])
					if midWord != [] :
						#modify final word of wordSet
						wordSet.pop() #delete last word
						wordSet.append(midWord[0])
						if tmp_str != '' : #string with starting punctuation
							frontWords = []
							newWord = []
							newWord.append(Word(tmp_str, (wordSet[len(wordSet)-1]).listNomTag(), (wordSet[len(wordSet)-1]).listNomFeature()))
							frontWords = self.sepTotalFrontPunc(newWord[0])
							wordSet += frontWords
							if frontWords != [] : endWord = newWord[0].nom
							else : endWord = ''
							if endWord != '' : wordSet.append(newWord[0])
					else : #No punctuation
						endWord = ''
						
				for w in wordSet : 
					feat_str = self._featureCheck(w.nom)
					if w.getTag("c") == -1 : w.addFeature(feat_str.split(" "))
					reorgWords.append(w)

			#for w in reorgWords : w.affiche()			
			reference.replaceReference(reorgWords,len(reorgWords))	
			
		return
	
		
	def sepFrontPunc(self, word):
		
		frontWords = []
		input_str = word.nom
		tagNames = word.listNomTag()
		featNames = word.listNomFeature()
		tmp_str = input_str
		i=0
		while (i < len(input_str)) :
			c = input_str[i]
			if c in  ".,():;{}[]!?#$%\*+/<=>@^_|~" :
				tmpWord = Word(c, tagNames, featNames)
				tmpWord.addTag("c")
				frontWords.append(tmpWord) #create word for a punctuation mark
				tmp_str = input_str[i+1:]
				i += 1
			else : i = len(input_str)	#exit
				
		return frontWords, tmp_str
	
		
	def sepFrontSpePunc(self, word):
		
		frontWords = []
		input_str = word.nom
		tagNames = word.listNomTag()
		featNames = word.listNomFeature()
		new_str = input_str
		
		for key in self.special.keys() :
			if new_str.find(key) == 0 :
				new_str = new_str[len(key):]
				tmpWord = Word(key, tagNames, featNames)
				tmpWord.addTag("c")
				frontWords.append(tmpWord)
				
		return frontWords, new_str
	
	
	def sepTotalFrontPunc(self, word):
		
		[frontWords, tmp_str] = self.sepFrontPunc(word)
		word.nom = tmp_str
		newfrontWords = []
		change = True
		while not re.match("^\w+", tmp_str) and len(tmp_str) > 0 and change : 
			[newfrontWords, tmp_str] = self.sepFrontSpePunc(word)
			frontWords = frontWords + newfrontWords
			if word.nom != tmp_str : word.nom = tmp_str
			else : change = False
			[newfrontWords, tmp_str] = self.sepFrontPunc(word)
			frontWords = frontWords + newfrontWords
			if word.nom != tmp_str : word.nom = tmp_str
			else : change = False
		
		return frontWords


	def sepMidWord(self, word):
		
		midWord = []
		tagNames = word.listNomTag()
		featNames = word.listNomFeature()
		i=0
		new_str =''
		tmp_str = ''
		while (i < len(word.nom)) :
			c = word.nom[i]
			if c in  ".,():;{}[]!?#$%\*+/<=>@^_|~" :
				midWord.append(Word(new_str, tagNames, featNames))
				tmp_str = word.nom[i:]
				i = len(word.nom)
			else : 
				new_str += c
				i += 1
				
		return midWord, tmp_str
			
			
	def _initCheck(self, input_str) :
		'''
		Check initial expressions
		'''
		init1 = re.compile('^[A-Z][a-z]?\.-?[A-Z]?[a-z]?\.?')
		init2 = re.compile('^[A-Z][a-z]?-[A-Z]?[a-z]?\.?')
		init3 = re.compile('^[A-Z][A-Z]?\.?-?[A-Z]?[a-z]?\.')
		p1 = init1.findall(input_str)
		p2 = init2.findall(input_str)
		p3 = init3.findall(input_str)
		
		retrn_str = ''
		if p1 : 
			#print '################',p1[0]
			retrn_str = p1[len(p1)-1]
		elif p2 : 
			#print '################',p2[0]
			retrn_str = p2[len(p2)-1]
		elif p3 : 
			#print '################',p3[0]
			retrn_str = p3[len(p3)-1]
	
		return retrn_str
	
	
	def _refCheck(self, input_str) :
		'''
		Check web link expressions
		'''
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
		'''
		Check number, guillemot
		'''
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
		if new_str.find('«') >= 0 : retrn_str = ' guillemot_left'	# eliminate previously detected features
		if new_str.find('»') >= 0 : retrn_str = ' guillemot_right'
		
		#quote check
		if new_str.find('“') >= 0 : retrn_str = ' quote_left'
		if new_str.find('”') >= 0 : retrn_str = ' quote_right'
	
		return retrn_str

			
	def _checkLexique(self, word, input_str):
		'''
		Add attributes according to predefined rules in a lexicon file
		'''
		new_str = '' 
		retrn_str = ''
		
		'check if rules are matched in the string'
		for ruleType in self.regles :
			for regle in self.regles[ruleType]:
				for chaine in self.regles[ruleType][regle]["regle"]:
					if (input_str.lower()).find(chaine[0]) == 0 :
						charck = re.compile('[a-z]')	
						'In case of including the key word in the string, no character except the key word'
						if regle == "editor" and not charck.findall((input_str.lower()).replace(chaine[0],'')) :
							word.delAllFeature()
							word.addFeature(self.regles[ruleType][regle]["caracteristique"])
							retrn_str = chaine[0]
							new_str = input_str
							input_str = re.sub(retrn_str, '', input_str.lower())
							new_str = new_str.replace(input_str, '')
						'In case of just matching the key word'
						if regle == "page" and chaine[0] == input_str.lower() :
							word.addFeature(self.regles[ruleType][regle]["caracteristique"])
							retrn_str = input_str
							new_str = input_str
							input_str = ''
									
		if retrn_str == '':
			retrn_str = self._initCheck(input_str)
			if not retrn_str == '' :
				new_str = retrn_str
				input_str = re.sub(retrn_str, '', input_str)
				word.addFeature('initial')
				
		'check url'
		retrn_str = self._refCheck(input_str)
		if not retrn_str == '' :
			new_str = input_str
			input_str = ''
			word.addFeature('weblink')

		return [new_str, input_str]
				
				
				
		
