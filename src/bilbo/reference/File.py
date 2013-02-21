# -*- coding: utf-8 -*-
'''
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
'''
from bs4 import BeautifulSoup, NavigableString
from bilbo.format.Clean import Clean
from bilbo.format.CleanCorpus1 import CleanCorpus1
from bilbo.format.CleanCorpus2 import CleanCorpus2
from bilbo.format.Rule import Rule
from bilbo.reference.ListReferences import ListReferences
from bilbo.output.identifier import extractDoi, loadTEIRule, toTEI
import re
import sys

prePunc =  {'.':0, ',':0, ')':0, ':':0, ';':0, '-':0, '”':0, '}':0, ']':0, '!':0, '?':0, '/':0}
postPunc = {'(':0, '-':0, '“':0, '{':0, '[':0}
specialPunc =  {'«':0, '»':0, '“':0, '”':0, '"':0, '–':0, '-':0}

prePtrlimit = -1
postPtrlimit = -1

class File(object):
	'''
	A file class containing all references in a file
	'''

	def __init__(self, fname, options):
		'''
		Attributes
		----------
		nom : string
			target file name
		corpus : dictionary of reference list
			 references in the file
		'''
		self.nom = fname
		self.corpus = {}
		self.options = options
	

	def extract(self, typeCorpus, tag, external):
		'''
		Extract references
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		tag : string, {"bibl", "note"}
			tag name defining reference types
			"bibl" : corpus 1, "note" : corpus 2
		external : int, {1, 0}
			1 : if the references are external data except CLEO, 0 : if that of CLEO
			it is used to decide whether Bilbo learn call a SVM classification or not.			
		'''	
		clean = Clean()
		if typeCorpus == 1:
			clean = CleanCorpus1()
		elif typeCorpus == 2:
			clean = CleanCorpus2()
			
		#print self.nom
		references = clean.processing(self.nom, tag, external)
		if len(references) >= 1:
			self.corpus[typeCorpus] = ListReferences(references, typeCorpus)
			rule = Rule()
			rule.reorganizing(self.corpus[typeCorpus])


	def getListReferences(self, typeCorpus):
		'''
		Return reference list
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		'''
		try:
			return self.corpus[typeCorpus]
		except :
			return -1
		

	def nbReference(self, typeCorpus):
		'''
		count the number of references
		'''
		try:
			return self.corpus[typeCorpus].nbReference()
			
		except :
			return 0	
			
	
	def _html2unicode(self, tmp_str) :
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
					tmp_str = tmp_str.replace(hit, unichr(entnum))
				except ValueError:
					pass
		
		tmp_str = tmp_str.replace('&','&amp;')
		
		return tmp_str

	
	def buildReferences(self, references, tagTypeCorpus, typeCorpus, dirResult):
		'''
		Construct final xml output file, called from Corpus::addTagReferences
		Unlike the first version, compare token by token, replace the token by automatically tagged token. 
		That's why we keep perfectly the original data format
		
		Parameters
		----------
		references : list 
			automatically annotated references by system
		tagTypeCorpus : string, {"bibl", "note"}
			tag name defining reference types
			"bibl" : corpus 1, "note" : corpus 2
				typeCorpus : int, {1, 2, 3}
		type of corpus
			1 : corpus 1, 2 : corpus 2...
		tagTypeList : string, "listbibl"
			tag name wrapping all references
		
		Attributes
		----------
		
		'''
		cptRef = 0		#reference counter
		tmp_str = ""
		ref_ori = []
		
		'Read the source file to check the initial contents of references'
		for line in open (self.nom, 'r') :
			tmp_str = tmp_str + line
		
		soup = BeautifulSoup (tmp_str)
		s = soup.findAll (tagTypeCorpus)
		
		basicTag = {} #tags existing in the original files

		for ss in s :
			for sss in ss.find_all() :
				basicTag[sss.name] = 1

		tagConvert = {}
		tagConvert = loadTEIRule(tagConvert)
		
		'Reconstruct references by checking input string token by token'
		includedLabels = {}
		for ref in references:
			for reff in ref.find_all() :
				includedLabels[reff.name] = 1
				try : del basicTag[reff.name]
				except : pass 
			parsed_soup = ''.join(s[cptRef].findAll(text = True)) # String only
			ptr = 0
			if (len(parsed_soup.split()) > 0) : #if empty <bibl>, pass it
				oriRef = (str(s[cptRef]))

				for r in ref.contents :
					ck = 0
					try : r.name
					except : ck = 1
					if ck == 0 and not r.name == "c" and not r.name == "nonbibl" and r.string:
						r.string = r.string.replace('&', "&amp;")
						for token in r.string.split() :
							#if token == "&" : token = "&amp;"
							token = token.encode('utf8')
							pre_ptr = ptr
							ptr = oriRef.find(token, ptr)
							while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) and oriRef.find("<", ptr) > 0 :
								ptr = oriRef.find(token, ptr+1)
							if oriRef.find("<", ptr) < 0 : ptr = -1
							
							inner_string = ""
							if ptr >= 0 :
								tmp_str2 = oriRef[pre_ptr:ptr]
								soup2 = BeautifulSoup (tmp_str2)
								for s2 in soup2 :
									try : inner_string = ''.join(s2.findAll(text = True))
									except : pass
									inner_string = inner_string.encode('utf8')
							#EXCEPTION
							if (ptr < 0) or inner_string.find(token) >= 0 : 
								#try again by eliminating tags
								c = token[0]
								ptr = oriRef.find(c, pre_ptr)
								while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) : # the token is in a tag
									ptr = oriRef.find(c, ptr+1)
								ptr_start = ptr
								newtoken = ""
								if (oriRef.find("</", ptr) < oriRef.find(">", ptr)) : #case) <hi rend="sup">c</hi>Awâd,
									tag_start_l = oriRef.find("<",ptr_start)
									tag_start_r = oriRef.find(">",tag_start_l)
									newtoken = oriRef[ptr_start:tag_start_l]
									mtoken_r = oriRef.find(token[len(token)-1],tag_start_r)
									newtoken += oriRef[tag_start_r+1:mtoken_r+1]
									#print token[len(token)-1], oriRef[mtoken_r+1]
									ptr_start = ptr_start - oriRef[ptr_start:pre_ptr:-1].find("<",0)
									ptr_end = mtoken_r
								else :												#case) B<hi font-variant="small-caps">ayram</hi>
									tag_start_l = oriRef.find("<",ptr_start)
									tag_start_r = oriRef.find(">",tag_start_l)
									tag_end_l = oriRef.find("<",tag_start_r)
									tag_end_r = oriRef.find(">",tag_end_l)
									ptr_end = tag_end_r
									newtoken = oriRef[ptr_start:tag_start_l]+oriRef[tag_start_r+1:tag_end_l]
									newtoken = re.sub(' ', ' ', newtoken)
									newtoken = newtoken.lstrip()
									newtoken = newtoken.rstrip()
								if newtoken == token or newtoken.find(token) >= 0: 
									token = oriRef[ptr_start:ptr_end+1]
									ptr = ptr_start
								else :
									print pre_ptr, ptr, '*'+newtoken+'*', token
									print "PROBLEM, CANNOT FIND THE TOKEN", token
									print s[cptRef]
									ptr = -1
									pass
							else :
								while (oriRef.find(">", ptr) < oriRef.find("<", ptr)) : # the token is in a tag
									ptr = oriRef.find(token, ptr+1)
							
							if (ptr >= 0) :
								nstr = "<"+r.name+">"+token+"</"+r.name+">"
								oriRef = oriRef[:ptr] + nstr + oriRef[ptr+len(token):]
								ptr += len(nstr)
							else :
								ptr = pre_ptr
				
				'check continuously annotated tags to eliminate tags per each token'
				oriRef = self.continuousTags(basicTag, includedLabels, oriRef)
				'arrange name tag'
				oriRef = self.arrangeTagsPerToken(includedLabels, oriRef, tagTypeCorpus)
				
				if oriRef.find("<author>") < 0 : #non-annotated input
					'add persName tags'
					oriRef = self.findAuthor(includedLabels, oriRef)
					'correct missed tag inserting'
					oriRef = self._correctMissTag(oriRef, basicTag, "persName")
				
				if self.options.o == 'tei' :
					oriRef = toTEI(oriRef, tagConvert)
				ref_ori.append(oriRef)
			cptRef += 1
		
		try:
			tmp_str = self.writeResultInOriginal(tmp_str, soup, ref_ori, references, tagTypeCorpus)
			
		except :
			pass

		fich = open(dirResult+self._getName(), "w")
		fich.write(tmp_str)
		fich.close()
		
		return


	def writeResultInOriginal(self, tmp_str, soup, ref_ori, references, tagTypeCorpus):
		cpt = 0
		listRef = soup.findAll(tagTypeCorpus)
			
		pre_p1 = 0
		for ref in listRef:
			contentString ="" # TO CHECK IF THE REFERENCE or NOTE HAS NO CONTENTS
			for rf in ref.contents :
				if rf == rf.string : contentString += rf
					
			for tag in ref.findAll(True) :
					if len(tag.findAll(True)) == 0 and len(tag.contents) > 0 :
						for con in tag.contents :
							contentString += con
			
			'Find the starting and ending of corresponding tag and replace the string by labeled one'
			p1 = tmp_str.find('<'+tagTypeCorpus+'>', pre_p1+10)
			p11 = tmp_str.find('<'+tagTypeCorpus+' ', pre_p1+10)
			if p1 < 0 or (p11 > 0 and p1 > p11) : p1 = p11
			p2 = tmp_str.find('</'+tagTypeCorpus+'>', p1)
			
			if len(contentString.split()) > 0 :
				doistring = ''
				text = str(ref_ori[cpt])
				if self.options.d :
					doistring = extractDoi(str(references[cpt]), tagTypeCorpus)
					if doistring != '' : 
						doistring = 'http://dx.doi.org/'+str(doistring)
						doistring = '<idno type=\"DOI\">'+doistring+'</idno>'
						ptr1 = text.find('</title>')+len('</title>')
						text = text[:ptr1] + doistring + text[ptr1:]
						#print text
				tmp_list = list(tmp_str)
				tmp_list[p1:p2+len('</'+tagTypeCorpus+'>')] = text
				tmp_str = ''.join(tmp_list)

			cpt += 1 
			pre_p1 = p1		
		
		return tmp_str

		
	def continuousTags(self, basicTag, includedLabels, oriRef):
		'''
		Check continuously annotated tags to eliminate tags per each token
		'''
		preTag = ""
		noncontinuousck = ["surname", "forename"]
		newsoup = BeautifulSoup(oriRef)
		ptr2 = 0
		ptr1 = 0
		found = {}
		preparentname = ""
		for ns in newsoup.find_all() :
			if preTag == ns.name and preparentname == ns.parent.name and not preTag in noncontinuousck:
				ptr1 = oriRef.find("</"+preTag+">", ptr2)
				ptr2 = oriRef.find("<"+preTag+">", ptr1)
				if ptr2 > ptr1 and oriRef.find(">", ptr1+len("</"+preTag+">"), ptr2) < 0 :
					token = "</"+preTag+">"
					oriRef = oriRef[:ptr1] + oriRef[ptr1+len(token):]
					token = "<"+preTag+">"
					ptr = oriRef.find(token, ptr1)
					oriRef = oriRef[:ptr] + oriRef[ptr+len(token):]
					found[ns.name] = 0 #there is no other continuous tag after this tag 
					for k in found.keys():
						if k == ns.name : found[k] = 0
						else : found[k] = 1
				ptr2 = ptr1+1
			else :
				if (found.has_key(ns.name) and found[ns.name] == 0) or (preTag == ns.name and preparentname != ns.parent.name and not preTag in noncontinuousck) :
					ptr1 = oriRef.find("</"+ns.name+">", ptr2)
					ptr2 = oriRef.find("<"+ns.name+">", ptr1)
					if ptr2 < 0 : ptr2 = ptr1+1
					for k in found.keys():
						if k == ns.name : found[k] = 0
						else : found[k] = 1
				found[ns.name] = 0
			preTag = ns.name
			preparentname = ns.parent.name
		
		return oriRef

	
	def arrangeTagsPerToken(self, includedLabels, oriRef, tagTypeCorpus):
		'''
		Check if a field of tokens annotated by a label tag has wrapped by other basic tag.
		If yes, change order. It's for prevent the mismatching error of persName tag and 
			also find other continuous tags.
		e.g. To prevent the following error (interruption of <persName> in <hi>)
			<hi font-variant="small-caps"><persName><surname>Alves</surname></hi>
			change order as following before add <persName>
			<surname><hi font-variant="small-caps">Alves</hi></surname>
		e.g. To find undetected continuous tags as follows
			
		'''
		nameck = ["surname", "forename", "namelink", "genname"]
		for tmpTag in includedLabels :
			ptr2 = 0
			ptr1 = oriRef.find('<'+tmpTag+'>', ptr2) #find the starting of an annotated tag
			while ptr1 > 0 :
				ptr2 = oriRef.find('</'+tmpTag+'>', ptr1)+len('</'+tmpTag+'>') #find its ending 
				ptr3 = oriRef.find('</',ptr2)	#find closest other ending tag
				closeTag = ''
				if oriRef.find('<',ptr2,ptr3) < 0 and self._onlyPunc(oriRef[ptr2:ptr3]) : #if there is no starting tag between them and NO char
					ptr4 = oriRef.find('>',ptr3)
					closeTag = oriRef[ptr3+len('</'):ptr4] #extract the closest tag name
					if closeTag not in ["note", "bibl", "listNote", "listBibl"] :
						[st1, ed1, dummyTag] = self._closestPreOpeningTag(oriRef, ptr1)
						if oriRef[st1:ed1].find('<'+closeTag) == 0 and self._onlyPunc(oriRef[ed1:ptr1]) :#if there is no tag between them and NO char
							#then exchange tags
							tmpRef = self._moveSecondTag(oriRef, st1, ed1, ptr1, ptr1+len('<'+tmpTag+'>'))
							tmpRef = self._moveFirstTag(tmpRef, ptr2-len('</'+tmpTag+'>'), ptr2, ptr3, ptr4+1)
							oriRef = tmpRef
				ptr1 = oriRef.find('<'+tmpTag+'>', ptr2)
		#final continuous check
		continuousTagck = []
		for tmpTag in includedLabels :
			continuousTagck.append('</'+tmpTag+'><'+tmpTag+'>')
			if tmpTag not in nameck :
				continuousTagck.append('</'+tmpTag+'> <'+tmpTag+'>')
				continuousTagck.append('</'+tmpTag+'> <'+tmpTag+'>')

		for tmpTag in continuousTagck :
			oriRef = oriRef.replace(tmpTag,'')

		return oriRef
	
	
	def _onlyPunc(self, tmp_str):
		
		new_str = tmp_str.replace(' ', ' ')
		for key in specialPunc.iterkeys(): new_str = new_str.replace(key, ' ')
		new_str = re.sub('\W', ' ', new_str)
		onlyPunc = False
		if len(new_str.split()) == 0 : onlyPunc = True
					
		return onlyPunc
			
			
	def findAuthor(self, includedLabels, oriRef):
		'''
		Post-processing RULE about author field
		Separate surname and forename pair per author
		Step 1. check group of fields continuously tagged as surname or as forename over whole string
		Step 2. per group, verify if there are more than an author 
			2-1. Check if there is a comma (or others like &, et, and)
			2-2. Check if there are more than three tokens
			if only an author -> wrap the fields with <persName></persName>
		Step 3. if more than an author, check the type.
			3-1 separate tokens by comma (or others), if there are more than a token in a separated group,
				we assume that authors are separated by a comma
				wrap the fields with <persName></persName>
			3-2 if there is only a token in a separated group,
				SURNAME, FORENAME (FORENAME...), SURNAME, FORENAME (FORENAME...), 
				separate them by surname
		'''		
		preTag = ""
		continuousck = ["surname", "forename", "namelink", "genname"]
		group = []
		newsoup = BeautifulSoup(oriRef)
		tmp_group = []
		for ns in newsoup.find_all() :
			if ns.name in continuousck :
				tmp_group.append(ns.name)
			elif ns.name in includedLabels :
				if len(tmp_group) > 0 : group.append(tmp_group)
				tmp_group = []
				
		ptr2 = 0
		#tmpRef = oriRef
		for tmp_group in group :
			if len(tmp_group) > 1 :
				'add persName tag per tmp_group'
				ptr0 = oriRef.find("<"+tmp_group[0]+">", ptr2)
				oriRef = oriRef[:ptr0] + "<persName>" + oriRef[ptr0:]
				for tmp_tag in tmp_group :
					ptr1 = oriRef.find("<"+tmp_tag+">", ptr2)
					ptr2 = oriRef.find("</"+tmp_tag+">", ptr1)
				tmp_tag = tmp_group[len(tmp_group)-1]
				ptr2 = ptr2 + len("</"+tmp_tag+">")
				oriRef = oriRef[:ptr2] + "</persName>" + oriRef[ptr2:]
				
				'Check if there are more than an author in current tmp_group'
				if len(tmp_group) > 3 :
					tmp_soup = BeautifulSoup(oriRef[ptr0:ptr2])
					parsed_bs = ''.join(tmp_soup.findAll(text = True))
					#if oriRef.find(";", ptr0, ptr2) > 0 : #separated by ;
					if parsed_bs.find(";") > 0 : #separated by ; and search only in contents in case ; exists in tag
						ptr1 = oriRef.find(";", ptr0, ptr2)
						while ptr1 > 0 :
							[oriRef, ptr1, ptr2] = self._insertPersonTag(oriRef, ptr1, ptr2, ";")

					elif oriRef.find(",", ptr0, ptr2) > 0 : #include comma
						tmp_string = ''.join(BeautifulSoup(oriRef[ptr0:ptr2]).findAll(text = True))
						#print "Maybe Multiple person"
						multi = True #multiple person indicator
						if oriRef.count(",", ptr0, ptr2) == 1 : #one comma and exist a field with one token
							for ts in tmp_string.split(",") : 
								if len(ts.split()) == 1 : multi = False
						if multi :
							'Check separate tokens by comma'
							commaCut = True #indicator if we can simply separate by comma
							doubleCut = True #indicator if we can separate by two commas
							for ts in tmp_string.split(",") :  
								if len(ts.split()) == 1 : #check if all fields have two tokens at least
									commaCut = False
								else : #check if all fields have just one token
									doubleCut = False
							if commaCut : #separate by comma
								#print "Comma cut"
								ptr1 = oriRef.find(",", ptr0, ptr2)
								while ptr1 > 0 :
									[oriRef, ptr1, ptr2] = self._insertPersonTag(oriRef, ptr1, ptr2, ",")
							elif doubleCut : 
								#print "Double cut"
								ptr1 = oriRef.find(",", ptr0, ptr2)
								if ptr1 > 0 : ptr1 = oriRef.find(",", ptr1+1, ptr2)
								while ptr1 > 0 :
									[oriRef, ptr1, ptr2] = self._insertPersonTag(oriRef, ptr1, ptr2, ",")
									if ptr1 > 0 : ptr1 = oriRef.find(",", ptr1+1, ptr2)								
							else :
								#special case
								prePtr1 = ptr0
								tmp_fields = tmp_string.split(",")
								start = True #indicator is current token if start of a person
								ptr1 = oriRef.find(",", ptr0, ptr2)
								for tmp in tmp_fields :
									if len(tmp.split()) > 1 and ptr1 > 0 :
										if oriRef[prePtr1:ptr1].find("<surname>") > 0 and oriRef[prePtr1:ptr1].find("<forename>") > 0 :
											#ok, sufficient as a person
											prePtr1 = ptr1
											[oriRef, ptr1, ptr2] = self._insertPersonTag(oriRef, ptr1, ptr2, ",")
											start = True
										else : # is probable that surname or forename
											if start : 
												start = False
												prePtr1 = ptr1
												ptr1 = oriRef.find(",", ptr1+1, ptr2)
											else :
												prePtr1 = ptr1
												[oriRef, ptr1, ptr2] = self._insertPersonTag(oriRef, ptr1, ptr2, ",")
												start = True
									elif ptr1 > 0 :
										if start : 
											start = False
											prePtr1 = ptr1
											ptr1 = oriRef.find(",", ptr1+1, ptr2)	
										else :
											#print oriRef[ptr1:]
											prePtr1 = ptr1
											[oriRef, ptr1, ptr2] = self._insertPersonTag(oriRef, ptr1, ptr2, ",")
											start = True
							
			elif len(tmp_group) == 1 :
				ptr1 = oriRef.find("<"+tmp_group[0]+">", ptr2)
				ptr2 = oriRef.find("</"+tmp_group[0]+">", ptr1)
		
		return oriRef
	
	
	def _insertPersonTag(self, oriRef, ptr1, ptr2, sep):
		'ADD THE CASE OF INTERUPPED TAG'
		if oriRef.find(">", ptr1) > oriRef.find("<", ptr1) and oriRef.find("<", ptr1) >= 0 :
			oriRef = oriRef[:ptr1] + "</persName>" + oriRef[ptr1:]
			ptr1 = oriRef.find("<", ptr1+len("</persName>"+sep), ptr2)
			oriRef = oriRef[:ptr1] + "<persName>" + oriRef[ptr1:]
			ptr2 = ptr2 + len("<persName></persName>")
			ptr1 = oriRef.find(sep, ptr1, ptr2)
		else :
			ptr1 = oriRef.find(sep, ptr1+1, ptr2)
		
		return oriRef, ptr1, ptr2
	
		
	def _exchangeTags(self, oriRef, st1, ed1, st2, ed2):
		'''
		Exchange the position of two tags
			A		<B>		  C			<D>		E
		[:st1] [st1:ed1] [ed1:st2] [st2:ed2] [ed2:]
		->
			A		<D>		  C			<B>		E
		'''
		tmpRef = oriRef[:st1] + oriRef[st2:ed2] + oriRef[ed1:st2]
		tmpRef += oriRef[st1:ed1] + oriRef[ed2:]		
		
		return tmpRef
	
	
	def _moveFirstTag(self, oriRef, st1, ed1, st2, ed2):
		'''
		Exchange the position of two tags by moving the first tag
			A		<B>		  C			<D>		E
		[:st1] [st1:ed1] [ed1:st2] [st2:ed2] [ed2:]
		->
			A		C		<D>			<B>		E
		'''
		tmpRef = oriRef[:st1] + oriRef[ed1:st2] + oriRef[st2:ed2]
		tmpRef += oriRef[st1:ed1] + oriRef[ed2:]		
		
		return tmpRef
	
	
	def _moveSecondTag(self, oriRef, st1, ed1, st2, ed2):
		'''
		Exchange the position of two tags by moving the second tag
			A		<B>		  C			<D>		E
		[:st1] [st1:ed1] [ed1:st2] [st2:ed2] [ed2:]
		->
			A		<D>		 <B>		C		E
		'''
		tmpRef = oriRef[:st1] + oriRef[st2:ed2] + oriRef[st1:ed1]
		tmpRef +=  oriRef[ed1:st2] + oriRef[ed2:]		
		
		return tmpRef
	
	
	def _closestPreOpeningTag(self, oriRef, ptr1):
		'''
		Find the position of closest previous tag from a position
		'''
		startck1 = (oriRef[ptr1::-1]).find(">", 0)
		startck2 = (oriRef[ptr1::-1]).find("<", startck1)
		st = ptr1-startck2
		ed = ptr1-startck1+1		
		tagName = ((oriRef[st:ed].split('>')[0]).split()[0])[1:]

		return st, ed, tagName
		
	
	def _preOpeningTag(self, oriRef, ptr1, tagN):
		'''
		Find the position of previous tag called tagN from a position
		'''
		tagName = ''
		startck2 = 0
		startck1 = 0
		prePtrlimit
		
		while tagName != tagN or startck1 < 0:
			startck1 = (oriRef[ptr1::-1]).find(">", startck2)
			startck2 = (oriRef[ptr1::-1]).find("<", startck1)
			st = ptr1-startck2
			ed = ptr1-startck1+1		
			tagName = ((oriRef[st:ed].split('>')[0]).split()[0])[1:]
		if prePtrlimit > st :
			tagName = ''
			
		return st, ed, tagName
	
	
	def _correctMissTag(self, oriRef, basicTag, addedTag):
		'''
		Check interrupted tags in newly attached tag (wrapping other tags), then replace them
		This interruption arrives because of originally existing tags (basicTag) in the input file.
		By grouping fields per person, opening and ending tags can be conflicted.
		e.g. case 1 : <hi rend="bold"><persName><surname>Lallement</surname> <forename>E.</forename></hi></persName>
			 case 2 : ... <hi rend="bold"> <forename>M.</forename></persName> (<abbr>dir</abbr>.)</hi>
		By searching from the beginning of the input string, check case 1 and correct, then check case2 and correct
			[Algo]	1. find the starting and ending of target tag (pointers, ptr1, ptr2)
					2. 	(case 1) find an ending tag in basicTag from ptr1, if no starting tag between ptr1 and ptr2
						find the starting tag by inversely checking the string. Once 
					
		'''
		[limited1, limitst2] = self._totallyWrapped(oriRef)
		prePtrlimit = limited1
		postPtrlimit = limitst2
		
		tmpRef = oriRef
		ptr1 = tmpRef.find('<'+addedTag+'>', 0) #find the starting of new tag
		while ptr1 >= 0 :
			ptr2 = tmpRef.find('</'+addedTag+'>', ptr1)	
			#Starting tag, case 1	
			tagName = ''
			found = []
			st2 = tmpRef.find('</', ptr1, ptr2)
			ed2 = tmpRef.find('>', st2, ptr2)
			if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
			while st2 > 0 and tagName not in found : 
				while st2 > 0 and tagName not in basicTag :
					st2 = tmpRef.find('</', ed2, ptr2)
					ed2 = tmpRef.find('>', st2, ptr2)
					if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
				if st2 > 0 : 
					p1 = tmpRef.find('<'+tagName+' ', ptr1, st2)
					p2 = tmpRef.find('<'+tagName+'>', ptr1, st2)
					if p1 < 0 and p2 < 0 : 
						#no starting tag, so find starting tag
						[st1, ed1, tagN] = self._preOpeningTag(tmpRef, ptr1, tagName)
						if tagName == tagN :
							if len((tmpRef[ed1:ptr1+len('<'+addedTag+'>')]).split()) == 1 :
								tmpRef = self._moveSecondTag(tmpRef, st1, ed1, ptr1, ptr1+len('<'+addedTag+'>'))
								found.append(tagName)
							else :
								tmpstr = tmpRef[ptr2+len('</'+addedTag+'>'):st2]
								ignored = ["<nolabel>", "</nolabel>", "<abbr>", "</abbr>"]
								for st in ignored : tmpstr.replace(st,"")
								if tmpstr.find('<') < 0 :
									tmpRef = self._moveFirstTag(tmpRef, ptr1, ptr1+len('<'+addedTag+'>'), st2, ed2+1)
									found.append(tagName)
								else : 
									print "can't deal it"
									print tmpRef
					st2 = tmpRef.find('</', ed2, ptr2)
					ed2 = tmpRef.find('>', st2, ptr2)
					if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
					
			#Ending tag, case 2	
			tagName = ''
			found = []
			st2 = tmpRef.find('</', ptr2+1)
			ed2 = tmpRef.find('>', st2)
			if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
			while st2 > 0 and tagName not in found :
				while st2 > 0 and tagName not in basicTag :
					st2 = tmpRef.find('</', ed2)
					ed2 = tmpRef.find('>', st2)
					if st2 > 0 : tagName = tmpRef[st2+len('</'):ed2]
				if st2 > 0 : 
					p1 = tmpRef.find('<'+tagName+' ', ptr2, st2)
					p2 = tmpRef.find('<'+tagName+'>', ptr2, st2)
					if p1 < 0 and p2 < 0 : 
						#no starting tag, so find starting tag
						[st1, ed1, tagN] = self._preOpeningTag(tmpRef, ptr2, tagName)
						if tagName == tagN and st1 > ptr1 :
							tmpstr = tmpRef[ptr2+len('</'+addedTag+'>'):st2]
							ignored = ["<nolabel>", "</nolabel>", "<abbr>", "</abbr>"]
							for st in ignored : tmpstr.replace(st,"")
							if tmpstr.find('<') < 0 : 
								tmpRef = self._moveFirstTag(tmpRef, ptr2, ptr2+len('</'+addedTag+'>'), st2, ed2+1)
								found.append(tagName)
							else : # To avoid conflict just move the tag 
								tmpRef = self._moveSecondTag(tmpRef, st1, ed1, ptr2, ptr2+len('</'+addedTag+'>'))
								found.append(tagName)
					st2 = tmpRef.find('</', ed2)
					ed2 = tmpRef.find('>', st2)
					if st2 > 0 and st2 < postPtrlimit : tagName = tmpRef[st2+len('</'):ed2]
					
			ptr1 = tmpRef.find('<'+addedTag+'>', ptr2)
		
		return  tmpRef	
	
	
	def _totallyWrapped(self, oriRef):
		
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
	
	
	def _getName(self):
		'''
		Return the file name without the complete path
		'''
		chemin = self.nom.split("/")
		return chemin.pop()
	

	def convertToUnicode(self, chaine):
		'''
		Convert a string to unicode
		'''
		try:
			if isinstance(chaine, str):
				chaine = unicode(chaine, sys.stdin.encoding)
		except:
			chaine = unicode(chaine, 'ascii')
		return chaine

	