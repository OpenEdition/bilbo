#!/usr/bin/env python
# encoding: utf-8
"""
dataGeneratorV3C2.py

Created by Young-Min Kim on 2011-05-30.
Modified on 2011-08-08 for the extraction of notes (corpus2).

This this a modification of dataGenerator.py. Created for the
third experiment for the automatic labeling of references. A 
dictionary data 'tagAttDict' is added to extract all the types
of tag-attribute pairs. Undo the commented part at the end of
the main() to check up the extracted 'tagAttDict'. This code
is able to extract more in detail the attributes than the first
version.

+
For corpus2, we first need to separate notes in two groups where
one has notes with bibliographic information and the other without
this information. This verification is necessary because we have
no prior information about this for a new note to be estimated.

To sum up, this version includes the extraction of NONBIBL labels
that enable the creation of data for BIBL/NONBIBL classification.
This is the main difference compared to "dataGeneratorV3.py".

If the desired data is for CRF learning, use "dataGeneratorV3.py"
after using "biblExtractorC2V2.py" when the aimed corpus is level2
(Notes).
-------------------------------------------------------------------
Modified on 2012-04-04 for the extraction of data in the case of 
including tags in non-bibliographical notes.

"""

import sys
import os
import re
import string


from mypkg.ressources.BeautifulSoup import BeautifulSoup
from mypkg.ressources.BeautifulSoup import Tag
tagAttDict = {'0000': 0}
refSign = []
precitSign = []

def processing (fname) :
	
	try :

		tmp_str = ''
		for line in open (fname, 'r') :
			line = re.sub(' ', ' ', line)	# !!! eliminate this character representing a kind of SPACE but not a WHITESPACE
			line = line.replace('“', '“ ')			# !!! sparate the special characters '“', '”'
			line = line.replace('”', ' ”')			# !!! sparate the special characters '“', '”'
			line = line.replace('&amp;', '&')	
			line = posssign(line, refSign)		# term or phrase representing the reference part in note, IF THIS IS A PHRASE INSERT DASH BETWEEN WORDS
			line = posssign(line, precitSign)	# term or phrase indicating the previously cited reference, IF THIS IS A PHRASE INSERT DASH BETWEEN WORDS
			tmp_str = tmp_str + ' ' + line
			

		tmp_str = elimination (tmp_str)
		tmp_str = html2unicode(tmp_str)
		#tmp_str = tmp_str.decode('utf8')
		#tmp_str = bytes.fromhex(tmp_str).decode('utf-8')
		soup = BeautifulSoup (tmp_str)
		
		for nt in soup.findAll ('note') :

			#print len(nt), nt.contents
			c = 0
			for nt_c in nt.contents :
				if nt_c == nt_c.string :
					pass
				elif nt_c.name == 'bibl' : # bibl or other tag
					#print nt_c.name
					pass
				elif nt_c.findAll('bibl') : ############### structure flatten, pull <bibl> to top level for the extraction #################
					#print nt_c
					#print nt_c.name
					newc = nt_c.findAll('bibl')
					#print '***', len(newc), '***'
					
					#if nt_c.name != newc[0].findParents()[0].name : # parent tag
											
					nsoup = BeautifulSoup (nt_c.renderContents())
					#print nsoup.contents, len(nsoup.contents)
					nt_c.replaceWith( nsoup.contents[0] )
					#print nsoup.contents, len(nsoup.contents)
					nsouplen = len(nsoup.contents)
					if (nsouplen > 0) :
						for iter in range(nsouplen) :
							#print 'herehere'
							nt.insert(c+1+iter,Tag(soup,"mytag"))
							nt.mytag.replaceWith( nsoup.contents[0] )
							
					#print nt.contents, len(nt.contents)
					
					#raw_input("Press Enter to Exit")
					
					pass
				
				c += 1
				
			#raw_input("Press Enter to Exit1")
			
			j = 0
			i = 0
			s = nt.findAll ('bibl')	
			sAll = nt.contents 
			#while i < len(s) :
			while j < len(sAll) :
				b = sAll[j]
				#b = s[i]	#each bibl 
				if b != b.string :
					allTags = b.findAll(True)					#extract all tags in the current bibl
					
					if len(allTags) > 0 :	##### if there is any tags, but we should consider <nonbibl> containing tags in it #####
						#current_tag = b(allTags[0].name)[0]
						for c_tag in b.contents :
							if len(c_tag) > 0  and str(c_tag) != "\n" :
								
								if (c_tag != c_tag.string) :
									extract_tags(c_tag, len(s)) ##### modified on 2012-04-04 for the case of including tags in non-bibl notes #####
								else :
									c_tag_str = string.split(c_tag)
									if len(c_tag_str) > 0 and c_tag_str != "\n" :
										for ss in c_tag_str :
											print ss.encode('utf8'),
											if len(s) > 0 :
												print '  ++ ++  ' + 'nolabel'
											else :
												print '  ++ ++  ' + 'nonbibl'
											

						if b.find('relateditem') :					# related item
							j += 1
							br =  sAll[j]
							print '********in********'

							allTags = br.findAll(True)					#extract all tags in the current bibl
							#current_tag = br(allTags[0].name)[0]
							for c_tag in br.contents :
								if len(c_tag) > 0  and str(c_tag) != "\n" :
									if (c_tag != c_tag.string) :
										extract_tags(c_tag, len(s))
									else :
										c_tag_str = string.split(c_tag)
										if len(c_tag_str) > 0 and c_tag_str != "\n" :
											for ss in c_tag_str :
												print ss.encode('utf8'),
												print '  ++ ++  ' + 'nolabel'
						#print
					else :
						if len(b.contents) > 0 :
							input_str = b.contents[0]
							for input in input_str.split() :
								print input.encode('utf8'), '  ++',
								if len(b.attrs) : print b.attrs[0][1],
								print '++  ', b.name, 'nonbibl'
								
							#print b.contents[0], '  ++', 
							#if len(b.attrs) : print b.attrs[0][1],
							#print '++  ', b.name, 'nonbibl'
							#raw_input("Press Enter to Exit2")
							
						
				elif len(b.split()) > 0 :
					#print b, '  ++ ++  ', 'nonbibl'
					for input in b.split() :
						print input.encode('utf8') + '  ++ ++  nonbibl'
					#raw_input("Press Enter to Exit3")
						
				#else : print
				
				j += 1
			print
					
	except :
		pass
		print 'reading error\n\n'
		return
		
	return
	

def load_sign(fname, sign) :

	for line in open (fname, 'r') :
		
		nline = ''
		sn = ''
		for n in line.split() :
			nline = nline+'-'+n
			sn = sn+' '+n

		nline = nline[1:len(nline)]
		nline = re.sub(',', '', nline)
		nline = re.sub('\.', '', nline)
		sn = sn[1:len(sn)]
	
		sign.append([])
		sign[len(sign)-1].append(sn)
		sign[len(sign)-1].append(nline)
		
	
	return


def posssign(line, sign) :

	for s in sign :
		nline = line.replace(s[0], s[1]) # When re.sub is used, french accents were broken
		#nline = line
		if nline != line :
			line = nline
			#print s[0], s[1]
			#print line 
			#raw_input("Press Enter to Exit")
	
	return line
	
	



def extract_tags(current_tag, lens) :

	txts = []
	tokens = []
	tags = []
	attrs = []

	
	#read current tag
	n = current_tag
	top_tag = n.name
	top_att = ''

			
	#read attributes 
	if len(n.attrs) > 0 :					# if attributes exist
		top_att = ''
		attstyp_string = ''
		for curr_att in n.attrs :
			top_att = top_att + curr_att[1]+' '
			attstyp_string = attstyp_string+curr_att[0]+' '
			
		tagatt_string = n.name+' '+ attstyp_string+' '+top_att
		if tagAttDict.has_key(tagatt_string) :
			tagAttDict[tagatt_string] += 1
		else : 
			tagAttDict[tagatt_string] = 1	
		
	else :
		pass

		
	#read contents
	if str(n.string) == 'None' :			# case1 : no contents, case2 : tags in current tag
		ncons = len(n.contents)

		if ncons == 0 :						#case1
			pass
		else :								#case2
			arrangeData(n, txts, tags, attrs, top_tag, top_att)
								
	else :									#case 3 just a content, no tags in it
		txt = n.string
		txts.append(txt)
		tags.append([])
		attrs.append([])
		ct = len(txts)
		tags[ct-1].append(top_tag)
		if (top_att) : attrs[ct-1].append(top_att)
		st = string.split(n.string)
		for s in st :
			tokens.append(s)
	
	#print result
	
	for j in range(0,len(txts)) :
		if str(txts[j]) == 'None' or str(txts[j]) == '\n':
			print '!NONE!   ++',
			for attr in attrs[j] :
				print attr,
			print '++  ',
			for tag in tags[j] :
				print tag,
			if not lens > 0 : print 'nonbibl',
			print
		#elif len(tags[j]) == 1 and tags[j][0] == 'num' : # to eliminate <num> tag which appears just one time. But... tokens are also eliminated.
		#	pass
		else :
			st = string.split(str(txts[j]))
			for s in st :
				print s,'  ++',
				for attr in attrs[j] :
					print attr,
				print '++  ',
				for tag in tags[j] :
					print tag,
				if not lens > 0 : print 'nonbibl',
				print
	
	return


def arrangeData(n, txts, tags, attrs, top_tag, top_att) :
	for con in n.contents :
		txt = con.string
		if str(txt) != 'None' : 
			txts.append(txt)
			tags.append([])
			attrs.append([])
			ct = len(txts)
			tags[ct-1].append(top_tag)
			if (top_att) : attrs[ct-1].append(top_att)		# APPEND ATTRIBUTE

			if con == con.string :
				pass
			else :
				tags[ct-1].append(con.name)
				if len(con.attrs) > 0 : 
					atts_string = ''
					attstyp_string = ''
					for curr_att in con.attrs :
						atts_string = atts_string + curr_att[1]+' '
						attstyp_string = attstyp_string + curr_att[0]+' '
					attrs[ct-1].append(atts_string)
					#print atts_string
					
					tagatt_string = con.name+' '+attstyp_string+' '+atts_string
					if tagAttDict.has_key(tagatt_string) :
						tagAttDict[tagatt_string] += 1
					else : 
						tagAttDict[tagatt_string] = 1
				
		else : 				#case2b : more than 2 levels
			temp_str = top_tag+' '+con.name
			atts_string = ''
			for curr_att in con.attrs :
				atts_string = atts_string + curr_att[1]+' '
			temp_attr = top_att+' '+atts_string
			arrangeData(con, txts, tags, attrs, temp_str, top_att)
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


def html2unicode(tmp_str) :

	#for numerical codes
	matches = re.findall("&#\d+;", tmp_str)
	if len(matches) > 0 :
		hits = set(matches)
		for hit in hits :
			name = hit[2:-1]
			try :
				entnum = int(name)
				tmp_str = tmp_str.replace(hit, unichr(entnum))
			except ValueError:
				pass

	#for hex codes
	matches = re.findall("&#[xX][0-9a-fA-F]+;", tmp_str)
	if len(matches) > 0 :
		hits = set(matches)
		for hit in hits :
			hex = hit[3:-1]
			try :
				entnum = int(hex, 16)
				#print unichr(entnum)
				tmp_str = tmp_str.replace(hit, unichr(entnum))
			except ValueError:
				pass
				
	return tmp_str


def main() :
	
	if len (sys.argv) != 3 :
		print 'python (dirname including xml files) (filelist)'
		sys.exit (1)
	
#	load_sign("/Users/young-minkim/Project/Data/Resources/refTerms.txt", refSign)
	#print refSign
	#raw_input("Press Enter to Exit")
	
#	load_sign("/Users/young-minkim/Project/Data/Resources/precitTerms.txt", precitSign)
	#print precitSign
	#raw_input("Press Enter to Exit")
	
	dirname = str(sys.argv[1])
	for line in open (str(sys.argv[2]), 'r') :
		line = string.split(line,'\n')
		fname = dirname + str(line[0])
		
		processing(fname)
	
	"""
	del tagAttDict['0000']
	keylist = tagAttDict.keys()
	keylist.sort()
	for key in keylist:
		pass
	    print "%s: %s" % (key, tagAttDict[key])
	
	print len(tagAttDict)
	"""


if __name__ == '__main__':
	main()

