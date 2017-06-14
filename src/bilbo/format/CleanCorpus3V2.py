# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 16:09:37 2016

@author: ollagnier
"""

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
import os

class CleanCorpus3V2(Clean):
    
    def __init__(self, options):
        Clean.__init__(self)
        self.tagAttDict = {'0000': 0}
        self.options = options
        

    def processing (self, fname, nameTagCorpus, external) :
        try :
            references = []
            tmp_str = ''
            for line in open (fname, 'r', encoding='utf8', errors='replace') :
                line = re.sub(' ', ' ', line)
                line = line.replace('<!-- <pb/> -->', '')
                line = line.replace('“', '“ ')
                line = line.replace('”', ' ”')
                line = line.replace('\'\'', ' " ')
                line = line.replace('&amp;nbsp;', '&nbsp;')
                tmp_str = tmp_str + ' ' + line
                
            tmp_str = self._elimination (tmp_str)
            tmp_str = self._xmlEntitiesDecode(tmp_str)
            soup = BeautifulSoup (tmp_str, "lxml")
            i = 0
            list_bibl=[]
            s = soup.findAll (nameTagCorpus)
            for bibl in s:
                if bibl.parent.name == 'p':
                    list_bibl.append(bibl)
            if len(list_bibl) > 15000:
                print("Attention : there are more than 15 000 references in a file so that it uses too much memory (divide the references in several different files)")
                return
                
            while i < len(list_bibl) :
                words = []
                b = list_bibl[i]
                if i == 639:
                    pass
                allTags = b.findAll(True)
                limit = 0
                if external == 1 : limit = 0
                if len(allTags) >= limit :
                    for c_tag in b.contents :
                        if len(c_tag) > 0  and c_tag != "\n" and c_tag != " " :
                            if (c_tag != c_tag.string) :
                                wordExtr = self._extract_tags(c_tag, 1)
                                if len(wordExtr) > 0:
                                    instanceWords = self._buildWords(wordExtr)
                                    words.extend(instanceWords)
                            else :
                                c_tag_str = string.split(c_tag)
                                if len(c_tag_str) > 0 and c_tag_str != "\n" :
                                    for ss in c_tag_str :
                                        words.append(Word(ss, ["nolabel"]))
                    if b.find('relateditem') or b.find(nameTagCorpus) :
                        i += 1
                        
                references.append(Reference(words,i))
                i += 1
                        
                
        except IOError:
            pass
            print('reading error \n\n')
            return references

        return references
	
