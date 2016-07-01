# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:05:17 2016

@author: ollagnier, orban
"""
import sys
from bs4 import BeautifulSoup
from codecs import open
import urllib2
import urllib
import pycurl
from StringIO import StringIO
import mysettings as s
crossref_url = 'http://doi.crossref.org/servlet/query?'

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

def searchDOI(references):
    for ref in references:
        doi = None
        if ref['title']:
            query = constructCrossrefQuery(ref['title'], ref['surname'])
            cr_resp = askCrossref(query)
        if cr_resp:
            xml_rep = BeautifulSoup(cr_resp)
            doi_rep = xml_rep.find('doi_record')
            if doi_rep:
                doi = (doi_rep.find('doi_data').find('doi').name if xml_rep.find('doi_record').find('doi') else None)
        ref['doi'] = doi
    return references



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

def askCrossref(query):
    get = {'usr': s.crossref_login, 'pwd': s.crossref_pwd, 'format':'unixref', 'qdata': query}
    get = urllib.urlencode(get)
    c = pycurl.Curl()
    buffer = StringIO()
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.URL, crossref_url + get)
    c.setopt(c.VERBOSE, False)
    c.perform()
    body = buffer.getvalue()
    status = c.RESPONSE_CODE
    c.close()
    buffer.close()
    # print status, get
    return body

if __name__ == '__main__':
    soup = BeautifulSoup(open(sys.argv[1]))
    references = formatFileDOI(soup)
    doi_references = searchDOI(references)
    for doi in doi_references:
#        if doi['doi'] != None:
 #           searchJson(doi['doi']
        print 'Le RESULTAT', doi












