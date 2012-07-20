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

dossier_fichier_out = "/Users/jade/Documents/jade/labo/BILBO/bilbo/Result/";   # dossier sortie : resultat
dossier_fichier_in = "/Applications/XAMPP/htdocs/WebService_python/fichier/"; # dossier ou l'on crée le fichier a annoter (ce dossier doit contenir que les fichier a annoter)
dossier_code = "/Users/jade/Documents/jade/labo/BILBO/bilbo/"; # dossier ou l'on retrouve le code objet dossier bilbo


'''######## fonction service proposee #########'''

'''
annoteText : annote un texte simple (texte considéré comme une référence)
    parametre :
        type corpus :
        reference : texte à annoter
'''
def annotateText(type, reference):
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
    if type == 1:
        fich.write("<bibl>"+reference+"</bibl>")
    elif type == 2:
        fich.write("<note place=\"foot\">"+reference+"</note>")
    fich.write("</listBibl>")
    fich.close()

    # lancement de mallet
    if type == 1:
        annoterCorpus1()
    elif type == 2:
        annoterCorpus2()

    #recupere le resultat de BILBO
    fich = open(dossier_fichier_out+"/fichier_a_annoter.xml", "r")
    resultat = fich.readlines()
    fich.close()

    return resultat

'''
annoteFile : annote un fichier complet
    parametre :
        type corpus :
        file : fichier a annoter
'''
def annotateFile(type, article):
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
    if type == 1:
        annoterCorpus1()
    elif type == 2:
        annoterCorpus2()
    
    #recupere le resultat de BILBO
    fich = codecs.open(dossier_fichier_out+"/fichier_a_annoter.xml", "r", "utf-8")
    resultat = fich.readlines()
    fich.close()
    
    return ''.join(resultat)

'''
    annoteAllFiles : annote un fichier complet
    parametre :
        type corpus :
        file : tableau de fichier a annoter
    '''
def annotateAllFiles(type, articles):
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
    if type == 1:
        annoterCorpus1()
    elif type == 2:
        annoterCorpus2()
    
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
    annoterCorpus1 : lance BILBO pour le corpus 1
    '''
def annoterCorpus1():
    repSave = os.getcwd()
    os.chdir(dossier_code)

    sys.argv=["Main.py", 1, dossier_fichier_in, dossier_fichier_out] 
    execfile("src/mypkg/Main.py") 
       
    os.chdir(repSave)

    return 

'''
    annoterCorpus2 : lance BILBO pour le corpus 2
'''
def annoterCorpus2():
    repSave = os.getcwd()
    os.chdir(dossier_code)
    
    sys.argv=["Main.py", 2, dossier_fichier_in, dossier_fichier_out] 
    execfile("src/mypkg/Main.py") 
    
    os.chdir(repSave)
    
    return 


def connect():
    server = SOAPpy.SOAPServer(("127.0.0.1",80))
    server.registerFunction(annotateText)
    server.registerFunction(annotateFile)
    server.registerFunction(annotateAllFiles)
    server.serve_forever()
    
if __name__ == '__main__':
    connect()
    
    
   