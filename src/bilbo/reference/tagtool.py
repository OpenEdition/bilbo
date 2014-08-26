# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on March 9, 2013

@author: Young-Min Kim

"""
from bs4 import BeautifulSoup
import re

def _findTagPosition(tmp_str, tagName, ptr):
		
	st1 = tmp_str.find('<'+tagName, ptr)
	ed1 = tmp_str.find('>', st1) + 1
	st2 = tmp_str.find('</'+tagName+'>', st1)
	ed2 = tmp_str.find('>', st2) + 1
	
	return st1, ed1, st2, ed2
	
	
def _exchangeTagPairs(tmp_str, tagName, a, bb, c, d):
		
	st1 = tmp_str.find('<'+tagName+'>', bb)
	ed1 = tmp_str.find('>', st1) + 1
	st2 = tmp_str.find('</'+tagName+'>', st1)
	ed2 = tmp_str.find('>', st2) + 1
	tmp_str = _moveSecondTag(tmp_str, a, bb, st1, ed1)
	tmp_str = _moveFirstTag(tmp_str, st2, ed2, c, d)
		
	return tmp_str
	
	
def _deleteTag(tmp_str, tagName, ptr):
		
	st1 = tmp_str.find('<'+tagName+'>', ptr)
	ed1 = tmp_str.find('>', st1) + 1
	st2 = tmp_str.find('</'+tagName+'>', st1)
	ed2 = tmp_str.find('>', st2) + 1
	if  st1 >= 0 and ed1 > 0 and st2 > 0 and ed2 > 0 :
		tmp_str = tmp_str[:st1]+tmp_str[ed1:st2]+tmp_str[ed2:]
		
	return tmp_str
	
	
def _insertTag(tmp_str, tagName, ptr):
	"""
	Insert a tag at the position ptr 
	"""
	tmp_str = tmp_str[:ptr]+tagName+tmp_str[ptr:]

	return tmp_str, len(tagName)
	
	
def _delAllandWrap(tmpRef, found, tagName, a, d):
								
	for f in found :
		tmpRef = _deleteTag(tmpRef, f, a)
		d -= 2*len(f)+len('<></>')
	tmpRef, move = _insertTag(tmpRef, '<'+tagName+'>', a)
	tmpRef, move = _insertTag(tmpRef, '</'+tagName+'>', d+move)
	d = d+move
			
	return tmpRef, d
	
	
def _devideHi(tmpRef, found, hiString, ptr):
	pre_ed = 0	
	for i in range(len(found)) :
		move = 0
		st1, ed1, st2, ed2 = _findTagPosition(tmpRef, found[i], ptr)
		if i != 0 : 
			if len(tmpRef[pre_ed:st1].split()) > 0 : 
				#print '**'+tmpRef[pre_ed:st1]+'**'
				tmpRef, move = _insertTag(tmpRef, hiString, pre_ed)
				tmpRef, move = _insertTag(tmpRef, '</hi>', st1+move)
				st1 = st1+len(hiString)+len('</hi>')
				st2 = st2+len(hiString)+len('</hi>')
				ed2 = ed2+len(hiString)+len('</hi>')
			tmpRef, move = _insertTag(tmpRef, hiString, st1)
		ptr = st2+move
		if i != len(found)-1 :
			nptr = ed2+move
			tmpRef, move = _insertTag(tmpRef, '</hi>', nptr)
			pre_ed = nptr+move
		else :
			st1 = tmpRef.find('</hi>', ed2)
			if len(tmpRef[ed2:st1].split()) > 0 :
				#print '**'+tmpRef[ed2+move:st1]+'**'
				nptr = ed2+move
				tmpRef, move = _insertTag(tmpRef, '</hi>', nptr)
				tmpRef, move = _insertTag(tmpRef, hiString, nptr+move)
		ptr = ptr+move
		
	return tmpRef
	
	
def _isName(tmpRef, centre, found, includedLabels, a):
		
	isName = False
	#check the certain case of name
	#1. include initial expression
	tmp_centre = centre
	for f in found : tmp_centre = _deleteTag(tmp_centre, f, 0)
	for tmp in tmp_centre.split() : 
		retrn_str = _initCheck(tmp)
		if retrn_str != '' : isName = True
	#2. First label of reference
	#2-1 first label
	if not isName :
		isName = True
		bs = BeautifulSoup(tmpRef[:a])
		for b in bs.find_all() :
			if b.name in includedLabels : isName = False
	#2-2 first label after ";"
	if not isName :
		ptr_semi = (tmpRef[a::-1]).find(";", 0)
		if ptr_semi > 0 :
			isName = True
			bs = BeautifulSoup(tmpRef[a-ptr_semi:a])
			for b in bs.find_all() :
				if b.name in includedLabels : isName = False
	#final check, include ':' it's not a name
	if centre.find(':') > 0 : isName = False

	return isName
	
	
def _hasTitleAfterSemi(tmpRef, a, d):
	"""
	Check if current reference has name by verifying from the previous semicolon,
	because references in a note are often separated by a semicolon.
	"""
	hasTitle = True
	ptr_semi = (tmpRef[a::-1]).find(";", 0)
	if ptr_semi > 0 :
		bs = BeautifulSoup(tmpRef[a-ptr_semi:d])
		if len(bs.find_all("^title")) == 0 :
			hasTitle = False

	return hasTitle
		
	
def _initCheck(input_str) :
	"""
	Check initial expressions
	"""
	init1 = re.compile('^[A-Z][a-z]?\.-?[A-Z]?[a-z]?\.?')
	init2 = re.compile('^[A-Z][a-z]?-[A-Z]?[a-z]?\.?')
	init3 = re.compile('^[A-Z][A-Z]?\.?-?[A-Z]?[a-z]?\.')
	p1 = init1.findall(input_str)
	p2 = init2.findall(input_str)
	p3 = init3.findall(input_str)
		
	retrn_str = ''
	if p1 : 
		retrn_str = p1[len(p1)-1]
	elif p2 : 
		retrn_str = p2[len(p2)-1]
	elif p3 : 
		retrn_str = p3[len(p3)-1]
	
	return retrn_str
	

		
def _exchangeTags(oriRef, st1, ed1, st2, ed2):
	"""
	Exchange the position of two tags
		A		<B>		  C			<D>		E
	[:st1] [st1:ed1] [ed1:st2] [st2:ed2] [ed2:]
	->
		A		<D>		  C			<B>		E
	"""
	tmpRef = oriRef[:st1] + oriRef[st2:ed2] + oriRef[ed1:st2]
	tmpRef += oriRef[st1:ed1] + oriRef[ed2:]		
		
	return tmpRef
	
	
def _moveFirstTag(oriRef, st1, ed1, st2, ed2):
	"""
	Exchange the position of two tags by moving the first tag
		A		<B>		  C			<D>		E
	[:st1] [st1:ed1] [ed1:st2] [st2:ed2] [ed2:]
	->
		A		C		<D>			<B>		E
	"""
	tmpRef = oriRef[:st1] + oriRef[ed1:st2] + oriRef[st2:ed2]
	tmpRef += oriRef[st1:ed1] + oriRef[ed2:]		
		
	return tmpRef
	
	
def _moveSecondTag(oriRef, st1, ed1, st2, ed2):
	"""
	Exchange the position of two tags by moving the second tag
		A		<B>		  C			<D>		E
	[:st1] [st1:ed1] [ed1:st2] [st2:ed2] [ed2:]
	->
		A		<D>		 <B>		C		E
	"""
	tmpRef = oriRef[:st1] + oriRef[st2:ed2] + oriRef[st1:ed1]
	tmpRef +=  oriRef[ed1:st2] + oriRef[ed2:]		
		
	return tmpRef
	
	
def _closestPreTag(oriRef, ptr1):
	"""
	Find the position of closest previous tag from a position
	"""
	startck1 = (oriRef[ptr1::-1]).find(">", 0)
	startck2 = (oriRef[ptr1::-1]).find("<", startck1)
	st = ptr1-startck2
	ed = ptr1-startck1+1		
	tagName = ((oriRef[st:ed].split('>')[0]).split()[0])[1:]

	return st, ed, tagName
		
	
def _preOpeningTag(oriRef, ptr1, tagN, prePtrlimit):
	"""
	Find the position of previous tag called tagN from a position
	"""
	tagName = ''
	startck2 = 0
	startck1 = 0
		
	while tagName != tagN or startck1 < 0:
		startck1 = (oriRef[ptr1::-1]).find(">", startck2)
		startck2 = (oriRef[ptr1::-1]).find("<", startck1)
		st = ptr1-startck2
		ed = ptr1-startck1+1		
		tagName = ((oriRef[st:ed].split('>')[0]).split()[0])[1:]
	if prePtrlimit > st :
		tagName = ''
			
	return st, ed, tagName

	
def _totallyWrapped(oriRef):
		
	limitst1 = -1
	limited1 = -1
	limitst2 = -1
	limited2 = -1
		
	s = BeautifulSoup(oriRef)
		
	tagName = "NOTAG"
	if s.find("bibl") : tagName="bibl"
	elif s.find("note") : tagName="note"
	if s.find(tagName) and len(s.find(tagName)) == 1 :
		if s.find_all() and len(s.find_all()) > 3 : #totally wrapped
				
			tagLimit = s.find_all()[3].name
			limitst1 = oriRef.find('<'+tagLimit, 0)
			limited1 = oriRef.find('>', limitst1)
			
			startck1 = (oriRef[::-1]).find("<")
			startck1 = (oriRef[::-1]).find("<",startck1)
			limitst2 = oriRef.find('</'+tagLimit, startck1)
			limited2 = oriRef.find('>', limitst1)
		
	return limited1, limitst2
