# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:45:56 2015

@author: ollagnier
"""
from codecs import open
import re
import os
import shutil

def setDirModel(dirModel):
    dirModel = dirModel
    
def extract_FullBibl(biblFile, outputFile):
    '''
    Extract Bibl tag with content whitout other tags
    '''
    content = open(biblFile,'r',encoding='utf-8')
    output = open(outputFile, 'w',encoding='utf-8')
    lines=content.read()
    reobj = re.compile(r"(.*<bibl.*?>.*?</bibl>.*)", re.IGNORECASE | re.DOTALL | re.MULTILINE)
    result = reobj.findall(lines)
    for item in result:
        item = re.sub('</?biblScope.*?>','', item)
        item = re.sub('</?persName.*?>','', item)
        item = re.sub('</?orgName.*?>','', item)
        item = re.sub('</?author.*?>','', item)
        item = re.sub('</?forename.*?>','', item)
        item = re.sub('</?surname.*?>','', item)
        item = re.sub('</?extent.*?>','', item)
        item = re.sub('</?pubPlace.*?>','', item)
        item = re.sub('</?genName.*?>','', item)
        item = re.sub('</?link.*?>','', item)
        item = re.sub('</?meeting.*?>','', item)
        item = re.sub('</?title.*?>','', item)
        item = re.sub('</?booktitle.*?>','', item)
        item = re.sub('</?publisher.*?>','', item)
        item = re.sub('</?date.*?>','', item)
        item = re.sub('</?abbr.*?>','', item)
        item = re.sub('</?edition.*?>','', item)
        item = re.sub('</?c.*?>','', item)
        item = re.sub('</?relatedItem.*?>','', item)
        item = re.sub('<bibl.*?>','<bibl>', item)
        item = re.sub('<bibl><bibl>','<bibl>', item)
        item = re.sub('</?note.*?>','', item)
        #print item
        output.write(item)
        output.write('\n')
    output.close

def extract_Bibl(biblFile, outputFile):
    '''
    Extract Bibl tag with content whitout other tags
    '''
    content = open(biblFile,'r',encoding='utf-8')
    output = open(outputFile, 'w',encoding='utf-8')
    lines=content.read()
    reobj = re.compile(r"(<bibl.*?>.*?</bibl>)", re.IGNORECASE | re.DOTALL | re.MULTILINE)
    result = reobj.findall(lines)
    for item in result:
        item = re.sub('</?biblScope.*?>','', item)
        item = re.sub('</?persName.*?>','', item)
        item = re.sub('</?orgName.*?>','', item)
        item = re.sub('</?note.*?>','', item)
        item = re.sub('</?author.*?>','', item)
        item = re.sub('</?forename.*?>','', item)
        item = re.sub('</?surname.*?>','', item)
        item = re.sub('</?extent.*?>','', item)
        item = re.sub('</?pubPlace.*?>','', item)
        item = re.sub('</?genName.*?>','', item)
        item = re.sub('</?link.*?>','', item)
        item = re.sub('</?meeting.*?>','', item)
        item = re.sub('</?title.*?>','', item)
        item = re.sub('</?booktitle.*?>','', item)
        item = re.sub('</?publisher.*?>','', item)
        item = re.sub('</?date.*?>','', item)
        item = re.sub('</?abbr.*?>','', item)
        item = re.sub('</?edition.*?>','', item)
        item = re.sub('</?c.*?>','', item)
        item = re.sub('</?relatedItem.*?>','', item)
        item = re.sub('<bibl.*?>','<bibl>', item)
        item = re.sub('<bibl><bibl>','<bibl>', item)
        output.write(item)
        output.write('\n')
    output.close
    
def extract_ContentBibl(biblFile, outputFile):
    '''
    Extract content of Bibl for create file for train CRF only on content of bibl
    
    '''
    content = open(biblFile,'r',encoding='utf-8')
    output = open(outputFile, 'w',encoding='utf-8')
    lines=content.read()
    reobj = re.compile(r"(<bibl.*?>.*?</bibl>)", re.IGNORECASE | re.DOTALL | re.MULTILINE)
    result = reobj.findall(lines)
    for item in result:
        output.write(item)
        output.write('\n')
    output.close
    
if __name__ == '__main__':
    main = os.path.realpath(__file__).split('/')
    rootDir = "/".join(main[:len(main)-4])
    extract_FullBibl(rootDir+'/Data/ref_implicites.xml',rootDir+'/Data/Corpus_FullBibl_Clean_ref_implicites.xml')
    extract_Bibl(rootDir+'/Data/ref_implicites.xml',rootDir+'/Data/Corpus_Bibl_Clean_ref_implicites.xml')
    extract_ContentBibl(rootDir+'/Data/ref_implicites.xml', rootDir+'/Data/Corpus_Bibl_ref_implicites.xml')