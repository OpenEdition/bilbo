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

class CleanCorpus2(Clean):
	"""
	A class that tokenizes xml input data for corpus 2 (notes).
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
		refSign = []
		precitSign = []
		references = []
		
		try :
		#if len(references) ==0:
			tmp_str = ''
			for line in open (fname, 'r', encoding='utf8', errors='replace') :
				line = re.sub(' ', ' ', line)	# !!! eliminate this character representing a kind of SPACE but not a WHITESPACE
				line = line.replace('<!-- <pb/> -->', '')
				line = line.replace('“', '“ ')			# !!! sparate the special characters '“', '”'
				line = line.replace('”', ' ”')			# !!! sparate the special characters '“', '”'
				line = line.replace('\'\'', ' " ')
				line = line.replace('&amp;nbsp;', '&nbsp;')
				line = self.posssign(line, refSign)		# term or phrase representing the reference part in note, IF THIS IS A PHRASE INSERT DASH BETWEEN WORDS
				line = self.posssign(line, precitSign)	# term or phrase indicating the previously cited reference, IF THIS IS A PHRASE INSERT DASH BETWEEN WORDS
				tmp_str = tmp_str + ' ' + line
				
			tmp_str = self._elimination (tmp_str)

			tmp_str = self._xmlEntitiesDecode(tmp_str)
			tmp_str = tmp_str.replace("\n", "")
			soup = BeautifulSoup (tmp_str)

			for nt in soup.findAll ('note') :
				c = 0
				for nt_c in nt.contents :
					'verify if the note has a reference'
					if nt_c == nt_c.string :
						pass
					elif nt_c.name == 'bibl' : # bibl or other tag
						pass
					elif nt_c.findAll('bibl') : # structure flatten, pull <bibl> to top level for the extraction ###
						nsoup = BeautifulSoup (nt_c.renderContents())
						nt_c.replace_with( nsoup.contents[0] )
						nsouplen = len(nsoup.contents)
						if (nsouplen > 0) :
							for iter in range(nsouplen) :
								nt.insert(c+1+iter,soup.new_tag("mytag"))
								nt.mytag.replaceWith( nsoup.contents[0] )
					c += 1
				
				i = 0
				s = nt.findAll ("bibl")
				sAll = nt.contents
				words = []
				#Filter the non-annotated notes for training, if we don't use SVM, just select notes including bibls
				validNote = True
				if self.options.T and not self.options.v and len(s) == 0 : validNote = False
				
				while i < len(sAll) and validNote :
					if i == 20:
						pass
					b = sAll[i]	#each item in nt.contents
					if b != b.string :
						allTags = b.findAll(True)	#extract all tags in the current bibl
						limit = 1
						if external == 1 : limit = 0
						
						if len(allTags) >= limit : # WHEN IT IS FOR EXTRACTION of NEW REFERENCE '>=0'
							for c_tag in b.contents :
								#ck = self._checkUTF8(c_tag)
								if len(c_tag) > 0  and c_tag != "\n" and c_tag != " " :
									
									if (c_tag != c_tag.string) :	#if : if there is tag
										wordExtr = self._extract_tags(c_tag, len(s))
										if len(wordExtr) > 0:
											instanceWords = self._buildWords(wordExtr)
											words.extend(instanceWords)
									else :							#else : if there is no tags : nolabel or nonbibl
										c_tag_str = string.split(c_tag)
										if len(c_tag_str) > 0 and c_tag_str != "\n" :
											for ss in c_tag_str :
												if len(s) > 0 :
													words.append(Word(ss, ["nolabel"]))
												else:
													words.append(Word(ss, ["nonbibl"]))
							if b.find('relateditem') :	#related item
								#i += 1 ##### don't need it because <bibl>s are in <note>, no risk to print again
								pass 

						else:
							if len(b.contents) > 0 :
								input_str = b.contents[0]
								for input in input_str.split() :
									features = []
									if len(b.attrs) :
										for key in b.attrs.keys() :
											if isinstance(b.attrs[key], unicode) : features.append(b.attrs[key])
											else : features.append(b.attrs[key][0])

									newWord = Word(input, [b.name, 'nonbibl'], features)
									words.append(newWord)
						
					elif len(b.split()) > 0 :
						for input in b.split() :
							newWord = Word(input, ['nonbibl'])
							words.append(newWord)
					i += 1
				references.append(Reference(words,i))
		
		except IOError:
			pass
			print 'reading error\n\n'
			return references
			
		return references
