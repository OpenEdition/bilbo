# -*- coding: utf-8 -*-
'''
Created on 17 juil. 2012

@author: jade
'''
import SOAPpy
from SOAPpy import WSDL

def client():
    text = []
    fich = open("../../../test/entite-tei-2236.xml", "r")
    resultat = fich.readlines()
    fich.close()
    
    server = SOAPpy.SOAPProxy("http://127.0.0.1:7070/")
    
    server.config.dumpSOAPOut = 1            
    server.config.dumpSOAPIn = 1

    text.append(''.join(resultat))
    text[0] = text[0].decode("utf-8")
    
    fich = open("../../../test/entite-tei-2236.xml", "r")
    resultat = fich.readlines()
    fich.close()
    
    server = SOAPpy.SOAPProxy("http://127.0.0.1:7070/")
    
    server.config.dumpSOAPOut = 1            
    server.config.dumpSOAPIn = 1
    
    text.append(''.join(resultat))
    text[1] = text[1].decode("utf-8")
    
    #print text.decode("utf-8")
    res = server.annotateAllFiles(1, text)
    #print server.annotateText(2, "test pour voir si ca marche")
    
    #print res[0]
    for resOk in res:
        print resOk
    
    '''
    fichier_wsdl = "http://localhost/WebService_python/config_wsdl2.wsdl"
    wsdl = WSDL.Proxy(fichier_wsdl)
    
    print wsdl.methods.keys()
    
    info = wsdl.methods["annotateText"]
    for param in info.inparams:
        print param.name , ':' , param.type
        

    #wsdl.soapproxy.config.dumpSOAPOut = 1            
    #wsdl.soapproxy.config.dumpSOAPIn = 1
    
    print wsdl.annotateText(2, "texte")'''


    
if __name__ == '__main__':
    client()
    
