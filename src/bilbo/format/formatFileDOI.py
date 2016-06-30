# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:05:17 2016

@author: ollagnier, orban
"""
import sys
from bs4 import BeautifulSoup
from codecs import open
import urllib2

def formatFileDOI(soup):
    #post process to question Crossref
    book_list =[]
    tag_list = ['surname', 'forename', 'title', 'booktitle']
    #main label around paragraphs
    for s in soup.findAll("impl"):
        try :
            for bibl in s.findAll('bibl') :
                reference = { tag: (bibl.find(tag).string if bibl.find(tag) is not None else None) for tag in tag_list }
                book_list.append(reference)
                #iteration on book list
                '''    
                for element in book_list:
                 print element
                '''
        except Exception, err:
            print 'Reading error of reference\n\n'
            print err
            pass
    return book_list

def searchDOI(blist):
    for b in blist:
        doi = None
        if b['title']:
            print b['title'], b['surname']
            q = constructCrossrefQuery(b['title'], b['surname'])
            print q


def constructCrossrefQuery(title, name = None):
    qtitle = '<article_title match="fuzzy">%s</article_title>' % urllib2.quote(title.encode('utf-8'))
    if name:
        qname = '<author search-all-authors="false">%s</author>' % urllib2.quote(name.encode('utf-8'))
    else:
        qname = None
    xml = '<?xml version = "1.0" encoding="UTF-8"?>\
    <query_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0" xmlns="http://www.crossref.org/qschema/2.0" xsi:schemaLocation="http://www.crossref.org/qschema/2.0 http://www.crossref.org/qschema/crossref_query_input2.0.xsd">\
    <head><doi_batch_id>bilbo</doi_batch_id></head>\
    <body><query list-components="false" expanded-results="true" key="key">\
    %s %s\
    </query></body></query_batch>' % (qtitle, qname) 
    return xml

if __name__ == '__main__':
    soup = BeautifulSoup(open(sys.argv[1]))
    references = formatFileDOI(soup)
    print searchDOI(references)
