# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Wed Sep 28 14:37:34 2016

@author: ollagnier
"""

from bs4 import BeautifulSoup
from bilbo.reference.Word import Word
from bilbo.reference.Reference import Reference
from bilbo.format.Clean import Clean
from codecs import open
import string
import re

class CleanCorpus3(Clean):
    
    def __init__(self, options):
        Clean.__init__(self)
        self.tagAttDict = {'0000': 0}
        self.options = options
	
    def processing (self, fname, nameTagCorpus, external) :
        refSign = []
        precitSign = []
        references = []
        
        try :
            tmp_str = ''
            for line in open (fname, 'r', encoding='utf8', errors='replace') :
                
                line = re.sub(' ', ' ', line)
                line = re.sub('<note.*?>.*?</note>', '', line)
                line = line.replace('<!-- <pb/> -->', '')
                line = line.replace('“', '“ ')
                line = line.replace('”', ' ”')
                line = line.replace('\'\'', ' " ')
                line = line.replace('&amp;nbsp;', '&nbsp;')
                line = self.posssign(line, refSign)
                line = self.posssign(line, precitSign)
                tmp_str = tmp_str + ' ' + line
                #print('LINE :' + tmp_str)
                
            tmp_str = self._elimination (tmp_str)
            tmp_str = self._xmlEntitiesDecode(tmp_str)
            tmp_str = tmp_str.replace("\n", "")
            soup = BeautifulSoup (tmp_str, "lxml")

            for nt in soup.findAll ('p') :
                c = 0
                
                for nt_c in nt.contents :
                    'verify if the note has a reference'
                    if nt_c == nt_c.string :
                        pass
                    elif nt_c.name == 'bibl' :
                        pass
                    elif nt_c.findAll('bibl') : 
                        nsoup = BeautifulSoup (nt_c.renderContents(), "lxml")
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
                #print('Paragraphe with Ref')
                #print(sAll)
                words = []
                #Filter the non-annotated notes for training, if we don't use SVM, just select notes including bibls
                validNote = True
                if self.options.T and not self.options.v and len(s) == 0 : validNote = False
                
                while i < len(sAll) and validNote :
                    if i == 20:
                        pass
                    b = sAll[i]
                    
                    if b != b.string :
                        allTags = b.findAll(True)
                        limit = 1
                        if external == 1 : limit = 0
                            
                        if len(allTags) >= limit :
                            for c_tag in b.contents :
                                if len(c_tag) > 0  and c_tag != "\n" and c_tag != " " :
                                    if (c_tag != c_tag.string) :
                                        wordExtr = self._extract_tags(c_tag, len(s))
                                        if len(wordExtr) > 0:
                                            instanceWords = self._buildWords(wordExtr)
                                            words.extend(instanceWords)
                                    else :	
                                        c_tag_str = string.split(c_tag)
                                        if len(c_tag_str) > 0 and c_tag_str != "\n" :
                                            for ss in c_tag_str :
                                                if len(s) > 0 :
                                                    words.append(Word(ss, ["nolabel"]))
                                                else:
                                                    words.append(Word(ss, ["nonbibl"]))
                            if b.find('relateditem') :
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
            print('reading error\n\n')
            return references

        return references
