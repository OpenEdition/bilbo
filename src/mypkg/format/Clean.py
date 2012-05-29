# encoding: utf-8
'''
Created on 18 avr. 2012

@author: jade
'''

from mypkg.ressources.BeautifulSoup import BeautifulSoup
from mypkg.ressources.BeautifulSoup import Tag
from mypkg.reference.Word import Word
from mypkg.reference.Reference import Reference
import string
import re

class Clean(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		self.tagAttDict = {'0000': 0}
		self.nonLabels = {}
		'''
		charge les nonLabels et les features se trouvant dans le fichier features
		'''
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
			print "le fichier features est introuvable : config/features.txt \n"
		
	
	def posssign(self, line, sign) :

		for s in sign :
			nline = line.replace(s[0], s[1]) # When re.sub is used, french accents were broken
			#nline = line
			if nline != line :
				line = nline
				#print s[0], s[1]
				#print line 
				#raw_input("Press Enter to Exit")
		
		return line
	
	

	def _extract_tags(self,current_tag, lens) :
	
		words = []
	
		txts = []
		tokens = []
		tags = []
		attrs = []
	
		
		#read current tag
		n = current_tag
		top_tag = n.name
		top_att = ''
		
		'si la balise appartient au non label'
		if self.nonLabels.has_key(top_tag):
			baliseN = "<"+top_tag
			for attribut in n.attrs:
				baliseN += " "+attribut[0]+"="+"\""+attribut[1]+"\""
			baliseN += ">"
			words.append({"nom":baliseN, "caracteristique":"", "balise":["noLabel"]})
			
		#read attributes 
		if len(n.attrs) > 0 :					# if attributes exist
			top_att = ''
			attstyp_string = ''
			for curr_att in n.attrs :
				top_att = top_att + curr_att[1]+' '
				attstyp_string = attstyp_string+curr_att[0]+' '
				
			tagatt_string = n.name+' '+ attstyp_string+' '+top_att
			if self.tagAttDict.has_key(tagatt_string) :
				self.tagAttDict[tagatt_string] += 1
			else : 
				self.tagAttDict[tagatt_string] = 1	
			
		else :
			pass
	
			
		#read contents
		if str(n.string) == 'None' :			# case1 : no contents, case2 : tags in current tag
			ncons = len(n.contents)
	
			if ncons == 0 :						#case1
				pass
			else :								#case2
				self._arrangeData(n, txts, tags, attrs, top_tag, top_att)
									
		else :									#case 3 just a content, no tags in it
			txt = n.string
			txts.append(txt)
			tags.append([])
			attrs.append([])
			ct = len(txts)
			tags[ct-1].append(top_tag)
			if (top_att) : attrs[ct-1].append(top_att)
			st = string.split(n.string)
			for s in st :
				tokens.append(s)
		
		#print result
		
		for j in range(0,len(txts)) :
			balise = []
			caract = []
			if str(txts[j]) != 'None' or str(txts[j]) != '\n':
				st = string.split(str(txts[j]))
				for s in st :
					balise = []
					caract = []
					#print s,'  ++',
					for attr in attrs[j] :
						caract.extend(attr.split(" "))
					#print '++  ',
					for tag in tags[j] :
						balise.extend(tag.split(" "))
					
					if not lens > 0 : 
						balise.append("nonbibl")
					#print
					words.append({"nom":s, "caracteristique":caract, "balise":balise})
					
		
		'si la balise appartient au non label'
		if self.nonLabels.has_key(top_tag):
			baliseN = "</"+top_tag+">"
			words.append({"nom":baliseN, "caracteristique":"", "balise":["noLabel"]})
			
		return words
	
	
	def _arrangeData(self, n, txts, tags, attrs, top_tag, top_att) :
		for con in n.contents :
			txt = con.string
			if str(txt) != 'None' : 
				txts.append(txt)
				tags.append([])
				attrs.append([])
				ct = len(txts)
				tags[ct-1].append(top_tag)
				if (top_att) : attrs[ct-1].append(top_att)		# APPEND ATTRIBUTE
	
				if con == con.string :
					pass
				else :
					tags[ct-1].append(con.name)
					if len(con.attrs) > 0 : 
						atts_string = ''
						attstyp_string = ''
						for curr_att in con.attrs :
							atts_string = atts_string + curr_att[1]+' '
							attstyp_string = attstyp_string + curr_att[0]+' '
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
				for curr_att in con.attrs :
					atts_string = atts_string + curr_att[1]+' '
				temp_attr = top_att+' '+atts_string
				self._arrangeData(con, txts, tags, attrs, temp_str, top_att)
		return
	
	
	def _elimination (self, tmp_str) :
		
		targer_tag_st = "<hi font-variant=\"small-caps\">"
		targer_tag_end = "</hi>"
		
		new_str = tmp_str
		a = tmp_str.find(targer_tag_st,0)
		while a > 0 :
			b = a + len(targer_tag_st)
			c = tmp_str.find(targer_tag_end, b)
			d = c + len(targer_tag_end)
			
			new_str =  tmp_str[0:a] + tmp_str[b:c] + tmp_str[d:len(tmp_str)]
			tmp_str = new_str
			a = tmp_str.find(targer_tag_st,0)
			#raw_input("Press Enter to Exit")
			
		return new_str
		
	'''
	permet d'instancier des words avec balise et caracteristique
	dicWord : dictionnaire des words : [word, caracteristique] & [word, balise]
	'''
	def _buildWords(self, dicWords):
		words = []
		
		for word in dicWords:
			instanceWord = Word(word["nom"], word["balise"], word["caracteristique"])
			if "noLabel" in word["balise"]:
				instanceWord.ignoreWord = 1
			
			words.append(instanceWord)
		return words


	'''
	html2unicode
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
		
	