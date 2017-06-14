# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bilbo.reference.File import File
from bilbo.output.identifier import teiValidate
from bs4 import BeautifulSoup
from codecs import open
import os.path
import commands
import shutil

class Corpus(object):
    def __init__(self, directory, options):
        self.directory = directory
        self.fichiers = []
        self.options = options


    def getFiles(self):
        if os.path.isdir(self.directory):
            lsOut = commands.getoutput('ls '+self.directory)
            listFichiers = lsOut.split("\n")
        else:
            nomSplit = self.directory.split("/")
            listFichiers = []
            listFichiers.append(nomSplit[len(nomSplit)-1])
            del nomSplit[len(nomSplit)-1]
            self.directory = "/".join(nomSplit)
        if self.options.v in ['input', 'all'] : listFichiers = self.validateXml(listFichiers)
        return listFichiers


    def validateXml(self, listFichiers):
        newList = []
        for filename in listFichiers :
            try :
                valide, numErr = teiValidate(os.path.join(self.directory, filename), 'input')
            except Exception, error :
                valide = False
                print(filename)
                print("Can't even try validation", error)
                pass
            if valide : newList.append(filename)
        print("valide files")
        for f in newList : print(f)
        return newList


    def extract(self, type, tag, nomFichiers="", external=0):
        if nomFichiers == "":
            nomFichiers = self.getFiles()
        for nomFichier in nomFichiers:
            fichObj = File(self.directory+"/"+nomFichier, self.options)
            print('My File : ')
            print(self.directory+nomFichier)
            fichObj.extract(type, tag, external)
            self.fichiers.append(fichObj)
            
            
    def extractBibl(self, type, tag, nomFichiers="", external=0):
        if nomFichiers == "":
            nomFichiers = self.getFiles()
        for nomFichier in nomFichiers:
            fichObj = File(self.directory+"/"+nomFichier, self.options)
            print('My File : ')
            print(self.directory+nomFichier)
            fichObj.extractBibl(type, tag, external, self.directory)
            self.fichiers.append(fichObj)


    def getListReferences(self, typeCorpus):
        allReferences = []
        for fichier in self.fichiers:
            listRef = fichier.getListReferences(typeCorpus)
            if listRef != -1:
                allReferences.extend(listRef.getReferences())
        return allReferences


    def nbReference(self, typeCorpus):
        nb = 0
        for fichier in self.fichiers:
            nb += fichier.nbReference(typeCorpus)
        return nb


    def addTagReferences(self, dirResult, fname, tagTypeCorpus, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
        tmp_str = ""
        references = []
        fileRes = dirResult+fname
        for line in open (fileRes, 'r', encoding='utf8') :
            tmp_str = tmp_str + ' ' + line
        soup = BeautifulSoup (tmp_str, "lxml")
        
        s = soup.findAll ("bibl")
        cpt = 0 #total reference count
        for fichier in self.fichiers:
            nbRefFile = fichier.nbReference(typeCorpus)
            references[:] = []
            cptRef = 0 # reference count in the file
            for ref in s:
                if cptRef < nbRefFile:
                    if len(refsAfterSVM) > 0 and refsAfterSVM[cpt].train == -1 : 
                        for tag in (s[cpt]).findAll(True) :
                            tag.replaceWith(tag.renderContents())
                        s2 = BeautifulSoup()
                        tag1 = s2.new_tag("bibl")
                        tag2 = s2.new_tag("nonbibl")
                        s2.insert(0, tag1)
                        tag1.insert(0, tag2)
                        tag2.insert(0, s[cpt].renderContents())
                        references.append(s2.find("bibl"))
                    else :
                        references.append(s[cpt])
                else:
                    break
                cptRef += 1
                cpt += 1
            dirResultRoot = os.path.abspath(os.path.join(dirResult, os.path.pardir))+'/'
            fichier.buildReferences(references, tagTypeCorpus, dirResultRoot)
        return
        
        
    def addTagReferencesP(self, dirResult, fname, tagTypeCorpus, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
        tmp_str = ""
        references = []
        fileRes = dirResult+fname
        for line in open (fileRes, 'r', encoding='utf8') :
            tmp_str = tmp_str + ' ' + line
        soup = BeautifulSoup (tmp_str, "lxml")
        s = soup.findAll ("bibl")
        cpt = 0 #total reference count
        for fichier in self.fichiers:
            nbRefFile = fichier.nbReference(typeCorpus)
            references[:] = []
            cptRef = 0 # reference count in the file
            for ref in s:
                if cptRef < nbRefFile:
                    if len(refsAfterSVM) > 0 and refsAfterSVM[cpt].train == -1 : 
                        for tag in (s[cpt]).findAll(True) :
                            tag.replaceWith(tag.renderContents())
                        s2 = BeautifulSoup()
                        tag1 = s2.new_tag("bibl")
                        tag2 = s2.new_tag("nonbibl")
                        s2.insert(0, tag1)
                        tag1.insert(0, tag2)
                        tag2.insert(0, s[cpt].renderContents())
                        references.append(s2.find("bibl"))
                    else :
                        references.append(s[cpt])
                else:
                    break
                cptRef += 1
                cpt += 1
            dirResultRoot = os.path.abspath(os.path.join(dirResult, os.path.pardir))+'/'
            dirResult_Bibl = dirResultRoot+'corpus_JustBibl'
            if not os.path.exists(dirResult_Bibl): os.makedirs(dirResult_Bibl)
            else:
                shutil.rmtree(dirResult_Bibl)
                os.makedirs(dirResult_Bibl)
            fichier.buildReferences(references, tagTypeCorpus, dirResult_Bibl)
        return

    def addTagReferencesFinal(self, dirResult, fname, tagTypeCorpus, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
        tmp_str = ""
        references = []
        fileRes = dirResult+fname
        for line in open (fileRes, 'r', encoding='utf8') :
            tmp_str = tmp_str + ' ' + line
        soup = BeautifulSoup (tmp_str, "lxml")
        
        s = soup.findAll ("bibl")
        cpt = 0 #total reference count
        for fichier in self.fichiers:
            nbRefFile = fichier.nbReference(typeCorpus)
            references[:] = []
            cptRef = 0 # reference count in the file
            for ref in s:
                if cptRef < nbRefFile:
                    references.append(s[cpt])
                else:
                    break
                cptRef += 1
                cpt += 1
            dirResultRoot = os.path.abspath(os.path.join(dirResult, os.path.pardir))+'/'
            fichier.buildReferencesP(references, tagTypeCorpus, dirResultRoot)
        return
        
    def addTagReferencesBibl(self, dirResult, fname, tagTypeCorpus, typeCorpus, refsAfterSVM=[]): #get "listRef" to check deleted notes
        tmp_str = ""
        references = []
        fileRes = dirResult+fname
        for line in open (fileRes, 'r', encoding='utf8') :
            tmp_str = tmp_str + ' ' + line
        soup = BeautifulSoup (tmp_str, "lxml")
        
        s = soup.findAll ("bibl")
        cpt = 0 #total reference count
        for fichier in self.fichiers:
            nbRefFile = fichier.nbReference(typeCorpus)
            references[:] = []
            cptRef = 0 # reference count in the file
            for ref in s:
                if cptRef < nbRefFile:
                    if len(refsAfterSVM) > 0 and refsAfterSVM[cpt].train == -1 : 
                        for tag in (s[cpt]).findAll(True) :
                            tag.replaceWith(tag.renderContents())
                        s2 = BeautifulSoup()
                        tag1 = s2.new_tag("bibl")
                        tag2 = s2.new_tag("nonbibl")
                        s2.insert(0, tag1)
                        tag1.insert(0, tag2)
                        tag2.insert(0, s[cpt].renderContents())
                        references.append(s2.find("bibl"))
                    else :
                        references.append(s[cpt])
                else:
                    break
                cptRef += 1
                cpt += 1
            dirResultRoot = os.path.abspath(os.path.join(dirResult, os.path.pardir))+'/'
            fichier.buildReferencesWithoutSVM(references, tagTypeCorpus, dirResultRoot)
        return

    def deleteAllFiles(self):
        self.fichiers[:] = []
