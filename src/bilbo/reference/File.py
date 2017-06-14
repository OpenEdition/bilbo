# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bs4 import BeautifulSoup, NavigableString
from bilbo.format.Clean import Clean
from bilbo.format.CleanCorpus1 import CleanCorpus1
from bilbo.format.CleanCorpus2 import CleanCorpus2
from bilbo.format.CleanCorpus3 import CleanCorpus3
from bilbo.format.CleanCorpus3V2 import CleanCorpus3V2
from bilbo.format.Rule import Rule
from bilbo.reference.ListReferences import ListReferences
from bilbo.output.identifier import extractDoi, loadTEIRule, toTEI, teiValidate
from bilbo.reference import tagtool
from xml.dom.minidom import parseString
from codecs import open
import copy
import re, sys
import os.path
import glob, os

specialPunc =  {'«':0, '»':0, '“':0, '”':0, '"':0, '–':0, '-':0}
prePtrlimit = -1
postPtrlimit = -1

class File(object):
    
    def __init__(self, fname, options):
        self.nom = fname
        self.corpus = {}
        self.options = options
        
    def extract(self, typeCorpus, tag, external):
        clean = Clean()
        if typeCorpus == 1:
            clean = CleanCorpus1(self.options)
        if typeCorpus == 2:
            clean = CleanCorpus2(self.options)
        elif typeCorpus == 3:
            clean = CleanCorpus3(self.options)
        references = clean.processing(self.nom, tag, external)
        if len(references) >= 1:
            self.corpus[typeCorpus] = ListReferences(references, typeCorpus)
            rule = Rule(self.options)
            rule.reorganizing(self.corpus[typeCorpus])
    
    def extractBibl(self, typeCorpus, tag, external, dirResult):
        clean = Clean()
        if typeCorpus == 3:
            clean = CleanCorpus3V2(self.options)
        #clean.postprocess(self.nom)
        references = clean.processing(self.nom, tag, external)
        if len(references) >= 1:
            self.corpus[typeCorpus] = ListReferences(references, typeCorpus)
            rule = Rule(self.options)
            rule.reorganizing(self.corpus[typeCorpus])
    


    def getListReferences(self, typeCorpus):
        try:
            return self.corpus[typeCorpus]
        except :
            return -1


    def nbReference(self, typeCorpus):
        try:
            return self.corpus[typeCorpus].nbReference()
        except :
            return 0


    def buildReferences(self, references, tagTypeCorpus, dirResult):
        cptRef = 0
        tmp_str = ""
        ref_ori = []
        for line in open (self.nom, 'r', encoding='utf8') :
            tmp_str = tmp_str + line
            
        soup = BeautifulSoup (tmp_str, "lxml")
        s = soup.findAll (tagTypeCorpus)
        
        basicTag = {}
        for ss in s :
            for sss in ss.find_all() :
                basicTag[sss.name] = 1
                
        tagConvert = {}
        tagConvert = loadTEIRule(tagConvert)
        
        includedLabels = {}
        for ref in references:
            for reff in ref.find_all() :
                includedLabels[reff.name] = 1
                try : del basicTag[reff.name]
                except : pass 
            parsed_soup = ''.join(s[cptRef].findAll(text = True))
            ptr = 0
            if (len(parsed_soup.split()) > 0) :
                oriRef = (unicode(s[cptRef]))
                oriRef = self._cleanTags(oriRef)
                
                if self.options.o == 'simple' :
                    parsed_soup = parsed_soup.replace('&', "&amp;")
                    parsed_soup = parsed_soup.replace('<pb/>', '')
                    parsed_soup = parsed_soup.replace('<', "&lt;")
                    parsed_soup = parsed_soup.replace('>', "&gt;")
                    oriRef = '<'+tagTypeCorpus+'>'+parsed_soup+'</'+tagTypeCorpus+'>'
                for r in ref.contents :
                    ck = 0
                    try : r.name
                    except : ck = 1
                    if ck == 0 and not r.name == "c" and r.string :
                        r.string = r.string.replace('&', "&amp;")
                        for token in r.string.split() :
                            pre_ptr = ptr
                            ptr = oriRef.find(token, ptr)
                            while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) and oriRef.find("<", ptr) > 0 :
                                ptr = oriRef.find(token, ptr+1)
                            if oriRef.find("<", ptr) < 0 : ptr = -1
                                
                            inner_string = ""
                            if ptr >= 0 :
                                tmp_str2 = oriRef[pre_ptr:ptr]
                                if tmp_str2 != '.':
                                    soup2 = BeautifulSoup (tmp_str2, "lxml")
                                    for s2 in soup2 :
                                        try : inner_string = ''.join(s2.findAll(text = True))
                                        except : pass
                                else:
                                    inner_string = tmp_str2
                                    
                            if (ptr < 0) or inner_string.find(token) >= 0 :
                                c = token[0]
                                ptr = oriRef.find(c, pre_ptr)
                                while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) :
                                    ptr = oriRef.find(c, ptr+1)
                                ptr_start = ptr
                                newtoken = ""
                                if (oriRef.find("</", ptr) < oriRef.find(">", ptr)) :
                                    tag_start_l = oriRef.find("<",ptr_start)
                                    tag_start_r = oriRef.find(">",tag_start_l)
                                    newtoken = oriRef[ptr_start:tag_start_l]
                                    mtoken_r = oriRef.find(token[len(token)-1],tag_start_r)
                                    newtoken += oriRef[tag_start_r+1:mtoken_r+1]
                                    ptr_start = ptr_start - oriRef[ptr_start:pre_ptr:-1].find("<",0)
                                    ptr_end = mtoken_r
                                else :
                                    tag_start_l = oriRef.find("<",ptr_start)
                                    tag_start_r = oriRef.find(">",tag_start_l)
                                    tag_end_l = oriRef.find("<",tag_start_r)
                                    tag_end_r = oriRef.find(">",tag_end_l)
                                    ptr_end = tag_end_r
                                    newtoken = oriRef[ptr_start:tag_start_l]+oriRef[tag_start_r+1:tag_end_l]
                                    newtoken = re.sub(' ', ' ', newtoken, flags=re.UNICODE)
                                    newtoken = newtoken.lstrip()
                                    newtoken = newtoken.rstrip()
                                if newtoken == token or newtoken.find(token) >= 0:
                                    token = oriRef[ptr_start:ptr_end+1]
                                    ptr = ptr_start
                                else :
                                    print(pre_ptr, ptr, '*'+newtoken+'*', token)
                                    print("PROBLEM, CANNOT FIND THE TOKEN", token)
                                    ptr = -1
                                    pass
                            else :
                                while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) :
                                    ptr = oriRef.find(token, ptr+1)
                            if (ptr >= 0) and token[:2] != '</' :
                                if token != None:
                                    nstr = "<"+r.name+">"+token+"</"+r.name+">"
                                    oriRef = oriRef[:ptr] + nstr + oriRef[ptr+len(token):]
                                    ptr += len(nstr)
                            else :
                                ptr = pre_ptr       
                oriRef = BeautifulSoup (oriRef, "lxml")
                oriRef = unicode(oriRef.body.contents[0])
                oriRef = self.continuousTags(basicTag, includedLabels, oriRef)
                oriRef = self.arrangeTagsPerToken(includedLabels, oriRef, tagTypeCorpus)
                oriRef = self.checkHiTag(oriRef, includedLabels)
                beforeRef = oriRef
                oriRef = oriRef.replace('&ndash;', '&#8211;')
                oriRef = oriRef.replace('&nbsp;', '&#160;')
                oriRef = oriRef.replace('&mdash;', '-')
                if oriRef.find("<author>") < 0 :
                    oriRef, noCutRef= self.findAuthor(includedLabels, oriRef)
                    oriRef = self.correctMissTag(oriRef, basicTag, "author")
                    #if tagTypeCorpus == 'note' or tagTypeCorpus == 'p':
                    if tagTypeCorpus == 'note':
                        oriRef = self.detectBibl(oriRef, includedLabels)
                        try : parseString(oriRef)
                        except Exception, err:
                            print(err, self.nom, oriRef.encode('utf8'))
                            pass
                if self.options.o == 'tei' :
                    oriRef = toTEI(oriRef, tagConvert)
                ref_ori.append(oriRef)
            cptRef += 1
            
        try:
            if self.options.o == 'simple' : tmp_str = self.writeResultOnly(ref_ori, references, tagTypeCorpus)
            else : tmp_str = self.writeResultInOriginal(tmp_str, soup, ref_ori, references, tagTypeCorpus)
        except Exception, err:
            print(err)
            print("ERROR : could not finish write of orgininal")
            pass
        
        fich = open(dirResult+'/'+self._getName(), "w", encoding='utf8')
        fich.write(tmp_str)
        fich.close()
        
        self.schemaValidation(len(references), dirResult)
        return
        
    def buildReferencesWithoutSVM(self, references, tagTypeCorpus, dirResult):
        cptRef = 0
        tmp_str = ""
        ref_ori = []
        for line in open (self.nom, 'r', encoding='utf8') :
            tmp_str = tmp_str + line
            
        soup = BeautifulSoup (tmp_str, "lxml")
        s = soup.findAll (tagTypeCorpus)
        
        basicTag = {}
        for ss in s :
            for sss in ss.find_all() :
                basicTag[sss.name] = 1
                
        tagConvert = {}
        tagConvert = loadTEIRule(tagConvert)
        
        includedLabels = {}
        for ref in references:
            for reff in ref.find_all() :
                includedLabels[reff.name] = 1
                try : del basicTag[reff.name]
                except : pass 
            parsed_soup = ''.join(s[cptRef].findAll(text = True))
            ptr = 0
            if (len(parsed_soup.split()) > 0) :
                oriRef = (unicode(s[cptRef]))
                oriRef = self._cleanTags(oriRef)
                
                if self.options.o == 'simple' :
                    parsed_soup = parsed_soup.replace('&', "&amp;")
                    parsed_soup = parsed_soup.replace('<pb/>', '')
                    parsed_soup = parsed_soup.replace('<', "&lt;")
                    parsed_soup = parsed_soup.replace('>', "&gt;")
                    oriRef = '<'+tagTypeCorpus+'>'+parsed_soup+'</'+tagTypeCorpus+'>'
                for r in ref.contents :
                    ck = 0
                    try : r.name
                    except : ck = 1
                    if ck == 0 and not r.name == "c" and r.string :
                        r.string = r.string.replace('&', "&amp;")
                        for token in r.string.split() :
                            pre_ptr = ptr
                            ptr = oriRef.find(token, ptr)
                            while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) and oriRef.find("<", ptr) > 0 :
                                ptr = oriRef.find(token, ptr+1)
                            if oriRef.find("<", ptr) < 0 : ptr = -1
                                
                            inner_string = ""
                            if ptr >= 0 :
                                tmp_str2 = oriRef[pre_ptr:ptr]
                                if tmp_str2 != '.':
                                    soup2 = BeautifulSoup (tmp_str2, "lxml")
                                    for s2 in soup2 :
                                        try : inner_string = ''.join(s2.findAll(text = True))
                                        except : pass
                                else:
                                    inner_string = tmp_str2
                                    
                            if (ptr < 0) or inner_string.find(token) >= 0 :
                                c = token[0]
                                ptr = oriRef.find(c, pre_ptr)
                                while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) :
                                    ptr = oriRef.find(c, ptr+1)
                                ptr_start = ptr
                                newtoken = ""
                                if (oriRef.find("</", ptr) < oriRef.find(">", ptr)) :
                                    tag_start_l = oriRef.find("<",ptr_start)
                                    tag_start_r = oriRef.find(">",tag_start_l)
                                    newtoken = oriRef[ptr_start:tag_start_l]
                                    mtoken_r = oriRef.find(token[len(token)-1],tag_start_r)
                                    newtoken += oriRef[tag_start_r+1:mtoken_r+1]
                                    ptr_start = ptr_start - oriRef[ptr_start:pre_ptr:-1].find("<",0)
                                    ptr_end = mtoken_r
                                else :
                                    tag_start_l = oriRef.find("<",ptr_start)
                                    tag_start_r = oriRef.find(">",tag_start_l)
                                    tag_end_l = oriRef.find("<",tag_start_r)
                                    tag_end_r = oriRef.find(">",tag_end_l)
                                    ptr_end = tag_end_r
                                    newtoken = oriRef[ptr_start:tag_start_l]+oriRef[tag_start_r+1:tag_end_l]
                                    newtoken = re.sub(' ', ' ', newtoken, flags=re.UNICODE)
                                    newtoken = newtoken.lstrip()
                                    newtoken = newtoken.rstrip()
                                if newtoken == token or newtoken.find(token) >= 0:
                                    token = oriRef[ptr_start:ptr_end+1]
                                    ptr = ptr_start
                                else :
                                    print(pre_ptr, ptr, '*'+newtoken+'*', token)
                                    print("PROBLEM, CANNOT FIND THE TOKEN", token)
                                    ptr = -1
                                    pass
                            else :
                                while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) :
                                    ptr = oriRef.find(token, ptr+1)
                            if (ptr >= 0) and token[:2] != '</' :
                                if token != None:
                                    nstr = "<"+r.name+">"+token+"</"+r.name+">"
                                    oriRef = oriRef[:ptr] + nstr + oriRef[ptr+len(token):]
                                    ptr += len(nstr)
                            else :
                                ptr = pre_ptr       
                oriRef = BeautifulSoup (oriRef, "lxml")
                oriRef = unicode(oriRef.body.contents[0])
                oriRef = self.continuousTags(basicTag, includedLabels, oriRef)
                oriRef = self.arrangeTagsPerToken(includedLabels, oriRef, tagTypeCorpus)
                oriRef = self.checkHiTag(oriRef, includedLabels)
                beforeRef = oriRef
                oriRef = oriRef.replace('&ndash;', '&#8211;')
                oriRef = oriRef.replace('&nbsp;', '&#160;')
                oriRef = oriRef.replace('&mdash;', '-')
                if oriRef.find("<author>") < 0 :
                    oriRef, noCutRef= self.findAuthor(includedLabels, oriRef)
                    oriRef = self.correctMissTag(oriRef, basicTag, "author")
                    #if tagTypeCorpus == 'note' or tagTypeCorpus == 'p':
                    if tagTypeCorpus == 'p':
                        oriRef = self.detectBibl(oriRef, includedLabels)
                        try : parseString(oriRef)
                        except Exception, err:
                            print(err, self.nom, oriRef.encode('utf8'))
                            pass
                if self.options.o == 'tei' :
                    oriRef = toTEI(oriRef, tagConvert)
                ref_ori.append(oriRef)
            cptRef += 1
            
        try:
            if self.options.o == 'simple' : tmp_str = self.writeResultOnly(ref_ori, references, tagTypeCorpus)
            else : tmp_str = self.writeResultInOriginal(tmp_str, soup, ref_ori, references, tagTypeCorpus)
        except Exception, err:
            print(err)
            print("ERROR : could not finish write of orgininal")
            pass
        
        fich = open(dirResult+'/'+self._getName(), "w", encoding='utf8')
        fich.write(tmp_str)
        fich.close()
        
        self.schemaValidation(len(references), dirResult)
        return
        
    def buildReferencesP(self, references, tagTypeCorpus, dirResult):
        dirResultRoot = os.path.abspath(os.path.join(dirResult, os.path.pardir))+'/'
        dirResult_Bibl = dirResultRoot+'test/corpus_JustBibl/'
        cptRef = 0
        tmp_str = ""
        ref_ori = []
        for file in glob.glob(dirResult_Bibl+"*.xml"):
            for line in open (file, 'r', encoding='utf8') :
                tmp_str = tmp_str + line
        soup = BeautifulSoup (tmp_str, 'lxml')
        s = soup.findAll ('bibl')
        for ele in s:
            if ele.parent.name == 'p':
                ref_ori.append(ele.text)
        for bibl in s :
            if bibl.parent.name == 'p':
                bibl.replaceWith(references[cptRef])
                cptRef  = cptRef + 1
        fich = open(dirResult+'/'+self._getName(), "w", encoding='utf8')
        fich.write(soup.prettify())
        fich.close()

        return

    def schemaValidation(self, numReferences, dirResult):
        if self.options.v in ['output', 'all'] :
            if self.options.o == 'tei' and numReferences > 0 :
                try :
                    valide, numErr = teiValidate(dirResult+self._getName(), 'output')
                    if not valide :
                        valide, numErrOri = teiValidate(self.nom, 'output')
                        if numErr == numErrOri : print("Original file also has", numErr, "errors. Annotation OK.")
                        else : print("Original file has", numErrOri, "errors. Annotation NOT OK.")
                except Exception, err:
                    print(err)
        return

    def writeResultInOriginal(self, tmp_str, soup, ref_ori, references, tagTypeCorpus):
        cpt = 0
        listRef = soup.findAll(tagTypeCorpus)
        
        pre_p1 = 0
        for ref in listRef:
            contentString =""
            for rf in ref.contents :
                if rf == rf.string : contentString += rf
                    
            for tag in ref.findAll(True) :
                if len(tag.findAll(True)) == 0 and len(tag.contents) > 0 :
                    for con in tag.contents :
                        contentString += con
                        
            p1 = tmp_str.find('<'+tagTypeCorpus+'>', pre_p1+10)
            p11 = tmp_str.find('<'+tagTypeCorpus+' ', pre_p1+10)
            if p1 < 0 or (p11 > 0 and p1 > p11) : p1 = p11
            p2 = tmp_str.find('</'+tagTypeCorpus+'>', p1)
            
            if len(contentString.split()) > 0 :
                text = ref_ori[cpt]
                text = self.doiExtraction(text, references[cpt], tagTypeCorpus)
                tmp_list = list(tmp_str)
                tmp_list[p1:p2+len('</'+tagTypeCorpus+'>')] = text
                tmp_str = ''.join(tmp_list)
                
            cpt += 1
            pre_p1 = p1
            
        return tmp_str


    def writeResultOnly(self, ref_ori, references, tagTypeCorpus) :
        tmp_str = '<list'+tagTypeCorpus.title()+'>\n'
        for i, r in enumerate(ref_ori) :
            text = ref_ori[i]
            text = self.doiExtraction(text, references[i], tagTypeCorpus)
            tmp_str += text+'\n'
        tmp_str += '</list'+tagTypeCorpus.title()+'>\n'
        return tmp_str


    def doiExtraction(self, text, reference, tagTypeCorpus):
        doistring = ''
        if self.options.d :
            doistring = extractDoi(unicode(reference), tagTypeCorpus)
            if doistring != '' :
                doistring = 'http://dx.doi.org/'+doistring
                doistring = '<idno type=\"DOI\">'+doistring+'</idno>'
                ptr1 = text.find('</title>')+len('</title>')
                text = text[:ptr1] + doistring + text[ptr1:]
        return text


    def continuousTags(self, basicTag, includedLabels, oriRef):
        preTag = ""
        noncontinuousck = ["surname", "forename"]
        newsoup = BeautifulSoup(oriRef, "lxml")
        ptr2 = 0
        ptr1 = 0
        found = {}
        preparentname = ""
        for ns in newsoup.find_all() :
            if preTag == ns.name and preparentname == ns.parent.name and not preTag in noncontinuousck:
                ptr1 = oriRef.find("</"+preTag+">", ptr2)
                ptr2 = oriRef.find("<"+preTag+">", ptr1)
                if ptr2 > ptr1 and oriRef.find(">", ptr1+len("</"+preTag+">"), ptr2) < 0 :
                    token = "</"+preTag+">"
                    oriRef = oriRef[:ptr1] + oriRef[ptr1+len(token):]
                    token = "<"+preTag+">"
                    ptr = oriRef.find(token, ptr1)
                    oriRef = oriRef[:ptr] + oriRef[ptr+len(token):]
                    found[ns.name] = 0
                    for k in found.keys():
                        if k == ns.name : found[k] = 0
                        else : found[k] = 1
                ptr2 = ptr1+1
            else :
                if (found.has_key(ns.name) and found[ns.name] == 0) or (preTag == ns.name and preparentname != ns.parent.name and not preTag in noncontinuousck) :
                    ptr1 = oriRef.find("</"+ns.name+">", ptr2)
                    ptr2 = oriRef.find("<"+ns.name+">", ptr1)
                    if ptr2 < 0 : ptr2 = ptr1+1
                    for k in found.keys():
                        if k == ns.name : found[k] = 0
                        else : found[k] = 1
                found[ns.name] = 0
            preTag = ns.name
            preparentname = ns.parent.name
            
        return oriRef


    def arrangeTagsPerToken(self, includedLabels, oriRef, tagTypeCorpus):
        nameck = ["surname", "forename", "namelink", "genname"]
        for tmpTag in includedLabels :
            ptr2 = 0
            ptr1 = oriRef.find('<'+tmpTag+'>', ptr2)
            while ptr1 > 0 :
                ptr2 = oriRef.find('</'+tmpTag+'>', ptr1)+len('</'+tmpTag+'>')
                ptr3 = oriRef.find('</',ptr2)
                closeTag = ''
                if oriRef.find('<',ptr2,ptr3) < 0 and self._onlyPunc(oriRef[ptr2:ptr3]) :
                    ptr4 = oriRef.find('>',ptr3)
                    closeTag = oriRef[ptr3+len('</'):ptr4]
                    if closeTag not in ["note", "bibl", "listNote", "listBibl", "ref", "p"] and closeTag not in includedLabels :
                        [st1, ed1, dummyTag] = tagtool._closestPreTag(oriRef, ptr1)
                        if oriRef[st1:ed1].find('<'+closeTag) == 0 and self._onlyPunc(oriRef[ed1:ptr1]) :
                            tmpRef = tagtool._moveSecondTag(oriRef, st1, ed1, ptr1, ptr1+len('<'+tmpTag+'>'))
                            tmpRef = tagtool._moveFirstTag(tmpRef, ptr2-len('</'+tmpTag+'>'), ptr2, ptr3, ptr4+1)
                            oriRef = tmpRef
                ptr1 = oriRef.find('<'+tmpTag+'>', ptr2)
                
        oriRef = self._continuousTagck(includedLabels, nameck, oriRef)
        st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'ref', 0)
        while(st1 >= 0) :
            centre = oriRef[ed1:st2]
            if centre.find("<") >= 0 and centre.find(">") > 0 :
                ns = BeautifulSoup(centre, "lxml")
                found = []
                for n in ns.find_all() :
                    if n.name in includedLabels : found.append(n.name)
                for f in found :
                    oriRef = tagtool._deleteTag(oriRef, f, ed1)
                    ed2 -= 2*len(f)+len('<></>')
            st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'ref', ed2)
            
        return oriRef


    def _continuousTagck(self, includedLabels, nameck, oriRef):
        tmp_str = oriRef
        for tmpTag in includedLabels :
            if tmpTag not in nameck :
                st1 = tmp_str.find('</'+tmpTag+'>', 0)
                while st1 >= 0:
                    ed1 = tmp_str.find('>', st1) + 1
                    st2 = tmp_str.find('<'+tmpTag+'>', st1)
                    ed2 = tmp_str.find('>', st2) + 1
                    if st2>=0 and self._onlyPunc(tmp_str[ed1:st2]) :
                        tmp_str = tmp_str[:st1]+tmp_str[ed1:st2]+tmp_str[ed2:]
                    st1 = tmp_str.find('</'+tmpTag+'>', st1+1)
        return tmp_str


    def _onlyPunc(self, tmp_str):
        new_str = tmp_str.replace(' ', ' ')
        for key in specialPunc.iterkeys(): new_str = new_str.replace(key, ' ')
        new_str = re.sub('\W', ' ', new_str, flags=re.UNICODE)
        onlyPunc = False
        if len(new_str.split()) == 0:
            onlyPunc = True
        return onlyPunc
        
    def _getName(self):
        chemin = self.nom.split("/")
        return chemin.pop()
        
    def _cleanTags(self, oriRef):
        target_tag_st = "<hi xml:lang=\""
        target_tag_mi = ">"
        target_tag_end = "</hi>"
        tmpRef = oriRef
        a = tmpRef.find(target_tag_st,0)
        while a > 0 :
            b = tmpRef.find(target_tag_mi, a + len(target_tag_st))
            c = tmpRef.find(target_tag_end, b)
            d = c + len(target_tag_end)
            if re.match('<hi xml:lang=\"\w\w\">', tmpRef[a:b+1], flags=re.UNICODE) :
                tmpRef = tmpRef[:a]+tmpRef[b+1:c]+tmpRef[d:]
                e = d-len('<hi xml:lang=\"AA\"></hi>')
                if e > 0 : a = tmpRef.find(target_tag_st, e)
                else : a = tmpRef.find(target_tag_st, 0)
            else :
                a = tmpRef.find(target_tag_st,d)
        tmpRef = self._cleanHiTagSpecific(tmpRef)
        
        return tmpRef
        
    def _cleanHiTagSpecific(self, tmpRef):
        hiStrings = ['<hi rend="subtitle1">', '<hi rend="st">', '<hi rend="apple-style-span">']
        target_tag_end = "</hi>"
        for hiString in hiStrings :
            a = tmpRef.find(hiString,0)
            while a > 0 :
                b = a + len(hiString)
                c = tmpRef.find(target_tag_end, b)
                d = c + len(target_tag_end)
                centre = tmpRef[b+1:c]
                cntHi = centre.count("<hi")
                if cntHi > 0 :
                    for i in range(cntHi) :
                        c = tmpRef.find(target_tag_end, d)
                        d = c + len(target_tag_end)
                tmpRef = tmpRef[:a]+tmpRef[b:c]+tmpRef[d:]
                e = d-len(hiString)-len(target_tag_end)
                a = tmpRef.find(hiString, e)
        return tmpRef



    def checkHiTag(self, oriRef, includedLabels):
        refLabels = []
        hasTitle = False
        soup = BeautifulSoup(oriRef, "lxml")
        for s in soup.find_all() :
            if s.name in includedLabels :
                refLabels.append(s.name)
                if (s.name).find("title") == 0 : hasTitle = True
        nameck = ["surname", "forename", "namelink", "genname"]
        canDelete = ["abbr", "w", "bookindicator", "nolabel", "nonbibl"]
        
        target_tag_st = "<hi"
        target_tag_mi = ">"
        target_tag_end = "</hi>"
        tmpRef = oriRef
        a = tmpRef.find(target_tag_st,0)
        while a > 0 and tmpRef[a:].find('<hi rend="Endnote">') != 0 :
            b = tmpRef.find(target_tag_mi, a + len(target_tag_st))
            c = tmpRef.find(target_tag_end, b)
            d = c + len(target_tag_end)
            
            centre = tmpRef[b+1:c]
            cntHi = centre.count("<hi")
            if cntHi > 0 :
                for i in range(cntHi) :
                    c = tmpRef.find(target_tag_end, d)
                    d = c + len(target_tag_end)
                    
            centre = tmpRef[b+1:c]
            if centre.find("<") < 0 and centre.find(">") < 0 :
                a = tmpRef.find(target_tag_st,d)
            else :
                ns = BeautifulSoup(centre, "lxml")
                found = []
                for n in ns.find_all() :
                    if n.name in includedLabels : found.append(n.name)
                if len(found)  > 1 and len(list(set(found))) == 1 :
                    new_str = self._continuousTagck(includedLabels, [], tmpRef[a:d])
                    tmpRef = tmpRef[:a]+new_str+tmpRef[d:]
                    found = [found[0]]
                    c = tmpRef.find(target_tag_end, b)
                    d = c + len(target_tag_end)
                    
                if len(found) == 1 :
                    tagName = found[0]
                    if tagName.find("title") == 0 :
                        tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
                    else :
                        st1, ed1, st2, ed2 = tagtool._findTagPosition(tmpRef, tagName, a)
                        if self._onlyPunc(tmpRef[b+1:st1]) and self._onlyPunc(tmpRef[ed2:c]) :
                            tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
                        else :
                            tmp_centre = tagtool._deleteTag(centre, tagName, 0)
                            if len(tmp_centre.split()) == 2 :
                                tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
                            else :
                                for f in found :
                                    tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
                                    d -= 2*len(f)+len('<></>')
                                    
                else :
                    cntT = 0
                    cntN = 0
                    tagName = ''
                    for f in found :
                        if f.find("title") == 0 :
                            tagName = f
                            cntT += 1
                        if f in nameck+['nolabel', 'abbr'] : cntN += 1
                    if cntT == 1 :
                        tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
                        for f in found :
                            if f != tagName :
                                tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
                                d -= 2*len(f)+len('<></>')
                                
                    elif cntT > 1 :
                        if cntT == len(found) :
                            tmpRef = tagtool._exchangeTagPairs(tmpRef, found[0], a, b+1, c, d)
                            for f in found[1:] :
                                tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
                                d -= 2*len(f)+len('<></>')
                        else :
                            tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
                            for f in found :
                                tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
                                d -= 2*len(f)+len('<></>')
                    elif len(found) > 0 and cntN == len(found) :
                        tmp_centre = centre
                        for f in found : tmp_centre = tagtool._deleteTag(tmp_centre, f, 0)
                        if len(tmp_centre.split()) > len(found) :
                            for f in found :
                                tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
                                d -= 2*len(f)+len('<></>')
                        else :
                            hiString = tmpRef[a:b+1]
                            if hiString == '<hi font-variant="small-caps">' or hiString == '<hi rend="bold">' :
                                tmpRef = tagtool._devideHi(tmpRef, found, hiString, a)
                                d = a
                            elif not hasTitle :
                                tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
                            else :
                                isName = tagtool._isName(tmpRef, centre, found, includedLabels, a)
                                if isName :
                                    hiString = tmpRef[a:b+1]
                                    tmpRef = tagtool._devideHi(tmpRef, found, hiString, a)
                                    d = a
                                else :
                                    tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
                    else :
                        if len(found) == 0 : pass
                        else :
                            allDelete = True
                            for f in found :
                                if f not in canDelete : allDelete = False
                            if allDelete :
                                for f in found :
                                    tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
                                    d -= 2*len(f)+len('<></>')
                            else :
                                isPublisher = False
                                if found == ['place','publisher','abbr'] : isPublisher = True
                                if not hasTitle or not tagtool._hasTitleAfterSemi(tmpRef, a, d) :
                                    tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
                                elif isPublisher :
                                    hiString = tmpRef[a:b+1]
                                    tmpRef = tagtool._devideHi(tmpRef, found, hiString, a)
                                    d = a
                                else :
                                    tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
									
             
            a = tmpRef.find(target_tag_st,d)
        tmpRef = self._continuousTagck(includedLabels, nameck, tmpRef)
        return tmpRef


    def findAuthor(self, includedLabels, oriRef):
        preTag = ""
        continuousck = ["surname", "forename", "namelink", "genname"]
        group = []
        newsoup = BeautifulSoup(oriRef, "lxml")
        tmp_group = []
        for ns in newsoup.find_all() :
            if ns.name in continuousck :
                tmp_group.append(ns.name)
            elif ns.name in includedLabels :
                if len(tmp_group) > 0 : group.append(tmp_group)
                tmp_group = []
                
        ptr2 = 0
        noCutRef = ''
        for tmp_group in group :
            if len(tmp_group) >= 1 :
                ptr0 = oriRef.find("<"+tmp_group[0]+">", ptr2)
                oriRef = oriRef[:ptr0] + "<author>" + oriRef[ptr0:]
                for tmp_tag in tmp_group :
                    ptr1 = oriRef.find("<"+tmp_tag+">", ptr2)
                    ptr2 = oriRef.find("</"+tmp_tag+">", ptr1)
                tmp_tag = tmp_group[len(tmp_group)-1]
                ptr2 = ptr2 + len("</"+tmp_tag+">")
                oriRef = oriRef[:ptr2] + "</author>" + oriRef[ptr2:]
                
                noCutRef = oriRef
                
                if len(tmp_group) > 3 :
                    tmp_soup = BeautifulSoup(oriRef[ptr0:ptr2], "lxml")
                    parsed_bs = ''.join(tmp_soup.findAll(text = True))
                    if parsed_bs.find(";") > 0 :
                        ptr1 = oriRef.find(";", ptr0, ptr2)
                        while ptr1 > 0 : [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ";")
                    elif oriRef.find(",", ptr0, ptr2) > 0 :
                        tmp_string = ''.join(BeautifulSoup(oriRef[ptr0:ptr2], "lxml").findAll(text = True))
                        multi = True
                        if oriRef.count(",", ptr0, ptr2) == 1 :
                            for ts in tmp_string.split(",") :
                                if len(ts.split()) == 1 : multi = False
                        if multi :
                            commaCut = True
                            doubleCut = True
                            for ts in tmp_string.split(",") :
                                if len(ts.split()) == 1 : commaCut = False
                                else : doubleCut = False
                            if commaCut :
                                ptr1 = oriRef.find(",", ptr0, ptr2)
                                while ptr1 > 0 : [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
                            elif doubleCut :
                                ptr1 = oriRef.find(",", ptr0, ptr2)
                                if ptr1 > 0 : ptr1 = oriRef.find(",", ptr1+1, ptr2)
                                while ptr1 > 0 :
                                    [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
                                    if ptr1 > 0 : ptr1 = oriRef.find(",", ptr1+1, ptr2)
                            else :
                                prePtr1 = ptr0
                                tmp_fields = tmp_string.split(",")
                                start = True
                                ptr1 = oriRef.find(",", ptr0, ptr2)
                                for tmp in tmp_fields :
                                    if len(tmp.split()) > 1 and ptr1 > 0 :
                                        if oriRef[prePtr1:ptr1].find("<surname>") > 0 and oriRef[prePtr1:ptr1].find("<forename>") > 0 :
                                            prePtr1 = ptr1
                                            [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
                                            start = True
                                        else :
                                            if start :
                                                start = False
                                                prePtr1 = ptr1
                                                ptr1 = oriRef.find(",", ptr1+1, ptr2)
                                            else :
                                                prePtr1 = ptr1
                                                [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
                                                start = True
                                    elif ptr1 > 0 :
                                        if start :
                                            start = False
                                            prePtr1 = ptr1
                                            ptr1 = oriRef.find(",", ptr1+1, ptr2)
                                        else :
                                            prePtr1 = ptr1
                                            [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
                                            start = True
            elif len(tmp_group) == 1 :
                ptr1 = oriRef.find("<"+tmp_group[0]+">", ptr2)
                ptr2 = oriRef.find("</"+tmp_group[0]+">", ptr1)
                
        st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'author', 0)
        while(st1 >= 0) :
            if oriRef[st1:ed2].find('surname') < 0 and oriRef[st1:ed2].find('forename') < 0 :
                oriRef = tagtool._deleteTag(oriRef, 'author', st1)
            st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'author', st1+1)
        oriRef = oriRef.replace('<orgname>', '<author><orgname>')
        oriRef = oriRef.replace('</orgname>', '</orgname></author>')
        
        return oriRef, noCutRef


    def _inserAuthorTag(self, oriRef, ptr1, ptr2, sep):
        valid = False
        if oriRef[ptr1:ptr2].find('<surname>') >= 0 or oriRef[ptr1:ptr2].find('<forename>') >= 0 :
            valid = True
        st, ed, tagName = tagtool._closestPreTag(oriRef, ptr1)
        if tagName == 'hi' :
            p = oriRef.find('<', ptr1)
            if oriRef[p:p+5] == '</hi>' : valid = False
        if valid and oriRef.find(">", ptr1) > oriRef.find("<", ptr1) and oriRef.find("<", ptr1) >= 0 :
            oriRef = oriRef[:ptr1] + "</author>" + oriRef[ptr1:]
            ptr1 = oriRef.find("<", ptr1+len("</author>"+sep), ptr2)
            oriRef = oriRef[:ptr1] + "<author>" + oriRef[ptr1:]
            ptr2 = ptr2 + len("<author></author>")
            ptr1 = oriRef.find(sep, ptr1, ptr2)
        else :
            ptr1 = oriRef.find(sep, ptr1+1, ptr2)
        return oriRef, ptr1, ptr2


    def correctMissTag(self, oriRef, basicTag, addedTag):
        [limited1, limitst2] = tagtool._totallyWrapped(oriRef)
        prePtrlimit = limited1
        postPtrlimit = limitst2
        
        tmpRef = oriRef
        ptr1 = tmpRef.find('<'+addedTag+'>', 0)
        while ptr1 >= 0 :
            ptr2 = tmpRef.find('</'+addedTag+'>', ptr1)
            tagName = ''
            found = []
            st2 = tmpRef.find('</', ptr1, ptr2)
            ed2 = tmpRef.find('>', st2, ptr2)
            if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
            while st2 > 0 and tagName not in found :
                while st2 > 0 and tagName not in basicTag :
                    st2 = tmpRef.find('</', ed2, ptr2)
                    ed2 = tmpRef.find('>', st2, ptr2)
                    if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
                if st2 > 0 :
                    p1 = tmpRef.find('<'+tagName+' ', ptr1, st2)
                    p2 = tmpRef.find('<'+tagName+'>', ptr1, st2)
                    if p1 < 0 and p2 < 0 :
                        [st1, ed1, tagN] = tagtool._preOpeningTag(tmpRef, ptr1, tagName, prePtrlimit)
                        if tagName == tagN :
                            if len((tmpRef[ed1:ptr1+len('<'+addedTag+'>')]).split()) == 1 :
                                tmpRef = tagtool._moveSecondTag(tmpRef, st1, ed1, ptr1, ptr1+len('<'+addedTag+'>'))
                                found.append(tagName)
                            else :
                                tmpstr = tmpRef[ptr2+len('</'+addedTag+'>'):st2]
                                ignored = ["<nolabel>", "</nolabel>", "<abbr>", "</abbr>"]
                                for st in ignored : tmpstr.replace(st,"")
                                if tmpstr.find('<') < 0 :
                                    tmpRef = tagtool._moveFirstTag(tmpRef, ptr1, ptr1+len('<'+addedTag+'>'), st2, ed2+1)
                                    found.append(tagName)
                                else :
                                    print("can't deal it")
                                    print(tmpRef)
                st2 = tmpRef.find('</', ed2, ptr2)
                ed2 = tmpRef.find('>', st2, ptr2)
                if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
                        
            tagName = ''
            found = []
            st2 = tmpRef.find('</', ptr2+1)
            ed2 = tmpRef.find('>', st2)
            if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
            while st2 > 0 and tagName not in found :
                while st2 > 0 and tagName not in basicTag :
                    st2 = tmpRef.find('</', ed2)
                    ed2 = tmpRef.find('>', st2)
                    if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
                if st2 > 0 :
                    p1 = tmpRef.find('<'+tagName+' ', ptr2, st2)
                    p2 = tmpRef.find('<'+tagName+'>', ptr2, st2)
                    if p1 < 0 and p2 < 0 :
                        [st1, ed1, tagN] = tagtool._preOpeningTag(tmpRef, ptr2, tagName, prePtrlimit)
                        if tagName == tagN and st1 > ptr1 :
                            tmpstr = tmpRef[ptr2+len('</'+addedTag+'>'):st2]
                            ignored = ["<nolabel>", "</nolabel>", "<abbr>", "</abbr>"]
                            for st in ignored : tmpstr.replace(st,"")
                            if tmpstr.find('<') < 0 :
                                tmpRef = tagtool._moveFirstTag(tmpRef, ptr2, ptr2+len('</'+addedTag+'>'), st2, ed2+1)
                                found.append(tagName)
                            else :
                                tmpRef = tagtool._moveSecondTag(tmpRef, st1, ed1, ptr2, ptr2+len('</'+addedTag+'>'))
                                found.append(tagName)
                    st2 = tmpRef.find('</', ed2)
                    ed2 = tmpRef.find('>', st2)
                    if st2 > 0 and st2 < postPtrlimit : tagName = tmpRef[st2+len('</'):ed2]
            ptr1 = tmpRef.find('<'+addedTag+'>', ptr2)
        return  tmpRef

    def detectBibl(self, oriRef, includedLabels):
        refLabels = []
        soup = BeautifulSoup(oriRef, "lxml")
        tempLabels = includedLabels
        tempLabels['author'] = 1
        toAdd = ['title_m', 'title_a', 'title_j', 'title_t', 'title_u', 'title_s']
        for k in toAdd : tempLabels[k] = 1
        if tempLabels.has_key('nonbibl') : del tempLabels['nonbibl']
        for s in soup.find_all() :
            if s.name in tempLabels : refLabels.append(s.name)
                
        if refLabels != [] :
            ptr2 = -1
            tagName = refLabels[0]
            ptr1 = oriRef.find("<"+tagName+">", 0)
            oriRef = oriRef[:ptr1] + "<bibl>" + oriRef[ptr1:]
            if tagName == 'author' : ptr2 = oriRef.find("</author>", ptr1)
            for tagName in refLabels[1:] :
                ptr1 = oriRef.find("<"+tagName+">", ptr1+1)
                if tagName == 'author' : ptr2 = oriRef.find("</author>", ptr1)
            ptr1 = oriRef.find("</"+tagName+">", ptr1)
            ptr1 = ptr1+len("</"+tagName+">")
            if ptr2 >= ptr1 : ptr1 = ptr2 +len("</author>")
            oriRef = oriRef[:ptr1] + "</bibl>" + oriRef[ptr1:]
            
        oriRef, case1 = self._separateSemicolonBibl(oriRef, includedLabels)
        if not case1 : oriRef = self._separateNonbiblBibl(oriRef, includedLabels)
        return oriRef


    def _separateSemicolonBibl(self, oriRef, includedLabels):
        validLabels = includedLabels
        toRemove = ['nolabel', 'nonbibl', 'w', 'bookindicator']
        toAdd = ['title_m', 'title_a', 'title_j', 'title_t', 'title_u', 'title_s']
        for k in toRemove :
            if k in validLabels : del validLabels[k]
        for k in toAdd : validLabels[k] = 1
        separateLabels = copy.deepcopy(validLabels)
        nameck = ['surname', 'forename', 'namelink', 'genname', 'author']
        for k in nameck :
            if k in separateLabels : del separateLabels[k]
        case1 = False
        tmp_soup = BeautifulSoup(oriRef, "lxml")
        sub_soup = tmp_soup.find('bibl')
        parsed_bs = ''
        if sub_soup : parsed_bs = ''.join(sub_soup.findAll(text = True))
        if parsed_bs.find(';') > 0 :
            ptr0 = oriRef.find('<bibl>') +len('<bibl>')
            ptr2 = oriRef.find('</bibl>')
            ptr1 = oriRef.find(";", ptr0, ptr2)
            ckend = oriRef.find("<", ptr1, ptr2)
            while ptr1 > 0 :
                centre = BeautifulSoup(oriRef[ptr0:ptr1], "lxml")
                if not oriRef[ckend:].find('</') == 0 :
                    sepBibl = False
                    for cen in centre.find_all() :
                        if cen.name in separateLabels : sepBibl = True
                    if sepBibl :
                        st, ed, preTagName = tagtool._closestPreTag(oriRef, ptr1)
                        if preTagName[1:] in validLabels :
                            tmpRef = oriRef[:ed] + '</bibl>' + oriRef[ed:]
                            st = tmpRef.find('<', ed+len('</bibl>'))
                            ed = tmpRef.find('>', st)
                            postTagName = tmpRef[st+1:ed]
                            while postTagName not in validLabels and st > 0 :
                                st = tmpRef.find('<', ed)
                                ed = tmpRef.find('>', st)
                                postTagName = tmpRef[st+1:ed]
                            if postTagName in validLabels :
                                tmpPtr = tmpRef.find(";", ed, ptr2)
                                if tmpPtr < 0 : tmpPtr = ptr2
                                tmpCentre = BeautifulSoup(tmpRef[st:tmpPtr], "lxml")
                                sepBibl = False
                                for tcen in tmpCentre.find_all() :
                                    if tcen.name in separateLabels : sepBibl = True
                                if sepBibl :
                                    tmpRef = tmpRef[:st] + '<bibl>' + tmpRef[st:]
                                    ptr1 = st
                                    oriRef = tmpRef
                                    case1 = True
                ptr0 = ptr1+1
                ptr1 = oriRef.find(";", ptr1+1, ptr2)
                
        return oriRef, case1


    def _separateNonbiblBibl(self, oriRef, includedLabels):
        validLabels = includedLabels
        toRemove = ['nolabel', 'nonbibl', 'w', 'bookindicator']
        for k in toRemove :
            if k in validLabels : del validLabels[k]
        separateLabels = copy.deepcopy(validLabels)
        nameck = ['surname', 'forename', 'namelink', 'genname', 'author']
        for k in nameck :
            if k in separateLabels : del separateLabels[k]
                
        case2 = False
        tmp_soup = BeautifulSoup(oriRef, "lxml")
        sub_soup = tmp_soup.find('bibl')
        if sub_soup :
            for ss in sub_soup.findAll() :
                if ss.name == 'nonbibl' : case2 = True
            if case2 :
                case2 = False
                st1, limit1, limit2, ed2 = tagtool._findTagPosition(oriRef, 'bibl', 0)
                st1, ed1, st2, ed2 = tagtool._findTagPosition(oriRef, 'nonbibl', limit1)
                while st1 > 0 :
                    preSoup = BeautifulSoup(oriRef[limit1:st1], "lxml")
                    sepBibl = False
                    c = 0
                    for ps in preSoup.find_all() :
                        if ps.name in separateLabels : c+=1
                    if c > 1 : sepBibl = True
                    if sepBibl :
                        st, ed, preTagName = tagtool._closestPreTag(oriRef, st1)
                        if preTagName[1:] in validLabels :
                            tmpRef = oriRef[:ed] + '</bibl>' + oriRef[ed:]
                            st = tmpRef.find('<', ed2)
                            ed = tmpRef.find('>', st)
                            postTagName = tmpRef[st+1:ed]
                            while postTagName not in validLabels and st > 0 :
                                st = tmpRef.find('<', ed)
                                ed = tmpRef.find('>', st)
                                postTagName = tmpRef[st+1:ed]
                            if postTagName in validLabels :
                                tmpPtr, ed1, st2, ed2 = tagtool._findTagPosition(tmpRef, 'nonbibl', ed)
                                if tmpPtr < 0 : tmpPtr = limit2
                                tmpCentre = BeautifulSoup(tmpRef[st:tmpPtr], "lxml")
                                sepBibl = False
                                c = 0
                                for tcen in tmpCentre.find_all() :
                                    if tcen.name in separateLabels : c+= 1
                                if c > 1 : sepBibl = True
                                if sepBibl :
                                    tmpRef = tmpRef[:st] + '<bibl>' + tmpRef[st:]
                                    st1 = st
                                    oriRef = tmpRef
                                    case2 = True
                    st1, ed1, st2, ed2 = tagtool._findTagPosition(oriRef, 'nonbibl', st1+1)
                    
        return oriRef

