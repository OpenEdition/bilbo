#!/usr/bin/env python
# encoding: utf-8
"""
identifier.py
Created by Young-Min Kim on 2012-12-30.

"""

import sys, os, re
import string
import urllib, urllib2
import ConfigParser
from bs4 import BeautifulSoup
from lxml import etree

#usrname is initialized in 'KB/config/others.txt'
prePunc =  {'.':0, ',':0, ')':0, ':':0, ';':0, '»':0, '-':0, '”':0, '}':0, ']':0,  '!':0, '?':0}
postPunc = {'(':0, '«':0, '-':0, '“':0, '{':0, '[':0}
codeURL = [[';', '%3B'], ['/', '%2F'], ['?', '%3F'], [':', '%3A'], ['@', '%40'], ['=', '%3D'], ['&', '%26'], [' ','%20']]


def extractDoi(input_str, tagTypeCorpus) :
	
	config = ConfigParser.ConfigParser()
	config.read('KB/config/others.txt')
	usrname = str(config.get("crossref", "usrname"))
	soup = BeautifulSoup(input_str)
	count = 0
	for s in soup.findAll("bibl") :
	
		sname = ''
		title = ''
		refString = ''
		try :		
			a = s.find('surname')
			if a :
				try : sname =  str(s.surname.string)
				except : sname =  (s.surname.string).encode('utf8')
			else : 
				pass
			b = s.find(re.compile('^title'))
			c = s.find('booktitle')
			
			if c :
				#tmp_str = ' '.join(str(x) for x in s.contents)
				tmp_str = str(s)
				if b and tmp_str.find('booktitle') < tmp_str.find(re.compile('^title'))  :
					tmp = b
					b = c
					c = tmp
					#print "Booktitle is title"		
			if b :
				tagname = b.name
				title = ''
				try : title = str(b.string)
				except : title =  (b.string).encode('utf8')
				
				if len(title.split()) > 2 :
					title = title
				else :
					add_title = b.findNext(re.compile('^title'))
					if add_title and add_title.name == tagname :
						try : title += str(add_title.string)
						except : title += (add_title.string).encode('utf8')
			elif c :
				try : title =  str(c.string)
				except : title =  (c.string).encode('utf8')
			else : pass #print "No title"
			#print 'First author : ', sname, '	Title : ', title
		except :
			pass
			print 'reading error \n\n'
		
		try : title2 = urllib.quote(title.encode('utf-8'))
		except : 
			title2 = urllib.quote(title)
			pass
		try : sname2 = urllib.quote(sname.encode('utf-8'))
		except : 
			sname2 = urllib.quote(sname)
			pass

		q1 = 'http://doi.crossref.org/servlet/query?usr='+usrname+'&format=unixref&qdata=%3C?xml%20version%20=%20%221.0%22%20encoding=%22UTF-8%22?%3E%3Cquery_batch%20version=%222.0%22%20xmlns%20=%20%22http://www.crossref.org/qschema/2.0%22%20xmlns:xsi=%22http://www.w3.org/2001/XMLSchema-instance%22%3E%3Chead%3E%3Cdoi_batch_id%3EDOI%20result%3C/doi_batch_id%3E%3C/head%3E%3Cbody%3E%3Cquery%20key=%22mykey%22%20expanded-results=%22true%22%3E%3Carticle_title%20match=%22fuzzy%22%3E'
		q2 = '%3C/article_title%3E%3Cauthor%20match=%22fuzzy%22%20search-all-authors=%22false%22%3E'
		q3 = '%3C/author%3E%3C/query%3E%3C/body%3E%3C/query_batch%3E'
				
		qry = q1+title2+q2+sname2+q3				
		xml = urllib2.urlopen(qry).read()
		#print xml
		
		doi = BeautifulSoup(xml).find('doi')
		doistring = ''
		if doi : 
			print refString
			print 'First author : ', sname, '	Start of title : ', title
			doistring = doi.string
			print 'DOI :', doistring
			print
			count += 1
		else :
			print 'No DOI'
		#print raw_input("Press Enter to Exit")
		#print 'Total Num. DOI :', count
		#print
	
	return doistring


def loadTEIRule(tagConvert):
	parser = ConfigParser.ConfigParser()
	parser.read('KB/config/others.txt')
	for name in parser.options('tei') :
		value = parser.get('tei', name)
		tagBefore = '<'+name+'>'
		tagAfter = '<'+value+'>'
		if value != 'NONE' : tagConvert[tagBefore] = tagAfter
		else : tagConvert[tagBefore] = ''
		tagBefore = '</'+name+'>'
		tagAfter = '</'+value.split()[0]+'>'
		if value != 'NONE' : tagConvert[tagBefore] = tagAfter
		else : tagConvert[tagBefore] = ''			
		
	return tagConvert


def toTEI(tmp_str, tagConvert):
	for key in tagConvert.keys() :
		tmp_str = tmp_str.replace(key, tagConvert[key])
		#print key, 'to', tagConvert[key], 'converting finished'	
	return tmp_str


def rfile(fname) :
	tmp_str = ''
	for line in open (fname, 'r') :
		tmp_str = tmp_str + ' ' + line
	return tmp_str


def toHttp(tmp_str) :
	for cd in codeURL :
		tmp_str = string.replace(tmp_str, cd[0],cd[1])
	return tmp_str


def teiValidate(fname) :
	'''
	Xml validation check using xml schema in a xsd file
	'''
	xmlschema_doc = etree.parse(open('KB/validation/tei_openedition3.xsd'))
	xmlschema = etree.XMLSchema(xmlschema_doc)
	doc = etree.parse(fname)
	xmlschema.validate(doc)
	
	print '\n*xml validation* '+fname
	if len(xmlschema.error_log) > 0 : print xmlschema.error_log
	print 'number of errors :', len(xmlschema.error_log)
	print
	#xmlschema.assertValid(doc)
	return


def main():
	if len (sys.argv) != 2 :
		print 'python identifier.py (xml file name)'
		sys.exit (1)
	#input = rfile(str(sys.argv[1]))
	#extractDoi(input)
	tagConvert = {}
	loadTEIRule(tagConvert)
	toTEI('test', tagConvert)


if __name__ == '__main__':
	main()

