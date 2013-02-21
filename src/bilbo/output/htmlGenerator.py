#!/usr/bin/env python
# encoding: utf-8
"""
htmlGenerator.py

Created by Young-Min Kim on 2011-06-17.

"""

import sys
import os

labels =  {'.':0, ',':0, '(':0, ')':0, ':':0, ';':0, '«':0, '»':0, '-':0, '—':0, '“':0, '”':0, '{':0, '}':0, '[':0, ']':0,  '!':0, '?':0}


def simpleComp(truefile, estfile, indicator):
	
	est = []
	for line in open (estfile, 'r') :
		line = line.split()
		if len(line) != 0 :
			est.append(line[0])

	num = 0
	j = 0
	preLabel = 'start'
	print '<meta charset="UTF-8">\n'
	print '<html>\n'
	for line in open (truefile, 'r') :
		if preLabel == 'start' :
			num += 1
			print 'No.'+str(num)+'<br>'
			#print '<br>'
		
		line = line.split()
		if len(line) != 0 :
			currToken = line[0]
			currLabel = line[len(line)-1]
			estLabel = est[j]
			
			if indicator == 2 : currLabel = estLabel
			
			if (preLabel == currLabel) :
				print currToken,
			else :
				if preLabel == 'start' :
					#print '</'+preLabel+'>'
					print_layout(currLabel, currToken, 1)
					pass
				else :
					print_layout(currLabel, currToken, 0)
				#print '<'+currLabel+'>',
				#print currToken,
			preLabel = currLabel	
			j += 1
		else : 
			print '</font>'
			print '<br><br>'
			preLabel = 'start'
			
	print '\n</html>\n'
		
	return
	
def print_layout(currLabel, currToken, st) :
	if (currLabel =='surname') :
		color = 'lightslategray'
	elif (currLabel =='forename') :
		color = 'plum'
	elif (currLabel =='title') :
		color = 'lightblue'
	elif (currLabel =='booktitle') :
		color = 'peachpuff'
	elif (currLabel =='date') :
		color = 'mistyrose'
	elif (currLabel =='publisher') :
		color = 'cornflowerblue'
	elif (currLabel =='c') :
		color = 'tan'
	elif (currLabel =='place') :
		color = 'palevioletred'
	elif (currLabel =='biblscope') :
		color = 'lemonchiffon'
	elif (currLabel =='abbr') :
		color = 'khaki'
	elif (currLabel =='orgname') :
		color = 'lavender'
	elif (currLabel =='nolabel') :
		color = 'lightcyan'
	elif (currLabel =='bookindicator') :
		color = 'thistle'
	elif (currLabel =='extent') :
		color = 'darkseagreen'
	elif (currLabel =='edition') :
		color = 'lightsteelblue'	
	elif (currLabel =='name') :
		color = 'skyblue'
	elif (currLabel =='pages') :
		color = 'lightpink'
	elif (currLabel =='w') :
		color = 'seagreen'
	else : #genname ref namelink author region
		color = 'peru'
	
	if st == 1 :
		str = "<font style=\"background:"+color+"\">"+currToken
	else :
		str = "</font><font style=\"background:"+color+"\">"+currToken
	print str,
	



def main():
	if len (sys.argv) != 4 :
		print 'python htmlGenerator.py (Input and true label file) (Estimated label file) (truefile=1 or estfile=2)'
		sys.exit (1)

	simpleComp(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]))


if __name__ == '__main__':
	main()

