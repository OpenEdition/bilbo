# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 18, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bs4 import BeautifulSoup
from bilbo.reference.Word import Word
from bilbo.reference.Reference import Reference
from bilbo.format.Clean import Clean
from codecs import open
import string
import re

class CleanCorpus1(Clean):
	"""
	A class that tokenizes xml input data for corpus 1 (references).
	Sub class of Clean
	"""
	def __init__(self, options):
		Clean.__init__(self)
		self.tagAttDict = {'0000': 0}
		self.options = options
		

	def processing (self, fname, nameTagCorpus, external) :
		"""
		Extract tags and attributes of each word and create a Word object 
		
		Parameters
		----------
		fname : string
			name of file to be treated
		nameTagCorpus : string, {'bibl', 'note', ...}
			tag name of Corpus
		external : int, {1, 0}
			1 : if the references are external data except CLEO, 0 : if that of CLEO
		"""
		try :
			references = []
			tmp_str = ''

			for line in open (fname, 'r', encoding='utf8', errors='replace') :
				line = re.sub(' ', ' ', line)  # !!! eliminate this character representing a kind of SPACE but not a WHITESPACE
				line = line.replace('<!-- <pb/> -->', '')
				line = line.replace('“', '“ ') # !!! sparate the special characters '“', '”'
				line = line.replace('”', ' ”') # !!! sparate the special characters '“', '”'
				line = line.replace('\'\'', ' " ')
				#line = line.replace('&amp;', '&')
				line = line.replace('&amp;nbsp;', '&nbsp;')
				tmp_str = tmp_str + ' ' + line
			
			tmp_str = self._elimination (tmp_str)
				
			tmp_str = self._xmlEntitiesDecode(tmp_str)
			soup = BeautifulSoup (tmp_str)

			# find features document wide
			reference_features = self.get_reference_features(soup)

			i = 0
			s = soup.findAll (nameTagCorpus)
			if len(s) > 15000:
				print "Attention : there are more than 15 000 references in a file so that it uses too much memory (divide the references in several different files)"
				return
			
			while i < len(s) :
				words = []
				b = s[i] #each bibl
				if i == 639:
					pass
				allTags = b.findAll(True) #extract all tags in the current bibl
				limit = 0
				if external == 1 : limit = 0
				if len(allTags) >= limit : #WHEN IT IS FOR EXTRACTION of NEW REFERENCE '>=0', It's for the elimination of empty references.
					for c_tag in b.contents :
						if len(c_tag) > 0  and c_tag != "\n" and c_tag != " " :# NEW----------------
							
							if (c_tag != c_tag.string) : #if : if there is tag
								wordExtr = self._extract_tags(c_tag, 1)
								if len(wordExtr) > 0:
									instanceWords = self._buildWords(wordExtr)
									words.extend(instanceWords)
							else :                       #else : if there is no tags : nolabel or nonbibl
								c_tag_str = string.split(c_tag)
								if len(c_tag_str) > 0 and c_tag_str != "\n" :
									for ss in c_tag_str :
										words.append(Word(ss, ["nolabel"]))
										
					if b.find('relateditem') or b.find(nameTagCorpus) : #related item
						i += 1

				reference = Reference(words, i , features=reference_features)
				references.append(reference)
				i += 1
						
		except IOError:
			pass
			print 'reading error \n\n'
			return references
			
		return references
	
