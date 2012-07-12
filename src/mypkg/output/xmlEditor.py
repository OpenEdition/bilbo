#!/usr/bin/env python
# encoding: utf-8
"""
xmlEditor.py

Created by Young-Min Kim on 2011-05-30.

"""

import sys
import os
import string

labels =  {'.':0, ',':0, '(':0, ')':0, ':':0, ';':0, '«':0, '»':0, '-':0, '“':0, '”':0, '{':0, '}':0, '[':0, ']':0,  '!':0, '?':0}


def simpleComp(truefile, orifile):
	
	ori = []
	ori.append([])
	
	for line in open (orifile, 'r') :
		line = line.split('\n')
		if len(line[0]) != 0 :
			ori[len(ori)-1].append(line[0])
		else : 
			ori.append([])
	
	true = []
	true.append([])
	
	for line in open (truefile, 'r') :
		line = line.split('\n')
		if len(line[0]) != 0 :
			true[len(true)-1].append(line[0])
		else : 
			true.append([])

	for i in range(len(true)) :
		for j in range(len(true[i])) :
			n = true[i][j].find('<hi rend="italic">')
			str = ''
			if n >= 0 :
				nn = n+len('<hi rend="italic">')
				m = true[i][j].find('</hi>')
				str = true[i][j][nn+1:m-1]
				
			if len(str) > 0 :
				#print str, ori[i][j]
				
				nstr = '<hi rend="italic"> '+str+' </hi>'
				
				if ori[i][j].find(str) < 0 :
					print i,j
				
				ori[i][j] = string.replace(ori[i][j], str, nstr)
				#print str, ori[i][j]
	
	
	#print true[105]
	#print ori[105]
	
	#for bibl in ori :
	#	for l in bibl :
	#		print l
	#	print
			
	
	return
	


def main():
	if len (sys.argv) != 3 :
		print 'python xmlEditor.py (xml correct file) (xml file to be modified)'
		sys.exit (1)

	simpleComp(str(sys.argv[1]), str(sys.argv[2]))


if __name__ == '__main__':
	main()

