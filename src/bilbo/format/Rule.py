# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 20, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.reference.Word import Word
from bilbo.reference.Reference import Reference
from codecs import open
import re, os

prePunc =  {'.':0, ',':0, ')':0, ';':0, '-':0, '”':0, '»':0, '}':0, ']':0, '!':0, '?':0, '\\':0, '*':0, '%':0, '*':0, '=':0, '_':0, '~':0, '>':0, '^':0, '+':0, '"':0} #'|':0, '/':0, ':':0,
postPunc = {'(':0, '–':0, '-':0, '“':0, '«':0, '{':0, '[':0, '#':0, '$':0, '@':0, '<':0} #'"':0,

class Rule(object):
	"""
	A class that reorganizes tokens according to the predefined rules.
	Especially the punctuation marks are separated and new Word objects are created.
	Features about initial expression, capitalized token etc. are verified and attached.
	"""

	def __init__(self, options):
		"""
		Constructor
		"""
		self.special =  {'«':0, '»':0, '“':0, '”':0, '"':0, '–':0}
		self.leadingQuotes = {'(':0, '{':0, '[':0, '«':0, '“':0}
		self.endingQuotes = {')':0, '}':0, ']':0, '»':0, '”':0}
		self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0, ';':0}
		
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-4])
		
		'Load the lexicon file'
		self.rules = {}
		self.options = options
		expression = "^#"
		if self.options.u : del self.special['"']
		
		try:
			fichier = open(os.path.join(self.rootDir, "KB/config/lexique.txt"), "r", encoding='utf8')
			lines = fichier.readlines()
			fichier.close()
			
			'Lexicon dictionary creation'
			#rules - {"000":{"000":[]}}, eg) rules["editor"]["feature"][0] : nonimpcap
			#                                rules["editor"]["feature"][1] : posseditor
			#                                rules["editor"]["rule"][0]    : ed
			ruleType = ''
			for line in lines:
				if line.split()[0][0] == '[' and line.split()[0][-1] == ']':
					if line.split()[0] == "[including]" :
						ruleType = "including"
					elif line.split()[0] == "[matching]" :
						ruleType = "matching"
					self.rules[ruleType] = {}
				else :
					if re.match(expression, line, flags=re.UNICODE):
						lineSplit = line.split()
						self.rules[ruleType][lineSplit[1]] = {} #Label name
						self.rules[ruleType][lineSplit[1]]["feature"] = [] #essential features
						self.rules[ruleType][lineSplit[1]]["rule"] = [] #when matching that chars add label
						'append the features of corresponding rule'
						cpt = 2
						while cpt < (len(lineSplit)):
							self.rules[ruleType][lineSplit[1]]["feature"].append(lineSplit[cpt])
							cpt += 1
					else:
						self.rules[ruleType][lineSplit[1]]["rule"].append(line.split())
					
		except:
			print "cannot open file lexique.txt"


	def reorganizing(self, listReference) :
		"""
		Separate punctuation marks and add tags or attributes according to predefined rules
		If there is a newly detached token, create a new 'Word' object and append it in the reference
		
		Parameters
		----------
		"""
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
					[midWord, tmp_str] = self._sepMidWord(wordSet[len(wordSet)-1])
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
			
		'if -u option is True, we attach punctuation. it is especially used for experiments'
		if self.options.u :
			self.attachPunc(listReference)
		#else : self.descPunc(listReference)
		
		return


	def sepTotalFrontPunc(self, word):
		"""
		Separate punctuation marks at the front of the word, it includes self._sepFrontPunc and self._sepFrontSpePunc.
		"""
		[frontWords, tmp_str] = self._sepFrontPunc(word)
		word.nom = tmp_str
		newfrontWords = []
		change = True
		while not re.match("^\w+", tmp_str, flags=re.UNICODE) and len(tmp_str) > 0 and change :
			[newfrontWords, tmp_str] = self._sepFrontSpePunc(word)
			frontWords = frontWords + newfrontWords
			if word.nom != tmp_str : word.nom = tmp_str
			else : change = False
			[newfrontWords, tmp_str] = self._sepFrontPunc(word)
			frontWords = frontWords + newfrontWords
			if word.nom != tmp_str : word.nom = tmp_str
			else : change = False
		
		return frontWords


	def _sepFrontPunc(self, word):
		"""
		Separate punctuation marks at the front of the word
		"""
		frontWords = []
		input_str = word.nom
		tagNames = word.listNomTag()
		featNames = word.listNomFeature()
		tmp_str = input_str
		i=0
		allPunc = '.,():;{}[]!?#$%\*+<=>@^_|~"' #exclude /
		if self.options.u : allPunc = allPunc[:-1]
		while (i < len(input_str)) :
			c = input_str[i]
			if c in allPunc :
				tmpWord = Word(c, tagNames, featNames)
				tmpWord.addTag("c")
				frontWords.append(tmpWord) #create word for a punctuation mark
				tmp_str = input_str[i+1:]
				i += 1
			else : i = len(input_str) #exit
				
		return frontWords, tmp_str


	def _sepFrontSpePunc(self, word):
		"""
		Separate special punctuation marks at the front of the word
		Special punctuation marks are non-English marks, which cannot be processed by regular expression
		Check out 'self.special'
		"""
		
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


	def _sepMidWord(self, word):
		"""
		Extract the word in the middle of string
		"""
		
		midWord = []
		tagNames = word.listNomTag()
		featNames = word.listNomFeature()
		i=0
		new_str =''
		tmp_str = ''
		allPunc = '.,():;{}[]!?#$%\*+<=>@^_|~"' #exclude /
		if self.options.u : allPunc = allPunc[:-1]
		while (i < len(word.nom)) :
			c = word.nom[i]
			if c in allPunc :
				midWord.append(Word(new_str, tagNames, featNames))
				tmp_str = word.nom[i:]
				i = len(word.nom)
			else :
				new_str += c
				i += 1
				
		return midWord, tmp_str


	def descPunc(self, listReference) :
		"""
		Add descriptions of punctuation as features when we detach the marks.
		It is used for experimental objective. Now we don't use it. But keep it for further experiments.
		"""
		
		for reference in listReference.getReferences() :
			quotes = 0
			for word in reference.words :
				if word.nom.find('"') >= 0 :
					quotes += 1
					if quotes % 2 == 0 : word.addFeature(['endingquotes'])
					else : word.addFeature(['leadingquotes'])
					
				if word.getTag("c") != -1 or word.nom == '"' : # it's a punctuation mark
					feat_str = 'punc '
					if word.nom == '.' : feat_str = 'point'
					elif word.nom == ',' : feat_str = 'comma'
					
					if self.leadingQuotes.has_key(word.nom) : feat_str = 'leadingquotes'
					elif self.endingQuotes.has_key(word.nom) : feat_str = 'endingquotes'
					elif self.link.has_key(word.nom) : feat_str = 'link'
					
					word.addFeature(feat_str.split())
		return


	def attachPunc(self, listReference) :
		"""
		Undo the separation of punctuation.
		"""
		for reference in listReference.getReferences() :
			reorgWords =[]
			postCk = False
			postToken = ''
			postfeat_str = ''
			for word in reference.words :
				if word.nom.find('"') >= 0 : word.addFeature(['punc'])
				oriword = 'NONE'
				if postCk :
					oriword = word.nom
					word.nom = postToken+word.nom
					word.addFeature(postfeat_str.split())
					
				if word.getTag("c") != -1 or word.nom == '"' : # it's a punctuation mark
					if prePunc.has_key(word.nom) and len(reorgWords) > 0 :
						#attach to the previous word
						preWord = reorgWords.pop()
						preWord.nom = preWord.nom+word.nom
						feat_str = 'punc '
						if word.nom == '.' : feat_str = 'point'
						elif word.nom == ',' : feat_str = 'comma'
						
						if self.endingQuotes.has_key(word.nom) : feat_str = 'endingquotes'
						elif self.link.has_key(word.nom) : feat_str = 'link'
						
						preWord.addFeature(feat_str.split())
						reorgWords.append(preWord)
						postCk = False
					#elif postPunc.has_key(word.nom) or postPunc.has_key(oriword) :
					else: # take punctuation not recognised as post, being pre ! (yes variable names prePunc, postPunc are misleading)
						postCk = True
						postToken = word.nom
						postfeat_str = 'punc '
						if word.nom == '.' : postfeat_str = 'point'
						
						if self.leadingQuotes.has_key(word.nom) : postfeat_str = 'leadingquotes'
						elif self.link.has_key(word.nom) : postfeat_str = 'link'
						
				else :
					reorgWords.append(word)
					postCk = False
				
			#for w in reorgWords : w.affiche()
			reorgWords = self._findPuncFunc(reorgWords)
			reference.replaceReference(reorgWords,len(reorgWords))
		
		return


	def _findPuncFunc(self, words):
		"""
		Add quotes features when we attach punctuation marks. They are essential features when punctuation is attached.
		"""
		for w in words :
			if w.nom[0] == '"' : w.addFeature(['leadingquotes'])
			elif w.nom.find('"') > 0 : w.addFeature(['endingquotes'])
			if w.nom.find('(') >= 0 and w.nom.find(')') > 0 :
				w.addFeature(['pairedbraces'])
		return words


	def _initCheck(self, input_str) :
		"""
		Check initial expressions
		"""
		init1 = re.compile('^[A-Z][a-z]?\.-?[A-Z]?[a-z]?\.?', flags=re.UNICODE)
		init2 = re.compile('^[A-Z][a-z]?-[A-Z]?[a-z]?\.?', flags=re.UNICODE)
		init3 = re.compile('^[A-Z][A-Z]?\.?-?[A-Z]?[a-z]?\.', flags=re.UNICODE)
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
		"""
		Check web link expressions
		"""
		ref1 = re.compile('^http', flags=re.UNICODE)
		ref2 = re.compile('^www.', flags=re.UNICODE)
		ref3 = re.compile('^url', flags=re.UNICODE)
		p1 = ref1.findall(input_str)
		p2 = ref2.findall(input_str)
		p3 = ref3.findall(input_str)
		retrn_str = ''
		if p1 or p2 or p3 :
			retrn_str = 'positive'
		
		return retrn_str


	def _featureCheck(self, new_str) :
		"""
		Check number, guillemot
		"""
		retrn_str = ''
	
		#number
		numbers = re.compile('\d+', flags=re.UNICODE)
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
			if (re.compile('-', flags=re.UNICODE)).search(new_str) :
				retrn_str = retrn_str+' dash'
			digitck = 0
			for nn in num :
				if len(nn) == 4 :  digitck += 1
			if digitck == len(num) :
				retrn_str = retrn_str+' fourdigit'
		
		#allcapital
		allnum = re.compile('^allnumbers', flags=re.UNICODE)
		num = re.compile('^numbers', flags=re.UNICODE)
		if not allnum.findall(retrn_str) :
			if not num.findall(retrn_str) : #if retrn_str != 'numbers' and retrn_str != 'numbers dash' :
				if new_str.upper() == new_str :
					retrn_str = retrn_str+' allcap'
				elif new_str[0].upper() == new_str[0] :
					retrn_str = retrn_str+' firstcap'
				elif new_str.lower() == new_str :
					retrn_str = retrn_str+' allsmall'
				else : retrn_str = retrn_str+' nonimpcap'
				
		#guillemot check
		if new_str.find('«') >= 0 : retrn_str = ' guillemot_left' # eliminate previously detected features
		if new_str.find('»') >= 0 : retrn_str = ' guillemot_right'
		
		#quote check
		if new_str.find('“') >= 0 : retrn_str = ' quote_left'
		if new_str.find('”') >= 0 : retrn_str = ' quote_right'
	
		return retrn_str


	def _checkLexique(self, word, input_str):
		"""
		Add attributes according to predefined rules in a lexicon file
		"""
		new_str = ''
		retrn_str = ''
		
		'check if rules are matched in the string'
		for ruleType in self.rules :
			for rule in self.rules[ruleType]:
				for chaine in self.rules[ruleType][rule]["rule"]:
					if (input_str.lower()).find(chaine[0]) == 0 :
						charck = re.compile('[a-z]', flags=re.UNICODE)
						'In case of including the key word in the string, no character except the key word'
						if ruleType == "including" and not charck.findall((input_str.lower()).replace(chaine[0],'')) :
							#word.delAllFeature()
							word.addFeature(self.rules[ruleType][rule]["feature"])
							retrn_str = chaine[0]
							new_str = input_str
							input_str = re.sub(retrn_str, '', input_str.lower(), flags=re.UNICODE)
							new_str = new_str.replace(input_str, '', 1)
						'In case of just matching the key word'
						if ruleType == "matching" and chaine[0] == input_str.lower() :
							word.addFeature(self.rules[ruleType][rule]["feature"])
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
