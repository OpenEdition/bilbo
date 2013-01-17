# encoding: utf-8
'''
Created on 18 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''
from bilbo.reference.Word import Word
import string
import re

class Clean(object):
	'''
	A class that tokenizes xml input data. Navigates the xml tree and extracts tokens, features and labels.
	It concerns the first step of tokenization such that words are separated by whitespace but not punctuation 
	marks. A clean object is created in a File object ("extract" method).
	'''

	def __init__(self):
		'''
		Load nonLabels and features in feature file
		Tags in nonLabels dictionary are that should be ignored
		'''
		self.tagAttDict = {'0000': 0}
		self.nonLabels = {}
		try:
			'flag = 1 : features, flag = 2 : nonLabels, flag = 3 : bookindicator'
			flag = 0 
			nameRegle = ""	
			for line in open("KB/config/features.txt"):
				lineSplit = re.split("\s", line)
				if lineSplit[0] == "#":
					nameRegle = lineSplit[1]
					flag += 1
				elif flag == 1:
					pass
				elif flag == 2:
					'nonLabels'
					self.nonLabels[lineSplit[0]] = lineSplit[1]
				
		except:
			pass
			print "Feature file not found : config/features.txt \n"
		


	def posssign(self, line, sign) :
		'''
		posssign : 
		'''
		for s in sign :
			nline = line.replace(s[0], s[1]) # When re.sub is used, French accents were broken
			#nline = line
			if nline != line :
				line = nline
		
		return line
	
	

	def _extract_tags(self,current_tag, lens) :
		'''
		Extract tags and attributes for each token by navigating xml tree
		We should carefully consider the encoding of input string because BeautifulSoup 4 causes encoding error
		when using str for the string including special accents only.
		'''	
		words = []
		txts = []
		tokens = []
		tags = []
		attrs = []
	
		#read current tag
		n = current_tag
		top_tag = n.name
		top_att = ''
		
		'If the tag appears in a nonLabel list'
		if self.nonLabels.has_key(top_tag):
			if self.nonLabels[top_tag] != "1":
				baliseN = "<"+top_tag
				for key in n.attrs.keys() :
					baliseN += " "+key+"="+"\""+n.attrs[key]+"\""
				baliseN += ">"
				words.append({"nom":baliseN, "caracteristique":"", "balise":["noLabel"]})
			
		#read attributes 
		if len(n.attrs) > 0 :	# if attributes exist, make attribute string
			top_att = ''
			attstyp_string = ''
			for key in n.attrs.keys() :
				top_att = top_att + n.attrs[key]+' '
				attstyp_string = attstyp_string+key+' '
				
			tagatt_string = n.name+' '+ attstyp_string+' '+top_att
			if self.tagAttDict.has_key(tagatt_string) :
				self.tagAttDict[tagatt_string] += 1
			else : 
				self.tagAttDict[tagatt_string] = 1	
		else :
			pass
	
		#read contents
		nstring = ''
		try : nstring = str(n.string)
		except : nstring = (n.string).encode('utf8')
			
		tagsCk = 1
		try : n.contents[0].name
		except : tagsCk = 0
		
		if nstring == 'None' or tagsCk == 1 :	#case1 : no contents, case2 : tags in current tag
			ncons = len(n.contents)
			if ncons == 0 :						#case1
				pass
			else :								#case2
				self._arrangeData(n, txts, tags, attrs, top_tag, top_att)							
		else :									#case 3 just a content, no tags in it
			txt = nstring
			txts.append(txt)
			tags.append([])
			attrs.append([])
			ct = len(txts)
			tags[ct-1].append(top_tag)
			if (top_att) : attrs[ct-1].append(top_att)
			st = string.split(nstring)
			for s in st :
				tokens.append(s)
		
		#save extracted tokens to the dictionary "words" 
		for j in range(0,len(txts)) :
			balise = []
			caract = []
			if str(txts[j]) != 'None' and str(txts[j]) != '\n':
				st = string.split(str(txts[j]))
				for s in st :
					balise = []
					caract = []
					for attr in attrs[j] :
						caract.extend(attr.split(" "))
					for tag in tags[j] :
						balise.extend(tag.split(" "))
					if not lens > 0 : 
						balise.append("nonbibl")
					words.append({"nom":s, "caracteristique":caract, "balise":balise})
				

		'If the tag appears in a nonLabel list'
		if self.nonLabels.has_key(top_tag):
			if self.nonLabels[top_tag] != "1":
				baliseN = "</"+top_tag+">"
				words.append({"nom":baliseN, "caracteristique":"", "balise":["noLabel"]})
		
		return words



	def _arrangeData(self, n, txts, tags, attrs, top_tag, top_att) :
		'''
		Unwrap the entered string(n) until the string has no tags in it. A recursive method.
		'''
		for con in n.contents :
			constring = ''
			try : constring = str(con.string)
			except : constring = (con.string).encode('utf8')
			
			tagsCk = 1
			try : con.contents[0].name
			except : tagsCk = 0

			txt = constring
			if str(txt) != 'None' and tagsCk == 0 : 
				txts.append(txt)
				tags.append([])
				attrs.append([])
				ct = len(txts)
				tags[ct-1].append(top_tag)
				if (top_att) : attrs[ct-1].append(top_att)		# APPEND ATTRIBUTE
	
				#constring2 = ''
				#try : constring2 = constring.decode('utf8')
				#except : constring2 = constring
	
				if con == constring.decode('utf8') :
					pass
				else :
					tags[ct-1].append(con.name)
					if len(con.attrs) > 0 : 
						atts_string = ''
						attstyp_string = ''
						for key in con.attrs.keys() :
							atts_string = atts_string + con.attrs[key]+' '
							attstyp_string = attstyp_string + key+' '
						attrs[ct-1].append(atts_string)
						#print atts_string
						
						tagatt_string = con.name+' '+attstyp_string+' '+atts_string
						if self.tagAttDict.has_key(tagatt_string) :
							self.tagAttDict[tagatt_string] += 1
						else : 
							self.tagAttDict[tagatt_string] = 1
					
			else : 				#case2b : more than 2 levels
				temp_str = top_tag+' '+con.name
				atts_string = ''
				#print con.name, con.attrs
				for key in con.attrs.keys() :
					atts_string = atts_string + con.attrs[key]+' '
				temp_attr = top_att+' '+atts_string
				self._arrangeData(con, txts, tags, attrs, temp_str, temp_attr)
		return
	


	def _elimination (self, tmp_str) :
		'''
		Eliminate unnecessary tags
		'''
		target_tag_st = "<hi font-variant=\"small-caps\">"
		target_tag_end = "</hi>"
		
		new_str = tmp_str
		a = tmp_str.find(target_tag_st,0)
		while a > 0 :
			b = a + len(target_tag_st)
			c = tmp_str.find(target_tag_end, b)
			d = c + len(target_tag_end)
			
			new_str =  tmp_str[0:a] + tmp_str[b:c] + tmp_str[d:len(tmp_str)]
			tmp_str = new_str
			a = tmp_str.find(target_tag_st,0)
			
		return new_str
		
		

	def _buildWords(self, dicWords):
		'''
		Make 'Word' objects with words in dicWords
		dicWord : dictionary of words returned from _extract_tags
		'''		
		words = []
		for word in dicWords:
			instanceWord = Word(word["nom"], word["balise"], word["caracteristique"])
			if "noLabel" in word["balise"]:
				instanceWord.ignoreWord = 1
			if "relateditem" in word["balise"]:
				instanceWord.item = 1
			
			words.append(instanceWord)
		return words



	def _html2unicode(self, tmp_str) :
		'''
		html2unicode
		'''
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
		
		#tmp_str = tmp_str.replace('&','&amp;')
		
		return tmp_str
		
		
	
	def _checkUTF8(self, tmp_str) :
		'''
		In BeatifulSoup 4, string matching error when there are accents only
		'''
		ck = 0
		try : str(tmp_str)
		except : 
			(tmp_str).encode('utf8')
			ck = 1
		return ck
		
	