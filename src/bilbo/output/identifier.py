#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

#usrname is initialized in 'KB/config/config.txt'
prePunc =  {'.':0, ',':0, ')':0, ':':0, ';':0, '»':0, '-':0, '”':0, '}':0, ']':0,  '!':0, '?':0}
postPunc = {'(':0, '«':0, '-':0, '“':0, '{':0, '[':0}
codeURL = [[';', '%3B'], ['/', '%2F'], ['?', '%3F'], [':', '%3A'], ['@', '%40'], ['=', '%3D'], ['&', '%26'], [' ','%20']]


main = os.path.realpath(__file__).split('/')
rootDir = "/".join(main[:len(main)-4])

def extractDoi(input_str, tagTypeCorpus) :
	config = ConfigParser.ConfigParser()
	config.read(os.path.join(rootDir, 'KB/config/config.txt'))
	usrname = unicode(config.get("crossref", "usrname"))
	soup = BeautifulSoup(input_str, "lxml")
	count = 0
	for s in soup.findAll("bibl") :
		title = ''
		sname = ''
		fname = ''
		refString = ''
		try :
			a = s.find('surname')
			aa = s.find('forename')
			if a :
				sname =  unicode(s.surname.string)
			if aa :
				fname =  unicode(s.forename.string)
			b = s.find(re.compile('^title', flags=re.UNICODE))
			c = s.find('booktitle')
			
			if c :
				#tmp_str = ' '.join(str(x) for x in s.contents)
				tmp_str = unicode(s)
				if b and tmp_str.find('<booktitle>') < tmp_str.find('<title>') :
					tmp = b
					b = c
					c = tmp
			if b :
				tagname = b.name
				title = ''
				title = unicode(b.string)
				
				if len(title.split()) > 2 :
					title = title
				else :
					add_title = b.findNext(re.compile('^title', flags=re.UNICODE))
					if add_title and add_title.name == tagname :
						title += unicode(add_title.string)
			elif c :
				title =  unicode(c.string)
			else :
				print 'First author : ', sname, '	Title : ', title
				pass
		except Exception, err:
			print 'Reading error of reference while searching DOI\n\n'
			print err
			pass
		
		title2 = urllib2.quote(title.encode('utf-8'))
		sname2 = urllib.quote(sname.encode('utf-8'))
		fname2 = urllib.quote(fname.encode('utf-8'))
		
		q1 = 'http://doi.crossref.org/servlet/query?usr='+usrname+'&format=unixref&qdata=%3C?xml%20version%20=%20%221.0%22%20encoding=%22UTF-8%22?%3E%3Cquery_batch%20version=%222.0%22%20xmlns%20=%20%22http://www.crossref.org/qschema/2.0%22%20xmlns:xsi=%22http://www.w3.org/2001/XMLSchema-instance%22%3E%3Chead%3E%3Cdoi_batch_id%3EDOI%20result%3C/doi_batch_id%3E%3C/head%3E%3Cbody%3E%3Cquery%20key=%22mykey%22%20expanded-results=%22true%22%3E%3Carticle_title%20match=%22fuzzy%22%3E'
		q2 = '%3C/article_title%3E%3Cauthor%20match=%22fuzzy%22%20search-all-authors=%22false%22%3E'
		q3 = '%3C/author%3E%3C/query%3E%3C/body%3E%3C/query_batch%3E'
		
		qry = q1+title2+q2+sname2+q3 # no str + unicode error !
		xml = urllib2.urlopen(qry).read()
		xml = xml.decode('utf8')
		doi = BeautifulSoup(xml, "lxml").find('doi')
		doistring = ''
		if doi :
			print refString
			print 'First author : ', sname, '	Start of title : ', title
			doistring = unicode(doi.string)
			print 'DOI :', doistring
			print
			count += 1
		else :
			qry = q1+title2+q2+fname2+q3
			xml = urllib2.urlopen(qry).read()
			doi = BeautifulSoup(xml, "lxml").find('doi')
			if doi :
				print refString
				print 'First author : ', fname, '	Start of title : ', title
				doistring = unicode(doi.string)
				print 'DOI :', doistring
				print
				count += 1
			else :
				print('No DOI')
	
	return doistring


def loadTEIRule(tagConvert):
	parser = ConfigParser.ConfigParser()
	parser.read(os.path.join(rootDir, 'KB/config/others.txt'))
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


def teiValidate(fname, objfile) :
	"""
	Xml validation check using xml schema in a xsd file
	"""
	valide = True
	if objfile == 'output' :
		xsdfile = os.path.join(rootDir, 'KB/validation/output/tei_openedition3.xsd')
		xmlschema_doc = etree.parse(open(xsdfile))
		xmlschema = etree.XMLSchema(xmlschema_doc)
		doc = etree.parse(fname)
		valide = xmlschema.validate(doc)
		numErr = len(xmlschema.error_log)
		
		print('\n*xml validation* '+fname)
		if len(xmlschema.error_log) > 0 : print(xmlschema.error_log)
		print('number of errors :', len(xmlschema.error_log))
		
	else :
		dtdfile = os.path.join(rootDir, 'KB/validation/input/tei_all.dtd')
		dtd = etree.DTD(open(dtdfile))
		doc = etree.parse(fname)
		valide = dtd.validate(doc)
		numErr = len(dtd.error_log)
		if not valide :
			print(dtd.validate(doc), fname)
			print('excluded : non valid xml file with TEI guidelines')
		
	return valide, numErr


def main():
	if len (sys.argv) != 2 :
		print('python identifier.py (xml file name)')
		sys.exit (1)
	#input = rfile(str(sys.argv[1]))
	#extractDoi(input)
	tagConvert = {}
	loadTEIRule(tagConvert)
	toTEI('test', tagConvert)


if __name__ == '__main__':
	main()
