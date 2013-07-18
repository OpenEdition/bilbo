# -*- coding: utf-8 -*-
'''
Created on 17 juil. 2012

@author: jade
'''
import SOAPpy
import sys 
import codecs
import glob
import os

dossier_fichier_out = "../../../soapResult/";   # dossier sortie : resultat
dossier_fichier_in = "../../../soapTmp/"; # dossier ou l'on crée le fichier a annoter (ce dossier doit contenir que les fichier a annoter)
dossier_code = "../"; # dossier ou l'on retrouve le code objet dossier bilbo

dossier_fichier_out = os.path.abspath(dossier_fichier_out) + "/"
dossier_fichier_in = os.path.abspath(dossier_fichier_in) + "/"
dossier_code = os.path.abspath(dossier_code) + "/"

#Import bilbo
sys.path.append('../..')
from bilbo.Bilbo import Bilbo
from bilbo.utils import *

'''######## fonction service proposee #########'''

'''
annoteText : annote un texte simple (texte considéré comme une référence)
    parametre :
        typeCorpus corpus :
        reference : texte à annoter
'''
def annotateText(typeCorpus, reference):
    #supprime les anciens fichiers
    files = os.listdir(dossier_fichier_in)
    for filename in files: 
        print filename
        os.remove(dossier_fichier_in+filename)
    
    files = os.listdir(dossier_fichier_out)
    for filename in files: 
        os.remove(dossier_fichier_out+filename)

    # creation fichier pour l'annoter
    fich = open(dossier_fichier_in+"/fichier_a_annoter.xml", "w")
    fich.write("<listBibl>")
    if typeCorpus == 1:
        fich.write("<bibl>"+reference+"</bibl>")
    elif typeCorpus == 2:
        fich.write("<note place=\"foot\">"+reference+"</note>")
    fich.write("</listBibl>")
    fich.close()

    # lancement de mallet
    annoterCorpus(typeCorpus)

    #recupere le resultat de BILBO
    fich = open(dossier_fichier_out+"/fichier_a_annoter.xml", "r")
    resultat = fich.readlines()
    fich.close()

    return resultat

'''
annoteFile : annote un fichier complet
    parametre :
        typeCorpus corpus :
        file : fichier a annoter
'''
def annotateFile(typeCorpus, article):
    #supprime les anciens fichiers
    files = os.listdir(dossier_fichier_in)
    for filename in files: 
        print filename
        os.remove(dossier_fichier_in+filename)
    
    files = os.listdir(dossier_fichier_out)
    for filename in files: 
        os.remove(dossier_fichier_out+filename)

    # creation fichier pour l'annoter
    fich = codecs.open(dossier_fichier_in+"/fichier_a_annoter.xml", "w", "utf-8")
    
    fich.write(article)
    print article
    # lancement de mallet
    annoterCorpus(typeCorpus)
    
    #recupere le resultat de BILBO
    fich = codecs.open(dossier_fichier_out+"/fichier_a_annoter.xml", "r", "utf-8")
    resultat = fich.readlines()
    fich.close()
    
    return ''.join(resultat)

'''
    annoteAllFiles : annote un fichier complet
    parametres :
        typeCorpus corpus :
        file : tableau de fichier a annoter
    '''
def annotateAllFiles(typeCorpus, articles):
    resultat = []
    cpt = 0
    
    #supprime les anciens fichiers
    files = os.listdir(dossier_fichier_in)
    for filename in files: 
        os.remove(dossier_fichier_in+filename)
    
    files = os.listdir(dossier_fichier_out)
    for filename in files: 
        os.remove(dossier_fichier_out+filename)
    
    for article in articles:
        fich = codecs.open(dossier_fichier_in+"/fichier_a_annoter_"+str(cpt)+".xml", "w", "utf-8")
    
        # creation fichier pour l'annoter
        fich.write(article)
        fich.close()
        cpt += 1
 
    # lancement de mallet
	annoterCorpus(typeCorpus)

    cpt -= 1
    while cpt >= 0:
        #recupere le resultat de BILBO
        fich = codecs.open(dossier_fichier_out+"/fichier_a_annoter_"+str(cpt)+".xml", "r", "utf-8")
        resultat.append(''.join( fich.readlines()))
        fich.close()
        cpt -= 1
        
    
    return resultat


'''######## fonction privee #########'''
'''
    annoterCorpus : lance BILBO
    '''
def annoterCorpus(typeCorpus):
	options = type('object', (), {'i':'tei', 'm':'revues', 'g':'simple', 'k':'none', 'v':'none', 'u':False, 's':False, 'o':'tei', 'd':False, 'e':False})
	dirCorpus = os.path.abspath('../../../model/corpus' + str(typeCorpus) + "/revues/") + "/"
	
	bilbo = Bilbo(dossier_fichier_out, options, "crf_model_simple")
	bilbo.annotate(dossier_fichier_in, dirCorpus, typeCorpus)
	return 

def connect():
    server = SOAPpy.SOAPServer(("127.0.0.1",7070))
    server.registerFunction(annotateText)
    server.registerFunction(annotateFile)
    server.registerFunction(annotateAllFiles)
    server.serve_forever()
    
if __name__ == '__main__':
    connect()
    
    
   