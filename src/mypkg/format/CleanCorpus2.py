# encoding: utf-8
'''
Created on 18 avr. 2012

@author: Young-Min Kim, Jade Tavernier
'''

from mypkg.ressources.BeautifulSoup import  BeautifulSoup
from mypkg.ressources.BeautifulSoup import  Tag
from mypkg.reference.Word import Word
from mypkg.reference.Reference import Reference
from mypkg.format.Clean import Clean
import string
import re

class CleanCorpus2(Clean):

	def __init__(self):
		Clean.__init__(self)
		self.tagAttDict = {'0000': 0}
		
	

	
	def processing (self, fname, typeCorpus, external) :
		tagAttDict = {'0000': 0}
		refSign = []
		precitSign = []
		references = []
		
		try :
		#if len(references) ==0:
			tmp_str = ''
			for line in open (fname, 'r') :
				line = re.sub(' ', ' ', line)	# !!! eliminate this character representing a kind of SPACE but not a WHITESPACE
				line = re.sub("<hi rend=\"sup\">", ' ',line)
				line = line.replace('“', '“ ')			# !!! sparate the special characters '“', '”'
				line = line.replace('”', ' ”')			# !!! sparate the special characters '“', '”'
				line = line.replace('&amp;', '&')	
				line = self.posssign(line, refSign)		# term or phrase representing the reference part in note, IF THIS IS A PHRASE INSERT DASH BETWEEN WORDS
				line = self.posssign(line, precitSign)	# term or phrase indicating the previously cited reference, IF THIS IS A PHRASE INSERT DASH BETWEEN WORDS
				tmp_str = tmp_str + ' ' + line
				
	
			tmp_str = self._elimination (tmp_str)
			try:
				tmp_str = tmp_str.decode('utf8')
			except:
				tmp_str = str(tmp_str)
			tmp_str = self._html2unicode(tmp_str)
			#tmp_str = tmp_str.decode('utf8')
			#tmp_str = bytes.fromhex(tmp_str).decode('utf-8')
			
			tmp_str = tmp_str.replace("\n", "")
			soup = BeautifulSoup (tmp_str)

			for nt in soup.findAll ('note') :
				#print len(nt), nt.contents
				c = 0
				for nt_c in nt.contents :
					'verifie si la note contient une reference'
					if nt_c == nt_c.string :
						pass
					elif nt_c.name == 'bibl' : # bibl or other tag
						pass
					elif nt_c.findAll('bibl') : ############### structure flatten, pull <bibl> to top level for the extraction #################
						newc = nt_c.findAll('bibl')
											
						nsoup = BeautifulSoup (nt_c.renderContents())
						nt_c.replaceWith( nsoup.contents[0] )
						nsouplen = len(nsoup.contents)
						if (nsouplen > 0) :
							for iter in range(nsouplen) :
								nt.insert(c+1+iter,Tag(soup,"mytag"))
								nt.mytag.replaceWith( nsoup.contents[0] )
						
						pass
					
					c += 1
					
				#raw_input("Press Enter to Exit1")
				i = 0
				s = nt.findAll ("bibl")	
				sAll = nt.contents 
				words = []
				while i < len(sAll) :
					if i == 20:
						pass
					b = sAll[i]	#each bibl 
		
					if b != b.string :
						allTags = b.findAll(True)					#extract all tags in the current bibl
						limit = 1
						if external == 1 : limit = 0 
						if len(allTags) >= limit : ######################## !!!!!!!!!!!!! WHEN IT IS FOR EXTRACTION of NEW REFERENCE insert '>=' IF NOT '>'
							for c_tag in b.contents :
								if len(c_tag) > 0  and str(c_tag) != "\n" and c_tag != " ":
									
									if (c_tag != c_tag.string) :	#'if : si il y a des balises'
										wordExtr = self._extract_tags(c_tag, len(s))
										if len(wordExtr) > 0:
											instanceWords = self._buildWords(wordExtr)
											words.extend(instanceWords)
									else :							#else : si il n y a pas de balise donc : nolabel
										c_tag_str = string.split(c_tag)
										if len(c_tag_str) > 0 and c_tag_str != "\n" :
											for ss in c_tag_str :
												if len(s) > 0 :
													words.append(Word(ss.encode('utf8'), ["nolabel"]))
												else:
													words.append(Word(ss.encode('utf8'), ["nonbibl"]))
			
							if b.find('relateditem') :					# related item
								i += 1
								br =  sAll[i]
			
								allTags = br.findAll(True)					#extract all tags in the current bibl
		
								for c_tag in br.contents :
									if len(c_tag) > 0  and str(c_tag) != "\n" and c_tag != " " :
										if (c_tag != c_tag.string) :
											wordExtr = self._extract_tags(c_tag, len(s))
											if len(wordExtr) > 0:
												newWord = self._buildWords(wordExtr)
												newWord[0].item = 1
												words.extend(newWord)
										else :
											c_tag_str = string.split(c_tag)
											if len(c_tag_str) > 0 and c_tag_str != "\n" :
												for ss in c_tag_str :
													newWord = Word(ss.encode('utf8'), ["nolabel"])
													newWord.item = 1
													words.append(newWord)
						else:
							if len(b.contents) > 0 :
								input_str = b.contents[0]
								for input in input_str.split() :
									feature = []
									if len(b.attrs) : 
										feature =  b.attrs[0][1],
									
									newWord = Word(input.encode('utf8'), [b.name, 'nonbibl'], feature)
									words.append(newWord)
									
						
					elif len(b.split()) > 0 :
						for input in b.split() :
							newWord = Word(input.encode('utf8'), ['nonbibl'])
							words.append(newWord)
					i += 1
				references.append(Reference(words,i))
				
						
		except IOError:
			pass
			print 'reading error\n\n'
			return references
			
		return references

