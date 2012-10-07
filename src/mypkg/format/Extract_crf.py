# -*- coding: utf-8 -*-
'''
Created on 11 juin 2012

@author: Young-min Kim, Jade Tavernier
'''
from mypkg.format.Extract import Extract

class Extract_crf(Extract):
    '''
    classdocs
    '''

    def __init__(self):
        Extract.__init__(self)
        
    '''
    extractor : extract training and test data
        ndocs : number of references
        typeCorpus : 1, 2 ou 3
        tr : indicator check, it gives the valid instance indices 
        extr : 
        fichierRes = nom du fichier sortie du resultat
    '''
    def extractor (self, typeCorpus, ndocs, fichierRes, listRef, tr=-1, extr=-1) :
        self.titleCK = 0
        self.titleAttr = ''
        self.relatItm = 0
            
        i = 0
        check = -5
        nonbiblck = 1
        
        listReferences = listRef.getReferences()
        tmp_nonbiblck = 0
        for reference in listReferences:
            
            if reference.train == -1 :
                pass # HERE You should eliminate reference....
            
            
            for mot in reference.getWord():
                if mot.ignoreWord == 0:
                    if mot.item == 1: self.relatItm = 1
                    
                    if tr == 1 : check = 1
                    else : check = 0
                    
                    '''
                    A PROBLEM !!!!!!!!!! IF train == -1 we should delete the reference in training. In test also....
                    But here change the tag (NOT CORRECT)
                    '''
                    if reference.train == -1:
                        mot.delAllTag()
                        mot.addTag("nonbibl")
                       
                    elif reference.train == check:
                                                
                        # finding just a label which is not in the nonLabels list
                        self._checkNonLabels(mot)
                        
                        #label check
                        self._updateTag(mot)
                        
                        #nobibl check,
                        tmp_nonbiblck = 0
                        for tmp in mot.getAllTag() :
                            if tmp.nom == 'nonbibl' :
                                tmp_nonbiblck = 1
                            elif tmp.nom == 'c':
                                if nonbiblck == 1:
                                    tmp_nonbiblck = 1

    
                        if tr == 0 :
                            mot.delAllTag()
                    
                        'del toutes ls caracteristique qui ne sont pas presente dans le tableau features'
                        supp = []
                        'si c est de la ponctuation on enleve toutes les caracteristiques'
                        balise = mot.getLastTag()
                        if balise != -1:
                            if balise.nom == "c":
                                mot.delAllFeature()
                                mot.addFeature("PUNC")
                                'sinon on enleve que celle non presente dans les features'
                                
                        
                        for carac in mot.getAllFeature():
                            if not self.features.has_key(carac.nom.lower()):
                                supp.append(carac.nom)
                                
                        for nomMot in supp:
                            mot.delFeature(nomMot)
                            
                        if tmp_nonbiblck == 0 : nonbiblck = 0
                
                
            i += 1
            self.titleCK = 0
            self.titleAttr = ''
            self.relatItm = 0
            
            if nonbiblck == 1 :
                reference.bibl = -1
            else : 
                reference.bibl = 1
            nonbiblck = 1
            
        
        if tr != -2 :
            self.nameObj.searchName(listRef, tr)
            self.placeObj.searchPlace(listRef, tr)
            self.properObj.searchProper(listRef, tr, 'place')
        
        if extr == 1 or extr == 2 :
            if tr != -2 :
                self._addlayout(listRef)                    ####### add layout features ### 2012-02-01 ###
                self._printdata(fichierRes, listRef, tr)
            else:
                self._printOnlyLabel(fichierRes, listRef)
            
        elif extr == 3 or extr == 4 or extr == 5 or extr == 6:
            self._printmoreFeatures(extr)
        
        if typeCorpus == 2:
            '''if tr == 1:
                self._print_alldata(fichierRes, listRef)
            else :'''
            
            self._print_parallel(fichierRes, listRef)
                
        return