# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:05:17 2016

@author: ollagnier
"""
import sys
from bs4 import BeautifulSoup
from codecs import open

def rfile(fname) :
	tmp_str = ''
	for line in open(fname, 'r', encoding='utf8') :
		tmp_str = tmp_str + ' ' + line
	return tmp_str

def formatFileDOI(xmlFile):
    #post process to question Crossref
    book_list =[]
    soup = BeautifulSoup(xmlFile)
    #main label around paragraphs
    for s in soup.findAll("impl") :
        try :
            for bibl in s.findAll('bibl') :
                for book in bibl.findAll("title"):
                    book_list.append(book.string)
                #iteration on book list
                '''    
                for element in book_list:
                    print element
                    '''
        except Exception, err:
            print 'Reading error of reference\n\n'
            print err
            pass
        

def main():
    print 'python formatFileDOI.py (xml file name)'
    input = rfile(str(sys.argv[1]))
    formatFileDOI(input)

if __name__ == '__main__':
	main()