# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Tue Oct  4 17:39:09 2016

@author: ollagnier
"""

from bilbo.extra.Name import Name
from bilbo.extra.Place import Place
from bilbo.extra.Properlist import Properlist
import sys, os
import re
from codecs import open

class UpperExtract(object):
    def __init__(self, options={}):
        self.options = options
        self.link = {':':0, '=':0, '_':0, '|':0, '~':0, '-':0, '–':0}
        self.nonLabels = {}
        self.features = {}
        self.regles = {}
        
        main = os.path.realpath(__file__).split('/')
        self.rootDir = "/".join(main[:len(main)-4])
        
        try:
            flag = 0
            nameRegle = ""
            
            for line in open(os.path.join(self.rootDir, "KB/config/features.txt"), encoding='utf8'):
                lineSplit = re.split("\s", line, flags=re.UNICODE)
                if lineSplit[0] == "#":
                    nameRegle = lineSplit[1]
                    flag += 1
                elif flag == 1:
                    'features'
                    self.features[lineSplit[0]] = 0
                elif flag == 2:
                    'nonLabels'
                    self.nonLabels[lineSplit[0]] = lineSplit[1]
                else:
                    'bookindicator'
                    if not self.regles.has_key(nameRegle):
                        self.regles[nameRegle] = {}
                    self.regles[nameRegle][lineSplit[0]] = 0
        except IOError:
            print("Cannot open the file \"KB/config/features.txt\" \n")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
            
        self.configTag = {}
        
        if self.options.i == "tei" :
            try:
                for line in open(os.path.join(self.rootDir, "KB/config/balise.txt"), "r", encoding='utf8'):
                    lineSplit = re.split("\s", line, flags=re.UNICODE)
                    self.configTag[lineSplit[0]] = lineSplit[1].split("\n")[0]
                if self.options.g == "detail" :
                    del self.configTag['meeting']
            except IOError:
                print("Cannot open the file \"KB/config/balise.txt\" \n")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
                
        self.nameObj = Name(os.path.join(self.rootDir, "KB/config/externalList/auteurs_revuesorg2.txt")) #SURNAMELIST, FORENAMELIST
        self.placeObj = Place(os.path.join(self.rootDir, "KB/config/externalList/list_pays.txt")) #PLACELIST
        self.cityObj = Properlist(os.path.join(self.rootDir, "KB/config/externalList/LargeCities.txt"), "PLACELIST") #PLCAELIST
        self.journalObj = Properlist(os.path.join(self.rootDir, "KB/config/externalList/journalAll.txt"), "JOURNALLIST") #PLCAELIST


    def extract(self):
        return


    def randomgen(self, listRef, tr) :
        nbRef = listRef.nbReference()
        for i in range(nbRef) :
            if tr == 1 :
                listRef.modifyTrainIndiceRef(i)
            else : 
                listRef.modifyTestIndiceRef(i)
        return


    def loadIndices(self, fichier):
        indices = []
        for line in open(fichier, encoding='utf8'):
            indices.append(line)
        return indices


    def _printdata(self, fichier, listRef, tr, opt="saveNegatives") :
        fich = open(fichier, "w", encoding="utf-8")
        for reference in listRef.getReferences():
            if (not (opt=="deleteNegatives" and reference.train == -1)) and (not (opt=="deletePositives" and reference.train != -1)) :
                for mot in reference.getWord():
                    if mot.ignoreWord == 0:
                        fich.write(mot.nom)
                        nbCarac = mot.nbFeatures()
                        cpt = 0
                        if nbCarac > 0:
                            caracteristique = mot.getFeatureIndice(nbCarac-1)
                            fich.write(" "+caracteristique.nom.upper())
                            
                            while cpt < nbCarac-1:
                                caracteristique = mot.getFeatureIndice(cpt)
                                fich.write(" "+caracteristique.nom.upper())
                                cpt += 1
                        if tr != 0:
                            #mot.affiche()
                            for w in mot.listNomTag():
                                    
                                if w == 'nonbibl':
                                    balise = mot.getLastTag()
                                else:
                                    mot.addTag('bibl')
                                    balise = mot.getLastTag()
                            #print(mot.listNomTag())
                            fich.write(" "+balise.nom)
                            
                        fich.write("\n")
                fich.write("\n")
        fich.close()
        return


    def _printdataWapiti(self, fichier, listRef, tr, opt="saveNegatives") :
        features = [['ALLNUMBERS', 'NUMBERS'],['DASH'],['ALLCAP', 'ALLSMALL', 'FIRSTCAP', 'NONIMPCAP'],['BIBL_START', 'BIBL_IN', 'BIBL_END'],['INITIAL'],['WEBLINK'],['ITALIC'],['POSSEDITOR'],['POSSPAGE'],['POSSMONTH'],['SURNAMELIST'],['FORENAMELIST'],['PLACELIST'],['JOURNALLIST']]
        if self.options.u : features.append(['PUNC', 'COMMA', 'POINT', 'LEADINGQUOTES', 'ENDINGQUOTES', 'LINK','PAIREDBRACES'])
        fich = open(fichier, "w", encoding="utf-8")
        for reference in listRef.getReferences():
            if (not (opt=="deleteNegatives" and reference.train == -1)) and (not (opt=="deletePositives" and reference.train != -1)):
                for mot in reference.getWord():
                    tmp_features = ['NONUMBERS', 'NODASH', 'NONIMPCAP', 'NULL', 'NOINITIAL','NOWEBLINK', 'NOITALIC', 'NOEDITOR', 'NOPAGE', 'NOMONTH', 'NOSURLIST','NOFORELIST', 'NOPLACELIST', 'NOJOURLIST']
                    if self.options.u : tmp_features.append('NOPUNC')
                    if mot.ignoreWord == 0:
                        fich.write(mot.nom)
                        nbCarac = mot.nbFeatures()
                        cpt = 0
                        if nbCarac > 0:
                            total_features = ""
                            caracteristique = mot.getFeatureIndice(nbCarac-1)
                            cur_feature = ""
                            cur_feature = caracteristique.nom.upper()
                            total_features += cur_feature+" "
                            
                            while cpt < nbCarac-1:
                                caracteristique = mot.getFeatureIndice(cpt)
                                cur_feature = caracteristique.nom.upper()
                                total_features += cur_feature+" "
                                cpt += 1
                                
                            for i in range(len(features)) :
                                cur_feature = ''
                                for j in range(len(features[i])) :
                                    if total_features.count(features[i][j]) > 0 :
                                        cur_feature = features[i][j]
                                if cur_feature != '' :
                                    tmp_features[i] = cur_feature
                                    
                            string_features = ""
                            for ftr in tmp_features :
                                string_features += ftr+" "
                            fich.write(" "+string_features)
                            
                        if tr != 0:
                            #mot.affiche()
                            for w in mot.listNomTag():
                                    
                                if w == 'nonbibl':
                                    balise = mot.getLastTag()
                                else:
                                    mot.addTag('bibl')
                                    balise = mot.getLastTag()
                            #print(mot.listNomTag())
                            fich.write(" "+balise.nom)
                            fich.write("\n")
                fich.write("\n")
                        
        fich.close()
        return


    def _printOnlyLabel(self, fichier, listRef) :
        fich = open(fichier, "w", encoding="utf-8")
        for reference in listRef.getReferences():
            for mot in reference.getWord():
                for balise in mot.getAllTag():
                    fich.write(balise.nom)
                fich.write("\n")
            fich.write("\n")
        fich.close()
        return


    def _print_alldata(self, fichier, listRef) :
        fich = open(fichier, "w", encoding="utf-8")
        for reference in listRef.getReferences():
            for mot in reference.getWord():
                fich.write(mot.nom)
            fich.write("\n")
        fich.close()
        return


    def _print_parallel(self, fichier, listRef) :
        phrase = ""
        feature = ""
        cpt = 0;
        
        fich = open(fichier, "w", encoding="utf-8")
        for reference in listRef.getReferences():
            cpt=0
            for mot in reference.getWord():
                if mot.ignoreWord == 0:
                    for feat in mot.listNomFeature():
                        feature += feat.upper()+" "
                        if cpt == 0 and (feat.lower() == "initial"):
                            feature += "STARTINITIAL "
                    if re.search("NUMBERS", feature, flags=re.UNICODE) != 0 and re.search("ALLNUMBERS", feature, flags=re.UNICODE) != 0:
                        phrase += " "+mot.nom
                    cpt+=1
                    
            fich.write(unicode(reference.bibl))
            fich.write(phrase+"\n")
            
            fich.write(feature+"\n")
            
            fich.write("\n")
            
            feature = ""
            phrase = ""
            cpt+=1
        fich.close()
        return


    def _addlayout(self, listRef) :
        for reference in listRef.getReferences():
            i = 0
            tmp_length = float(reference.nbWord())
            range_middle = int(tmp_length/3.)
            range_end = int(tmp_length/3.*2.)
            for mot in reference.getWord():
                layout_feature = ''
                if i < range_middle :
                    layout_feature = 'BIBL_START'
                elif i < range_end :
                    layout_feature = 'BIBL_IN'
                elif i < tmp_length :
                    layout_feature = 'BIBL_END'
                if layout_feature != '' :
                    mot.addFeature(layout_feature)
                    
                i += 1
        return


    def _extract_title(self, mot, relatItm, titleCK, titleAttr) :
        flagU = 0
        for caracteristique in mot.getAllFeature():
            if caracteristique.nom == 'a' :
                titleAttr = caracteristique.nom
                mot.delFeature('a')
            elif caracteristique.nom == 'j' or caracteristique.nom == 's' or caracteristique.nom == 'm':
                if titleCK == 1 and titleAttr != caracteristique.nom :
                    balise = mot.getTag("title")
                    if balise > 0 : balise.nom = 'booktitle'
                else :
                    titleAttr = caracteristique.nom
                mot.delFeature('j')
                mot.delFeature('s')
            if caracteristique.nom == 'm' or caracteristique.nom == 'u' :
                if relatItm == 1 and titleCK == 1 :
                    balise = mot.getTag("title")
                    if balise > 0 : balise.nom = 'booktitle'
                else :
                    titleAttr = caracteristique.nom
                mot.delFeature('m')
                mot.delFeature('u')
                
                if caracteristique.nom == "u":
                    flagU = 1
                    
        namefeature = mot.listNomFeature()
        if flagU == 1 and 'sub' in  namefeature :
            balise = mot.getTag("title")
            balise.nom = 'booktitle'
            mot.delFeature('sub')
            flagU = 0
        return titleAttr


    def _extract_title_alter(self, mot, relatItm, titleCK, titleAttr) :
        for caracteristique in mot.getAllFeature():
            if caracteristique.nom == "a" :
                balise = mot.getTag("title")
                if balise != -1 : balise.nom = "title_a"
            elif caracteristique.nom == "m" or caracteristique.nom == "volume_title" :
                balise = mot.getTag("title")
                if balise != -1  : balise.nom = "title_m"
            elif caracteristique.nom == "j" :
                balise = mot.getTag("title")
                if balise != -1  : balise.nom = "title_j"
            elif caracteristique.nom == "s" :
                balise = mot.getTag("title")
                if balise != -1 : balise.nom = "title_s"
            elif caracteristique.nom == "u" :
                balise = mot.getTag("title")
                if balise != -1 : balise.nom = "title_u"
            elif caracteristique.nom == "translated_title" :
                balise = mot.getTag("title")
                if balise != -1 : balise.nom = "title_t"
            elif caracteristique.nom == "research_programm" :
                balise = mot.getTag("title")
                if balise != -1 : balise.nom = "title_r"
        return titleAttr


    def _extract_biblscope(self, mot):
        for caracteristique in mot.getAllFeature():
            if caracteristique.nom == "vol" :
                balise = mot.getTag("biblscope")
                if balise != -1 : balise.nom = "biblscope_v"
            elif caracteristique.nom == "issue" :
                balise = mot.getTag("biblscope")
                if balise != -1  : balise.nom = "biblscope_i"
            elif caracteristique.nom == "pp" :
                balise = mot.getTag("biblscope")
                if balise != -1  : balise.nom = "biblscope_pp"
            elif caracteristique.nom == "chap" :
                balise = mot.getTag("biblscope")
                if balise != -1 : balise.nom = "biblscope_c"
            elif caracteristique.nom == "part" :
                balise = mot.getTag("biblscope")
                if balise != -1 : balise.nom = "biblscope_pa"
        return


    def _checkTag(self, mot):
        balises = mot.getAllTag()
        for balise in balises:
            if self.configTag.has_key(balise.nom):
                balise.nom = self.configTag[balise.nom]
        return


    def _updateTag(self, mot):
        balise = mot.getLastTag()
        if balise != -1:
            nameTag = balise.nom
            self._checkTag(mot)
            if nameTag == 'title' or mot.getTag("title") != -1 :
                if self.options.g == 'simple' :
                    self.titleAttr = self._extract_title(mot, self.relatItm, self.titleCK, self.titleAttr)
                elif self.options.g == 'detail' :
                    self.titleAttr = self._extract_title_alter(mot, self.relatItm, self.titleCK, self.titleAttr)
                if mot.getLastTag().nom == 'title' : self.titleCK = 1
                    
            for nameRegle in self.regles:
                if nameTag == 'nolabel' and  (self.regles[nameRegle].has_key(mot.nom.lower())) :
                    mot.delAllTag()
                    mot.addTag(nameRegle)
                    
            if nameTag == 'biblscope' :
                if self.options.g == 'detail' : self._extract_biblscope(mot)
                if mot.getFeature('publicationDate') != -1:
                    mot.delAllTag()
                    mot.addTag('date')


    def _checkNonLabels(self, mot):
        j = mot.nbTag() - 2
        if mot.getLastTag() == -1:
            return
            
        if self.nonLabels.has_key(mot.getLastTag().nom) :
            try :
                while self.nonLabels.has_key(mot.getTagIndice(j).nom) :
                    j -= 1
                saveNom = mot.getTagIndice(j).nom
                mot.delAllTag()
                mot.addTag(saveNom)
                
            except :
                pass
            flag = 0
            nbTag = mot.nbTag()
            for tag in reversed(range(nbTag)) :
                try:
                    nomTag = mot.getTagIndice(tag).nom
                    if self.nonLabels[nomTag] == "1":
                        flag = 1
                        mot.delAllTag()
                        mot.addTag(nomTag)
                        
                except:
                    pass
                
            if flag == 0:
                mot.delAllTag()
                mot.addTag('nolabel')
                
            else:
                saveNom = mot.getLastTag().nom
                mot.delAllTag()
                mot.addTag(saveNom)


    def extractIndices(self, svmprediction_trainfile, listRef):
        nbRef = listRef.nbReference()
        svm_train = []
        for line in open (svmprediction_trainfile, 'r', encoding='utf8') :
            line = line.split()
            svm_train.append(float(line[0]))
            
        positive_indices = range(nbRef)
        
        n=0
        j=0
        for n in range(nbRef) :
            if svm_train[j] > 0 :
                positive_indices[n] = 1
            else :
                positive_indices[n] = 0
            j += 1
            
        n=0
        for ref in listRef.getReferences() :
            if positive_indices[n] == 0 :
                ref.train =  -1
            n += 1
            
        return


    def extractIndices4new(self, svmprediction_newfile, listRef):
        i = 0
        for line in open (svmprediction_newfile, 'r', encoding='utf8') :
            line = line.split()
            if float(line[0]) > 0 :
                listRef.getReferencesIndice(i).train = 0
            else :
                listRef.getReferencesIndice(i).train = -1
            i += 1
        return