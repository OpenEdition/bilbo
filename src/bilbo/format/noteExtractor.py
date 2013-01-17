#!/usr/bin/env python
# encoding: utf-8
"""
noteExtractor.py

Created by Young-Min Kim on 2011-07.

<note> extractor developed for corpus 2.
Because of a limit** of BeautifulSoup, a htmp/xml parser used in Bilbo,
a preprocessing is necessary before generating the primary data from
manually annotated xml files. Extracted notes are used to making 
training/test data for the classifiaction of <bibl>/<nonbibl> notes.


** If a tag contains a inner tag with identical name, BeautifulSoup can 
not correctly parse the contents from the start of identical inner tag.
It will disturb <note> and <bibl> extraction. That is why we need this
preprocessing code. A solution is to avoid using same inner tags in a 
xml tree even though they have different attributes. In our case, <hi>
tags cause the problem. In this version, a <bibl> can also have another
<bibl> inside of it, but this case always occurs with <relatedItem> tag,
and is already handled. 
"""

import sys
import os
import re
import string
import subprocess

sys.path.append("/Users/young-minkim/Codes/Lib")
from BeautifulSoup import BeautifulSoup

tagAttDict = {'0000': 0}

def processing (fname) :
	
	try :

		tmp_str = ''
		for line in open (fname, 'r') :
			tmp_str = tmp_str + ' ' + line
			
		soup = BeautifulSoup (tmp_str)
		
		stop = len(tmp_str)
		
		i = 0
		
		while i < len(tmp_str) :
		
			n = tmp_str.find('<note place',i)
	
			if (n > 0 and n < stop) :
	
				m = n+len('<note place=')

				n2 = tmp_str.find('</note>', m)
				m2 = n2+len('</note>')
					
				### print result
				tmp_str2 = tmp_str[n:m2]
				#print tmp_str2
				new_str = elimination (tmp_str2)
				print new_str
				#if (new_str != tmp_str2) : raw_input("Press Enter to Exit")
				i = m2
			
			else :
				i = len(tmp_str)

							
	except :
		pass
		print 'reading error\n\n'
		return
		
	return
	

def elimination (tmp_str) :
	
	targer_tag_st = "<hi font-variant=\"small-caps\">"
	targer_tag_end = "</hi>"
	
	new_str = tmp_str
	a = tmp_str.find(targer_tag_st,0)
	while a > 0 :
		b = a + len(targer_tag_st)
		c = tmp_str.find(targer_tag_end, b)
		d = c + len(targer_tag_end)
		
		new_str =  tmp_str[0:a] + tmp_str[b:c] + tmp_str[d:len(tmp_str)]
		tmp_str = new_str
		a = tmp_str.find(targer_tag_st,0)
		#raw_input("Press Enter to Exit")
		
	return new_str



def main() :
	
	if len (sys.argv) != 2 :
		print 'python noteExtractorC2.py (dirname including xml files)'
		sys.exit (1)
	
	
	command = 'ls '+str(sys.argv[1])+' > tmpfilelist.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()	
	
	print '<listBibl>\n'
	dirname = str(sys.argv[1])
	for line in open ("tmpfilelist.txt", 'r') :
		line = string.split(line,'\n')
		fname = dirname + str(line[0])
		
		processing(fname)
	print '\n</listBibl>\n'
	
	command = 'rm tmpfilelist.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	


if __name__ == '__main__':
	main()

