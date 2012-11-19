#!/usr/bin/env python
# encoding: utf-8
"""
identifier.py

Created by Young-Min Kim on 2012-12-30.

"""

import sys
import os
import string
import urllib2
import urllib 

from bs4 import BeautifulSoup


prePunc =  {'.':0, ',':0, ')':0, ':':0, ';':0, '»':0, '-':0, '”':0, '}':0, ']':0,  '!':0, '?':0}
postPunc = {'(':0, '«':0, '-':0, '“':0, '{':0, '[':0}

codeURL = [[';', '%3B'], ['/', '%2F'], ['?', '%3F'], [':', '%3A'], ['@', '%40'], ['=', '%3D'], ['&', '%26'], [' ','%20']]


def extractId(input_str) :
	
	soup = BeautifulSoup(input_str)
	#print soup
	count = 0
	for s in soup.findAll('bibl') :
	
		sname = ''
		title = ''
		refString = ''
		try :
		
			a = s.find('surname')
			if a :
				try : sname =  str(s.surname.string)
				except : sname =  (s.surname.string).encode('utf8')
			else : 
				#print "No name"
				pass
			b = s.find('title')
			c = s.find('booktitle')
			
			if c :
				#tmp_str = ' '.join(str(x) for x in s.contents)
				tmp_str = str(s)
				if b and tmp_str.find('booktitle') < tmp_str.find('title')  :
					tmp = b
					b = c
					c = tmp
					#print "Booktitle is title"
			
			if b :
				title = ''
				try : title = str(b.string)
				except : title =  (b.string).encode('utf8')
				
				if len(title.split()) > 1 :
					title = title
				elif b.findNext('title') :
					try : title += str(b.findNext('title').string)
					except : title += (b.findNext('title').string).encode('utf8')
					#print title
			elif c :
				try : title =  str(c.string)
				except : title =  (c.string).encode('utf8')
				#print title
			else : pass #print "No title"
			

			#print tmp_str
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
			
		#print title2, sname2
		
		q1 = 'http://doi.crossref.org/servlet/query?usr=youngminn.kim@gmail.com&format=unixref&qdata=%3C?xml%20version%20=%20%221.0%22%20encoding=%22UTF-8%22?%3E%3Cquery_batch%20version=%222.0%22%20xmlns%20=%20%22http://www.crossref.org/qschema/2.0%22%20xmlns:xsi=%22http://www.w3.org/2001/XMLSchema-instance%22%3E%3Chead%3E%3Cdoi_batch_id%3EDOI%20result%3C/doi_batch_id%3E%3C/head%3E%3Cbody%3E%3Cquery%20key=%22mykey%22%20expanded-results=%22true%22%3E%3Carticle_title%20match=%22fuzzy%22%3E'
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
	
	#print 'Total Num. DOI :', count
	
	return doistring


def rfile(fname) :
	
	tmp_str = ''
	for line in open (fname, 'r') :
		tmp_str = tmp_str + ' ' + line
	
	return tmp_str


def toHttp(tmp_str) :

	for cd in codeURL :
		tmp_str = string.replace(tmp_str, cd[0],cd[1])
	
	return tmp_str



def main():
	if len (sys.argv) != 2 :
		print 'python identifier.py (xml file name)'
		sys.exit (1)

	input = rfile(str(sys.argv[1]))
	extractId(input)


if __name__ == '__main__':
	main()

