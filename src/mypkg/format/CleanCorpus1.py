# encoding: utf-8
'''
Created on 18 avr. 2012

@author: Young-min Kim, Jade Tavernier
'''

from mypkg.ressources.BeautifulSoup import BeautifulSoup
from mypkg.reference.Word import Word
from mypkg.reference.Reference import Reference
from mypkg.format.Clean import Clean
import string
import re

class CleanCorpus1(Clean):

	def __init__(self):
		Clean.__init__(self)
		self.tagAttDict = {'0000': 0}
		
	
	'''
	processing : 
		fname : nom du fichier
		typeCorpus : balise de depart de la reference
	'''
	def processing (self,fname, typeCorpus, external) :
		try :
			references = []
			tmp_str = ''

			for line in open (fname, 'r') :
				line = re.sub(' ', ' ', line)	# !!! eliminate this character representing a kind of SPACE but not a WHITESPACE
				line = line.replace('“', '“ ')			# !!! sparate the special characters '“', '”'
				line = line.replace('”', ' ”')			# !!! sparate the special characters '“', '”'
				line = line.replace('&amp;', '&')
				tmp_str = tmp_str + ' ' + line
			
			tmp_str = self._elimination (tmp_str)
			try:
				tmp_str = tmp_str.decode('utf8')
			except:
				tmp_str = str(tmp_str)
			tmp_str = self._html2unicode(tmp_str)
			soup = BeautifulSoup (tmp_str)		

				
			i = 0
			s = soup.findAll (typeCorpus)
			if len(s) > 15000:
				print "Attention : il y a plus de 15 000 références dans le meme fichier cela prends trop de memoire (disperser les references dans plusieur fichier)"	
				return
			
			
			while i < len(s) :
				words = []
				b = s[i]	#each bibl
				#print b 
				if i == 639:
					pass
				allTags = b.findAll(True)					#extract all tags in the current bibl
				limit = 0
				if external == 1 : limit = 0 
				if len(allTags) >= limit : ######################## !!!!!!!!!!!!! WHEN IT IS FOR EXTRACTION of NEW REFERENCE insert '>=' IF NOT '>'
					for c_tag in b.contents :
						if len(c_tag) > 0  and str(c_tag) != "\n" and c_tag != " ":
							
							if (c_tag != c_tag.string) :	#'if : si il y a des balises'
								wordExtr = self._extract_tags(c_tag, 1)
								if len(wordExtr) > 0:
									instanceWords = self._buildWords(wordExtr)
									words.extend(instanceWords)
							else :							#else : si il n y a pas de balise donc : nolabel
								c_tag_str = string.split(c_tag)
								if len(c_tag_str) > 0 and c_tag_str != "\n" :
									for ss in c_tag_str :
										words.append(Word(ss.encode('utf8'), ["nolabel"]))
	
					if b.find('relateditem') :					# related item
						#print b
						i += 1
						br =  s[i]
	
						allTags = br.findAll(True)					#extract all tags in the current bibl

						for c_tag in br.contents :
							if len(c_tag) > 0  and str(c_tag) != "\n" and c_tag != " " :
								if (c_tag != c_tag.string) :
									wordExtr = self._extract_tags(c_tag, 1)
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
							
				references.append(Reference(words,i))
				i += 1
						
		except IOError:
			pass
			print 'reading error input file\n\n'
			return references
			
		return references
		