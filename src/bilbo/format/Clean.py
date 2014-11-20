# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.reference.Word import Word
import string
import regex as re
import os
from codecs import open

class Clean(object):
	"""
	A class that tokenizes xml input data. Navigates the xml tree and extracts tokens, features and labels.
	It concerns the first step of tokenization such that words are separated by whitespace but not by punctuation
	marks. A clean object is created in a File object ("extract" method).
	"""

	def __init__(self):
		"""
		Load nonLabels and features in feature file
		Tags in nonLabels dictionary are that should be ignored
		"""
		self.nonLabels = {}
		self.tagAttDict = {'0000': 0}
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-4])
		try:
			'flag = 1 : features, flag = 2 : nonLabels, flag = 3 : bookindicator'
			flag = 0
			nameRegle = ""
			
			for line in open(os.path.join(self.rootDir, "KB/config/features.txt"), encoding='utf8'):
				lineSplit = re.split("\s", line, flags=re.UNICODE)
				if lineSplit[0] == "#":
					nameRegle = lineSplit[1]
					flag += 1
				elif flag == 1:
					pass
				elif flag == 2:
					'nonLabels'
					self.nonLabels[lineSplit[0]] = lineSplit[1]
		except IOError:
			pass
			print "Feature file not found : config/features.txt \n"
		except:
			raise


	def posssign(self, line, sign) :
		for s in sign :
			nline = line.replace(s[0], s[1]) # When re.sub is used, French accents were broken
			#nline = line
			if nline != line :
				line = nline
		return line


	def _extract_tags(self,current_tag, lens) :
		"""
		Extract tags and attributes for each token by navigating xml tree
		We should carefully consider the encoding of input string because BeautifulSoup 4 causes encoding error
		when using str for the string including special accents only.
		"""
		words = []
		txts = []
		tokens = []
		tags = []
		attrs = []
	
		#read current tag
		n = current_tag
		top_tag = n.name
		top_att = ''
			
		#read attributes 
		if len(n.attrs) > 0 :	# if attributes exist, make attribute string
			top_att = ''
			attstyp_string = ''
			for key in n.attrs.keys() :
				if isinstance(n.attrs[key], (str, unicode)) :
					top_att = top_att + n.attrs[key]+' '
				else :
					top_att = top_att + n.attrs[key][0]+' '
				attstyp_string = attstyp_string+key+' '
				
			tagatt_string = n.name+' '+ attstyp_string+' '+top_att
			if self.tagAttDict.has_key(tagatt_string) :
				self.tagAttDict[tagatt_string] += 1
			else :
				self.tagAttDict[tagatt_string] = 1
		else :
			pass
	
		#read contents
		nstring = unicode(n.string)
			
		tagsCk = 1
		try :
			n.contents[0].name
		except :
			tagsCk = 0
		
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
			if txts[j] != 'None' and txts[j] != '\n':
				st = string.split(txts[j])
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
				
		return words


	def _arrangeData(self, n, txts, tags, attrs, top_tag, top_att) :
		"""
		Unwrap the entered string(n) until the string has no tags in it. A recursive method.
		"""
		for con in n.contents :
			constring = ''
			constring = unicode(con.string)
			
			tagsCk = 1
			try :
				con.contents[0].name
			except:
				tagsCk = 0

			txt = constring
			if txt != 'None' and tagsCk == 0 :
				txts.append(txt)
				tags.append([])
				attrs.append([])
				ct = len(txts)
				tags[ct-1].append(top_tag)
				if (top_att) :
					attrs[ct-1].append(top_att)		# APPEND ATTRIBUTE

				if unicode(con) == constring:
					pass
				else :
					tags[ct-1].append(con.name)
					if len(con.attrs) > 0 :
						atts_string = ''
						attstyp_string = ''
						for key in con.attrs.keys() :
							if isinstance(con.attrs[key], (str, unicode)) :
								atts_string = atts_string + con.attrs[key]+' '
							else :
								atts_string = atts_string + con.attrs[key][0]+' '
							attstyp_string = attstyp_string + key+' '
						attrs[ct-1].append(atts_string)
						tagatt_string = con.name+' '+attstyp_string+' '+atts_string
						if self.tagAttDict.has_key(tagatt_string) :
							self.tagAttDict[tagatt_string] += 1
						else :
							self.tagAttDict[tagatt_string] = 1
					
			else : #case2b : more than 2 levels
				temp_str = top_tag+' '+con.name
				atts_string = ''
				for key in con.attrs.keys() :
					if isinstance(con.attrs[key], (str, unicode)) :
						atts_string = atts_string + con.attrs[key]+' '
					else :
						atts_string = atts_string + con.attrs[key][0]+' '
				temp_attr = top_att+' '+atts_string
				self._arrangeData(con, txts, tags, attrs, temp_str, temp_attr)
		return


	def _elimination (self, tmp_str) :
		"""
		Eliminate unnecessary tags
		"""
		target_tag_st = "<hi font-variant=\"small-caps\">"
		target_tag_end = "</hi>"
		
		new_str = tmp_str
		a = tmp_str.find(target_tag_st,0)
		while a > 0 :
			b = a + len(target_tag_st)
			c = tmp_str.find(target_tag_end, b)
			d = c + len(target_tag_end)
			
			new_str =  tmp_str[:a] + tmp_str[b:c] + tmp_str[d:]
			tmp_str = new_str
			a = tmp_str.find(target_tag_st,0)
		
		target_tag_st = "<hi "	#a
		target_tag_mi = ">"		#c
		target_tag_end = "</hi>"#d e
		
		tmp_str = new_str
		a = tmp_str.find(target_tag_st,0)
		while a > 0 :
			b = a + len(target_tag_st)
			c = tmp_str.find(target_tag_mi, b)
			d = tmp_str.find(target_tag_end, c)
			e = d + len(target_tag_end)
			if c > 0 and d > 0 and e > 0 and ( re.match(" \p{L}", tmp_str[a-2:a], flags=re.UNICODE) or (re.match("\p{L}", tmp_str[d-1:d], flags=re.UNICODE) and re.match("\p{L}", tmp_str[e:e+1], flags=re.UNICODE))  ):
				new_str =  tmp_str[:a] + tmp_str[c+1:d] + tmp_str[e:]
				tmp_str = new_str
				a = tmp_str.find(target_tag_st,0)
			else :
				if c > 0 and d > 0 and e > 0 :
					a = tmp_str.find(target_tag_st,e)
				else : a = 0

		return new_str


	def _buildWords(self, dicWords):
		"""
		Make 'Word' objects with words in dicWords
		dicWord : dictionary of words returned from _extract_tags
		"""
		words = []
		for word in dicWords:
			instanceWord = Word(word["nom"], word["balise"], word["caracteristique"])
			if "noLabel" in word["balise"]:
				instanceWord.ignoreWord = 1
			if "relateditem" in word["balise"]:
				instanceWord.item = 1
			
			words.append(instanceWord)
		return words


	def _xmlEntitiesDecode(self, tmp_str) :
		"""
		xmlEntitiesDecode
		"""
		#for numerical codes
		matches = re.findall("&#\d+;", tmp_str, flags=re.UNICODE)
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
		matches = re.findall("&#[xX][0-9a-fA-F]+;", tmp_str, flags=re.UNICODE)
		if len(matches) > 0 :
			hits = set(matches)
			for hit in hits :
				hex = hit[3:-1]
				try :
					entnum = int(hex, 16)
					tmp_str = tmp_str.replace(hit, unichr(entnum))
				except ValueError:
					pass
		
		return tmp_str

	# Find features that are in the document not in the reference
	# all implemented here, but should be moved elsewhere one refactoring day !
	def get_reference_features(self, soup):
		features_to_find = [
			('JNAME', 'parent_tag_attr', ('publicationstmt', 'ref', 'target')),
			('LANG', 'parent_tag_attr', ('langusage', 'language', 'ident')),
			('CAT', 'parent_tag_attr', ('category', 'catdesc', 'xml:id')),
		]
		features = []
		for (feature_name, search_type, search_terms) in features_to_find:
			feature = None
			if search_type == 'parent_tag_attr':
				tag_parent, tag_name, attribute = search_terms
				feature = soup.find(tag_parent)
				if feature:
					feature = feature.find(tag_name)
				if feature:
					feature = feature.get(attribute)
				if feature:
					feature = feature_name + "_" + feature.upper()
				else:
					feature = "NO_" + feature_name
			if feature:
				features.append(feature)

		return features
