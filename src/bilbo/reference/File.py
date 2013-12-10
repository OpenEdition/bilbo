# -*- coding: utf-8 -*-
"""
Created on April 25, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from bs4 import BeautifulSoup, NavigableString
from bilbo.format.Clean import Clean
from bilbo.format.CleanCorpus1 import CleanCorpus1
from bilbo.format.CleanCorpus2 import CleanCorpus2
from bilbo.format.Rule import Rule
from bilbo.reference.ListReferences import ListReferences
from bilbo.output.identifier import extractDoi, loadTEIRule, toTEI, teiValidate
from bilbo.reference import tagtool
from xml.dom.minidom import parseString
import copy
import re, sys

specialPunc =  {'«':0, '»':0, '“':0, '”':0, '"':0, '–':0, '-':0}
prePtrlimit = -1
postPtrlimit = -1

class File(object):
	"""
	A file class containing all references in a file
	"""

	def __init__(self, fname, options):
		"""
		Attributes
		----------
		nom : string
			target file name
		corpus : dictionary of reference list
			 references in the file
		"""
		self.nom = fname
		self.corpus = {}
		self.options = options
	

	def extract(self, typeCorpus, tag, external):
		"""
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
		"""	
		clean = Clean()
		if typeCorpus == 1:
			clean = CleanCorpus1(self.options)
		elif typeCorpus == 2:
			clean = CleanCorpus2(self.options)
		#print self.nom
		references = clean.processing(self.nom, tag, external)
		if len(references) >= 1:
			self.corpus[typeCorpus] = ListReferences(references, typeCorpus)
			rule = Rule(self.options)
			rule.reorganizing(self.corpus[typeCorpus])


	def getListReferences(self, typeCorpus):
		"""
		Return reference list
		
		Parameters
		----------
		typeCorpus : int, {1, 2, 3}
			type of corpus
			1 : corpus 1, 2 : corpus 2...
		"""
		try:
			return self.corpus[typeCorpus]
		except :
			return -1
		

	def nbReference(self, typeCorpus):
		"""
		count the number of references
		"""
		try:
			return self.corpus[typeCorpus].nbReference()
			
		except :
			return 0	
	
		
	def buildReferences(self, references, tagTypeCorpus, dirResult):
		"""
		Construct final xml output file, called from Corpus::addTagReferences
		Unlike the first version, compare token by token, replace the token by automatically tagged token. 
		That's why we keep perfectly the original data format.
		Don't forget to put the '&amp;' instead of '&'
		
		Parameters
		----------
		references : list 
			automatically annotated references in the given file
		tagTypeCorpus : string, {"bibl", "note"}
			tag name defining reference types
			"bibl" : corpus 1, "note" : corpus 2
		tagTypeList : string, "listbibl"
			tag name wrapping all references
		
		Attributes
		----------
		
		"""
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
				oriRef = self._cleanTags(oriRef)
				
				if self.options.o == 'simple' :
					parsed_soup = parsed_soup.encode('utf8')
					parsed_soup = parsed_soup.replace('&', "&amp;")
					parsed_soup = parsed_soup.replace('<pb/>', '')
					parsed_soup = parsed_soup.replace('<', "&lt;")
					parsed_soup = parsed_soup.replace('>', "&gt;")
					oriRef = '<'+tagTypeCorpus+'>'+parsed_soup+'</'+tagTypeCorpus+'>'
				for r in ref.contents :
					ck = 0
					try : r.name
					except : ck = 1
					if ck == 0 and not r.name == "c" and r.string : #and not r.name == "nonbibl" :
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
							if (ptr >= 0) and token[:2] != '</' :
								nstr = "<"+r.name+">"+token+"</"+r.name+">"
								oriRef = oriRef[:ptr] + nstr + oriRef[ptr+len(token):]
								ptr += len(nstr)
							else :
								ptr = pre_ptr
				#'''
				'check continuously annotated tags to eliminate tags per each token'
				oriRef = self.continuousTags(basicTag, includedLabels, oriRef)
				'arrange existing tags and automatically annotated tag'
				oriRef = self.arrangeTagsPerToken(includedLabels, oriRef, tagTypeCorpus)
				'hi tag checking'
				oriRef = self.checkHiTag(oriRef, includedLabels)
				beforeRef = oriRef
				
				'WHEN DIRTY DATA CONTATING SPECIAL HTML TAGS'
				oriRef = oriRef.replace('&ndash;', '&#8211;')
				oriRef = oriRef.replace('&nbsp;', '&#160;')
				oriRef = oriRef.replace('&mdash;', '-')
				
				
				if oriRef.find("<author>") < 0 : #non-annotated input
					'add author tags'
					oriRef, noCutRef= self.findAuthor(includedLabels, oriRef)
					'correct missed tag inserting'
					oriRef = self.correctMissTag(oriRef, basicTag, "author")
					'''
					try : parseString(oriRef)
					except Exception, err:
						noCutRef = self.correctMissTag(noCutRef, basicTag, "author")
						oriRef = noCutRef
						try : parseString(oriRef)
						except Exception, err:
							print self.nom
							sys.stderr.write('ERROR: %s\n' % str(err))
							m = re.search('(?<=column )\w+', str(err))
							print "Abandon person separation"
							oriRef = beforeRef
					'''
					
					'bibl separation'
					if tagTypeCorpus == 'note' : 
						oriRef = self.detectBibl(oriRef, includedLabels)
					
						try : parseString(oriRef)
						except Exception, err:
							print err, self.nom, oriRef
							pass
					
				#'''
				if self.options.o == 'tei' :
					oriRef = toTEI(oriRef, tagConvert)
				ref_ori.append(oriRef)
			cptRef += 1
		
		try:
			if self.options.o == 'simple' : tmp_str = self.writeResultOnly(ref_ori, references, tagTypeCorpus)
			else : tmp_str = self.writeResultInOriginal(tmp_str, soup, ref_ori, references, tagTypeCorpus)	
		except :
			pass

		fich = open(dirResult+self._getName(), "w")
		fich.write(tmp_str)
		fich.close()
		
		'xml schema validation'
		self.schemaValidation(len(references), dirResult)
		
		return


	def schemaValidation(self, numReferences, dirResult):
		"""
		xml schema validation for output file
		"""
		if self.options.v in ['output', 'all'] :
			if self.options.o == 'tei' and numReferences > 0 :
				try : 
					valide, numErr = teiValidate(dirResult+self._getName(), 'output')
					if not valide :
						valide, numErrOri = teiValidate(self.nom, 'output')
						if numErr == numErrOri : print "Original file also has", numErr, "errors. Annotation OK."
						else : print "Original file has", numErrOri, "errors. Annotation NOT OK."
				except Exception, err: print err #when original file has a fundamental error
		return
	

	def writeResultInOriginal(self, tmp_str, soup, ref_ori, references, tagTypeCorpus):
		"""
		Write the labeling result in the original file. All the existing tags in the original file are kept.
		"""
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
				text = str(ref_ori[cpt])
				text = self.doiExtraction(text, str(references[cpt]), tagTypeCorpus)
				tmp_list = list(tmp_str)
				tmp_list[p1:p2+len('</'+tagTypeCorpus+'>')] = text
				tmp_str = ''.join(tmp_list)

			cpt += 1 
			pre_p1 = p1		
		
		return tmp_str


	def writeResultOnly(self, ref_ori, references, tagTypeCorpus) :
		"""
		Write simply the labeling result without article contents. The existing tags are already eliminated for this simple writing
		"""
		tmp_str = '<list'+tagTypeCorpus.title()+'>\n'
		for i, r in enumerate(ref_ori) :
			text = str(ref_ori[i])
			text = self.doiExtraction(text, references[i], tagTypeCorpus)
			tmp_str += text+'\n'
		tmp_str += '</list'+tagTypeCorpus.title()+'>\n'
		return tmp_str


	def doiExtraction(self, text, reference, tagTypeCorpus):
		"""
		Call extractDoi from indentifier.py then insert the result
		"""
		doistring = ''
		if self.options.d :
			doistring = extractDoi(str(reference), tagTypeCorpus)
			if doistring != '' : 
				doistring = 'http://dx.doi.org/'+str(doistring)
				doistring = '<idno type=\"DOI\">'+doistring+'</idno>'
				ptr1 = text.find('</title>')+len('</title>')
				text = text[:ptr1] + doistring + text[ptr1:]
		return text
		
			
	def continuousTags(self, basicTag, includedLabels, oriRef):
		"""
		Check continuously annotated tags to eliminate tags per each token
		"""
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
		"""
		Check if a field of tokens annotated by a label tag has wrapped by other basic tag.
		If yes, change order. It's for prevent the mismatching error of author tag and 
			also find other continuous tags.
		e.g. To prevent the following error (interruption of <author> in <hi>)
			<hi font-variant="small-caps"><author><surname>Alves</surname></hi>
			change order as following before add <author>
			<surname><hi font-variant="small-caps">Alves</hi></surname>
		e.g. To find undetected continuous tags as follows
			
		"""
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
					if closeTag not in ["note", "bibl", "listNote", "listBibl", "ref", "p"] and closeTag not in includedLabels :
						[st1, ed1, dummyTag] = tagtool._closestPreTag(oriRef, ptr1)
						if oriRef[st1:ed1].find('<'+closeTag) == 0 and self._onlyPunc(oriRef[ed1:ptr1]) :#if there is no tag between them and NO char
							#then exchange tags
							tmpRef = tagtool._moveSecondTag(oriRef, st1, ed1, ptr1, ptr1+len('<'+tmpTag+'>'))
							tmpRef = tagtool._moveFirstTag(tmpRef, ptr2-len('</'+tmpTag+'>'), ptr2, ptr3, ptr4+1)
							oriRef = tmpRef
				ptr1 = oriRef.find('<'+tmpTag+'>', ptr2)
		
		'final continuous check'		
		oriRef = self._continuousTagck(includedLabels, nameck, oriRef)
		'delete tags in <ref>'
		st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'ref', 0)
		while(st1 >= 0) :
			centre = oriRef[ed1:st2]
			if centre.find("<") >= 0 and centre.find(">") > 0 :
				ns = BeautifulSoup(centre)
				found = []
				for n in ns.find_all() : 
					if n.name in includedLabels : found.append(n.name)
				for f in found : 
					oriRef = tagtool._deleteTag(oriRef, f, ed1)
					ed2 -= 2*len(f)+len('<></>')
			st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'ref', ed2)

		return oriRef
	
	
	def _continuousTagck(self, includedLabels, nameck, oriRef):
		"""
		After a tag arrangement, check again if there are continuous tags. If yes, delete them.
		"""
		tmp_str = oriRef
		for tmpTag in includedLabels :
			if tmpTag not in nameck :
				st1 = tmp_str.find('</'+tmpTag+'>', 0)
				while st1 >= 0:
					ed1 = tmp_str.find('>', st1) + 1
					st2 = tmp_str.find('<'+tmpTag+'>', st1)
					ed2 = tmp_str.find('>', st2) + 1
					if st2>=0 and self._onlyPunc(tmp_str[ed1:st2]) :
						tmp_str = tmp_str[:st1]+tmp_str[ed1:st2]+tmp_str[ed2:]
					st1 = tmp_str.find('</'+tmpTag+'>', st1+1)

		return tmp_str
	
	
	def _onlyPunc(self, tmp_str):
		"""
		Check if tmp_str has non-alphanumeric character only. Find also special characters in dict specialPunc.
		"""
		new_str = tmp_str.replace(' ', ' ')
		for key in specialPunc.iterkeys(): new_str = new_str.replace(key, ' ')
		new_str = re.sub('\W', ' ', new_str)
		onlyPunc = False
		if len(new_str.split()) == 0 : onlyPunc = True
					
		return onlyPunc
	
	
	def checkHiTag(self, oriRef, includedLabels):
		"""
		Solve tag encoding problem concerning <hi> tag. As original xml contains a lot of <hi> tags, which are often
		complicate and sometimes not correctly written, we should especially deal with the conflict among <hi> tag
		and annotated tags by Bilbo. The objective is exchanging tags so that <hi> tag includes text only. It is not 
		easy because users sometimes do errors when they modify character appearance in their articles (<hi> concerns
		character appearance). Even if this is not very often, it's not easy to add some rules to detect and solve
		this problem because Bilbo also mistakes and it is not easy to automatically detect if the conflict comes 
		from user or Bilbo. Anyway we start the correction from the obvious error of Bilbo and try to make some 
		detailed rules for every error cases.
		"""
		
		refLabels = []
		hasTitle = False
		soup = BeautifulSoup(oriRef)
		for s in soup.find_all() : 
			if s.name in includedLabels : 
				refLabels.append(s.name)
				if (s.name).find("title") == 0 : hasTitle = True
				
		nameck = ["surname", "forename", "namelink", "genname"]
		canDelete = ["abbr", "w", "bookindicator", "nolabel", "nonbibl"]
		
		target_tag_st = "<hi"	#a
		target_tag_mi = ">"		#b
		target_tag_end = "</hi>"#c d
		tmpRef = oriRef
		a = tmpRef.find(target_tag_st,0)
		while a > 0 and tmpRef[a:].find('<hi rend="Endnote">') != 0 :
			b = tmpRef.find(target_tag_mi, a + len(target_tag_st))
			c = tmpRef.find(target_tag_end, b)
			d = c + len(target_tag_end)
			
			centre = tmpRef[b+1:c]
			cntHi = centre.count("<hi") # check if <hi> includes other <hi> tags
			if cntHi > 0 :
				for i in range(cntHi) :
					c = tmpRef.find(target_tag_end, d)
					d = c + len(target_tag_end)
					
			centre = tmpRef[b+1:c]
			if centre.find("<") < 0 and centre.find(">") < 0 :
				a = tmpRef.find(target_tag_st,d)
			else :
				'Find other tags and move them'
				ns = BeautifulSoup(centre)
				found = []
				for n in ns.find_all() : 
					if n.name in includedLabels : found.append(n.name)
				'If there is only one type of tag but the tags have not been joined because they are name tags'
				'-> group them, cause they are part of an author wrapped by <hi>'
				if len(found)  > 1 and len(list(set(found))) == 1 : #unattached <surname> or <forename> in <hi>
					new_str = self._continuousTagck(includedLabels, [], tmpRef[a:d])
					tmpRef = tmpRef[:a]+new_str+tmpRef[d:]
					found = [found[0]]
					c = tmpRef.find(target_tag_end, b)
					d = c + len(target_tag_end)
						
				if len(found) == 1 :
					tagName = found[0]
					'case 1 : if there is only one tag and it is title, move them'
					if tagName.find("title") == 0 :
						tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
					else :
						st1, ed1, st2, ed2 = tagtool._findTagPosition(tmpRef, tagName, a)
						'case 2 : if there is only one tag and no characters between pairs'
						if self._onlyPunc(tmpRef[b+1:st1]) and self._onlyPunc(tmpRef[ed2:c]) :
							tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
						else :
							'case 2-1 : just one another token, accept that token as same tag'
							tmp_centre = tagtool._deleteTag(centre, tagName, 0)
							if len(tmp_centre.split()) == 2 :
								tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
							else :
								'case 2-2 : if not, delete all'
								for f in found : 
									tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
									d -= 2*len(f)+len('<></>')
				else :
					cntT = 0
					cntN = 0
					tagName = ''
					for f in found : #Check if there is just one type of title
						if f.find("title") == 0 : 
							tagName = f
							cntT += 1
						if f in nameck+['nolabel', 'abbr'] : cntN += 1
					'case 3 : if there are more than one tag but only one title, move title and delete the other tags'
					if cntT == 1 :
						tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
						'delete the other tags'
						for f in found :
							if f != tagName :
								tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
								d -= 2*len(f)+len('<></>')
					elif cntT > 1 :
						if cntT == len(found) :
							'case 4 : if all tags are title tags, but different, take the first title tag for all'
							tmpRef = tagtool._exchangeTagPairs(tmpRef, found[0], a, b+1, c, d)
							for f in found[1:] :
								tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
								d -= 2*len(f)+len('<></>')
						else :
							'case 4-1 : mix of different titles and other tags, take the last title tag for all'
							tmpRef = tagtool._exchangeTagPairs(tmpRef, tagName, a, b+1, c, d)
							for f in found :
								tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
								d -= 2*len(f)+len('<></>')					
					elif len(found) > 0 and cntN == len(found) : #all name tag or (nolabel)
						'case 5 : if all tags are name tags and there are other words, maybe annotation error, delete'
						tmp_centre = centre
						for f in found : tmp_centre = tagtool._deleteTag(tmp_centre, f, 0)
						if len(tmp_centre.split()) > len(found) :
							'delete all'
							for f in found : 
								tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
								d -= 2*len(f)+len('<></>')
						else : ####FULLY ANNOTATED NAME TAGS####
							'case 5-1 : if <hi font-variant="small-caps"> or <hi rend="bold"> : person name, CUT'
							hiString = tmpRef[a:b+1]
							if hiString == '<hi font-variant="small-caps">' or hiString == '<hi rend="bold">' :
								tmpRef = tagtool._devideHi(tmpRef, found, hiString, a)
								'Then re-test the <hi>'
								d = a
							elif not hasTitle :
								'case 5-2 : if there is no title in oriRef, delete all tags and wrap with title_m'
								tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
							else :
								'case 5-3 : there is title in oriRef, then check it can be really name <-HOW'
								isName = tagtool._isName(tmpRef, centre, found, includedLabels, a)
								if isName : # Name, CUT it
									hiString = tmpRef[a:b+1]
									tmpRef = tagtool._devideHi(tmpRef, found, hiString, a)
									d = a
								else :		#<---------------------------TO BE MODIFIED for TITLE TYPE
									'case 5-4'
									tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
					else :
						if len(found) == 0 : pass #NO problem
						else : #### tags are mixed, but no title
							allDelete = True
							for f in found : 
								if f not in canDelete : allDelete = False
							'case 6 : if all tags are removable ones, delete ALL'
							if allDelete :
								for f in found : 
									tmpRef = tagtool._deleteTag(tmpRef, f, b+1)
									d -= 2*len(f)+len('<></>')
							else :
								'case 7 : fully mixed, but most of case is removable. consider some special sub cases.'
								isPublisher = False
								if found == ['place','publisher','abbr'] : isPublisher = True
								if not hasTitle or not tagtool._hasTitleAfterSemi(tmpRef, a, d) : 
									'case 7-1: if there is no title in oriRef, delete all tags and wrap with title_m'
									tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
								elif isPublisher :	
									'case 7-2: <place>, <publisher>, <abbr> <---- keep them'
									hiString = tmpRef[a:b+1]
									tmpRef = tagtool._devideHi(tmpRef, found, hiString, a)
									'Then re-test the <hi>'
									d = a
								else : #<---------------TO BE MODIFIED for more detailed check
									'case 7-3: other cases. for the moment, treat as sub case 1'
									tmpRef, d = tagtool._delAllandWrap(tmpRef, found, 'title_m', a, d)
									
			a = tmpRef.find(target_tag_st,d)
		
		tmpRef = self._continuousTagck(includedLabels, nameck, tmpRef)
			
		return tmpRef
	
	
	def findAuthor(self, includedLabels, oriRef):
		"""
		Post-processing RULE about author field
		Separate surname and forename pair per author
		Step 1. check group of fields continuously tagged as surname or as forename over whole string
		Step 2. per group, verify if there are more than an author 
			2-1. Check if there is a comma (or others like &, et, and)
			2-2. Check if there are more than three tokens
			if only an author -> wrap the fields with <author></author>
		Step 3. if more than an author, check the type.
			3-1 separate tokens by comma (or others), if there are more than a token in a separated group,
				we assume that authors are separated by a comma
				wrap the fields with <author></author>
			3-2 if there is only a token in a separated group,
				SURNAME, FORENAME (FORENAME...), SURNAME, FORENAME (FORENAME...), 
				separate them by surname
		"""		
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
		noCutRef = ''
		for tmp_group in group :
			if len(tmp_group) >= 1 : #even if there is ONE name field, wrap with <author>
				'add author tag per tmp_group'
				ptr0 = oriRef.find("<"+tmp_group[0]+">", ptr2)
				oriRef = oriRef[:ptr0] + "<author>" + oriRef[ptr0:]
				for tmp_tag in tmp_group :
					ptr1 = oriRef.find("<"+tmp_tag+">", ptr2)
					ptr2 = oriRef.find("</"+tmp_tag+">", ptr1)
				tmp_tag = tmp_group[len(tmp_group)-1]
				ptr2 = ptr2 + len("</"+tmp_tag+">")
				oriRef = oriRef[:ptr2] + "</author>" + oriRef[ptr2:]

				noCutRef = oriRef
				
				'Check if there are more than an author in current tmp_group'
				if len(tmp_group) > 3 :
					tmp_soup = BeautifulSoup(oriRef[ptr0:ptr2])
					parsed_bs = ''.join(tmp_soup.findAll(text = True))
					if parsed_bs.find(";") > 0 : #separated by ; and search only in contents in case ; exists in tag
						ptr1 = oriRef.find(";", ptr0, ptr2)
						while ptr1 > 0 : [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ";")
					elif oriRef.find(",", ptr0, ptr2) > 0 : #include comma
						tmp_string = ''.join(BeautifulSoup(oriRef[ptr0:ptr2]).findAll(text = True))
						multi = True #multiple person indicator
						if oriRef.count(",", ptr0, ptr2) == 1 : #one comma and exist a field with one token
							for ts in tmp_string.split(",") : 
								if len(ts.split()) == 1 : multi = False
						if multi :
							'Check separate tokens by comma'
							commaCut = True #indicator if we can simply separate by comma
							doubleCut = True #indicator if we can separate by two commas
							for ts in tmp_string.split(",") :  
								if len(ts.split()) == 1 : commaCut = False #check if all fields have two tokens at least
								else : doubleCut = False #check if all fields have just one token
							if commaCut : #separate by comma
								ptr1 = oriRef.find(",", ptr0, ptr2)
								while ptr1 > 0 : [oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
							elif doubleCut : 
								ptr1 = oriRef.find(",", ptr0, ptr2)
								if ptr1 > 0 : ptr1 = oriRef.find(",", ptr1+1, ptr2)
								while ptr1 > 0 :
									[oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
									if ptr1 > 0 : ptr1 = oriRef.find(",", ptr1+1, ptr2)								
							else : #special case
								prePtr1 = ptr0
								tmp_fields = tmp_string.split(",")
								start = True #the token is start of a person
								ptr1 = oriRef.find(",", ptr0, ptr2)
								for tmp in tmp_fields :
									if len(tmp.split()) > 1 and ptr1 > 0 :
										if oriRef[prePtr1:ptr1].find("<surname>") > 0 and oriRef[prePtr1:ptr1].find("<forename>") > 0 :
											#ok, sufficient as a person
											prePtr1 = ptr1
											[oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
											start = True
										else : # is probable that surname or forename
											if start : 
												start = False
												prePtr1 = ptr1
												ptr1 = oriRef.find(",", ptr1+1, ptr2)
											else :
												prePtr1 = ptr1
												[oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
												start = True
									elif ptr1 > 0 :
										if start : 
											start = False
											prePtr1 = ptr1
											ptr1 = oriRef.find(",", ptr1+1, ptr2)	
										else :
											prePtr1 = ptr1
											[oriRef, ptr1, ptr2] = self._inserAuthorTag(oriRef, ptr1, ptr2, ",")
											start = True
			elif len(tmp_group) == 1 : #it works when the previous if statement is more than 1 ( >1 )
				ptr1 = oriRef.find("<"+tmp_group[0]+">", ptr2)
				ptr2 = oriRef.find("</"+tmp_group[0]+">", ptr1)
				
		'final check, delete useless <author> not containing surname or forename caused by <nonbibl>'
		st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'author', 0)
		while(st1 >= 0) :
			if oriRef[st1:ed2].find('surname') < 0 and oriRef[st1:ed2].find('forename') < 0 :
				oriRef = tagtool._deleteTag(oriRef, 'author', st1)
			st1, ed1, st2, ed2  = tagtool._findTagPosition(oriRef, 'author', st1+1)
		'wrap <orgname> by <author>'
		oriRef = oriRef.replace('<orgname>', '<author><orgname>')
		oriRef = oriRef.replace('</orgname>', '</orgname></author>')
			
		return oriRef, noCutRef
	
	
	def _inserAuthorTag(self, oriRef, ptr1, ptr2, sep):
		"""
		Insert <author> tag at the given positions
		"""
		'check if there are contents between ptr1 and ptr2'
		valid = False
		if oriRef[ptr1:ptr2].find('<surname>') >= 0 or oriRef[ptr1:ptr2].find('<forename>') >= 0 :
			valid = True
		'check if ptr1 is not in the middle of hi tag'
		st, ed, tagName = tagtool._closestPreTag(oriRef, ptr1)
		if tagName == 'hi' :
			p = oriRef.find('<', ptr1)
			if oriRef[p:p+5] == '</hi>' : valid = False
			
		'ADD THE CASE OF INTERUPPED TAG'
		if valid and oriRef.find(">", ptr1) > oriRef.find("<", ptr1) and oriRef.find("<", ptr1) >= 0 :
			oriRef = oriRef[:ptr1] + "</author>" + oriRef[ptr1:]
			ptr1 = oriRef.find("<", ptr1+len("</author>"+sep), ptr2)
			oriRef = oriRef[:ptr1] + "<author>" + oriRef[ptr1:]
			ptr2 = ptr2 + len("<author></author>")
			ptr1 = oriRef.find(sep, ptr1, ptr2)
		else :
			ptr1 = oriRef.find(sep, ptr1+1, ptr2)
		
		return oriRef, ptr1, ptr2
	
		
	def correctMissTag(self, oriRef, basicTag, addedTag):
		"""
		Check interrupted tags in newly attached tag (wrapping other tags), then replace them
		This interruption arrives because of originally existing tags (basicTag) in the input file.
		By grouping fields per person, opening and ending tags can be conflicted.
		e.g. case 1 : <hi rend="bold"><author><surname>Lallement</surname> <forename>E.</forename></hi></author>
			 case 2 : ... <hi rend="bold"> <forename>M.</forename></author> (<abbr>dir</abbr>.)</hi>
		By searching from the beginning of the input string, check case 1 and correct, then check case2 and correct
			[Algo]	1. find the starting and ending of target tag (pointers, ptr1, ptr2)
					2. 	(case 1) find an ending tag in basicTag from ptr1, if no starting tag between ptr1 and ptr2
						find the starting tag by inversely checking the string. Once 		
		"""
		[limited1, limitst2] = tagtool._totallyWrapped(oriRef)
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
						[st1, ed1, tagN] = tagtool._preOpeningTag(tmpRef, ptr1, tagName, prePtrlimit)
						if tagName == tagN :
							if len((tmpRef[ed1:ptr1+len('<'+addedTag+'>')]).split()) == 1 :
								tmpRef = tagtool._moveSecondTag(tmpRef, st1, ed1, ptr1, ptr1+len('<'+addedTag+'>'))
								found.append(tagName)
							else :
								tmpstr = tmpRef[ptr2+len('</'+addedTag+'>'):st2]
								ignored = ["<nolabel>", "</nolabel>", "<abbr>", "</abbr>"]
								for st in ignored : tmpstr.replace(st,"")
								if tmpstr.find('<') < 0 :
									tmpRef = tagtool._moveFirstTag(tmpRef, ptr1, ptr1+len('<'+addedTag+'>'), st2, ed2+1)
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
						[st1, ed1, tagN] = tagtool._preOpeningTag(tmpRef, ptr2, tagName, prePtrlimit)
						if tagName == tagN and st1 > ptr1 :
							tmpstr = tmpRef[ptr2+len('</'+addedTag+'>'):st2]
							ignored = ["<nolabel>", "</nolabel>", "<abbr>", "</abbr>"]
							for st in ignored : tmpstr.replace(st,"")
							if tmpstr.find('<') < 0 : 
								tmpRef = tagtool._moveFirstTag(tmpRef, ptr2, ptr2+len('</'+addedTag+'>'), st2, ed2+1)
								found.append(tagName)
							else : # To avoid conflict just move the tag 
								tmpRef = tagtool._moveSecondTag(tmpRef, st1, ed1, ptr2, ptr2+len('</'+addedTag+'>'))
								found.append(tagName)
					st2 = tmpRef.find('</', ed2)
					ed2 = tmpRef.find('>', st2)
					if st2 > 0 and st2 < postPtrlimit : tagName = tmpRef[st2+len('</'):ed2]		
			ptr1 = tmpRef.find('<'+addedTag+'>', ptr2)
		
		return  tmpRef	
	
	
	def _cleanTags(self, oriRef):
		"""
		Clean unnecessary <hi> tag
		"""
		target_tag_st = "<hi xml:lang=\""	#a
		target_tag_mi = ">"		#b
		target_tag_end = "</hi>"#c d
		tmpRef = oriRef
		a = tmpRef.find(target_tag_st,0)
		while a > 0 :
			b = tmpRef.find(target_tag_mi, a + len(target_tag_st))
			c = tmpRef.find(target_tag_end, b)
			d = c + len(target_tag_end)
			if re.match('<hi xml:lang=\"\w\w\">', tmpRef[a:b+1]) :
				tmpRef = tmpRef[:a]+tmpRef[b+1:c]+tmpRef[d:]
				e = d-len('<hi xml:lang=\"AA\"></hi>')
				if e > 0 : a = tmpRef.find(target_tag_st, e)
				else : a = tmpRef.find(target_tag_st, 0)
			else :	
				a = tmpRef.find(target_tag_st,d)
		tmpRef = self._cleanHiTagSpecific(tmpRef)
	
		return tmpRef


	def _cleanHiTagSpecific(self, tmpRef):	
		"""
		Clean unnecessary <hi> tag with an exact matching
		"""
		hiStrings = ['<hi rend="subtitle1">', '<hi rend="st">', '<hi rend="apple-style-span">']
		target_tag_end = "</hi>"#c d
		for hiString in hiStrings :
			a = tmpRef.find(hiString,0)
			while a > 0 :
				b = a + len(hiString)
				c = tmpRef.find(target_tag_end, b)
				d = c + len(target_tag_end)
				centre = tmpRef[b+1:c]
				cntHi = centre.count("<hi") # check if <hi> includes other <hi> tags
				if cntHi > 0 :
					for i in range(cntHi) :
						c = tmpRef.find(target_tag_end, d)
						d = c + len(target_tag_end)
				tmpRef = tmpRef[:a]+tmpRef[b:c]+tmpRef[d:]
				e = d-len(hiString)-len(target_tag_end)	
				a = tmpRef.find(hiString, e)
				
		return tmpRef
	
	
	def detectBibl(self, oriRef, includedLabels):
		"""
		Separate references included in a note
		"""
		'find tags'
		refLabels = []
		soup = BeautifulSoup(oriRef)
		tempLabels = includedLabels
		tempLabels['author'] = 1
		toAdd = ['title_m', 'title_a', 'title_j', 'title_t', 'title_u', 'title_s']
		for k in toAdd : tempLabels[k] = 1
		if tempLabels.has_key('nonbibl') : del tempLabels['nonbibl']
		for s in soup.find_all() : 
			if s.name in tempLabels : refLabels.append(s.name)
		
		'find position and insert <bibl> and </bibl>'
		if refLabels != [] :
			ptr2 = -1
			tagName = refLabels[0]
			ptr1 = oriRef.find("<"+tagName+">", 0)
			oriRef = oriRef[:ptr1] + "<bibl>" + oriRef[ptr1:]
			if tagName == 'author' : ptr2 = oriRef.find("</author>", ptr1)
			for tagName in refLabels[1:] :
				ptr1 = oriRef.find("<"+tagName+">", ptr1+1)
				if tagName == 'author' : ptr2 = oriRef.find("</author>", ptr1)
			ptr1 = oriRef.find("</"+tagName+">", ptr1)
			ptr1 = ptr1+len("</"+tagName+">")
			if ptr2 >= ptr1 : ptr1 = ptr2 +len("</author>")
			oriRef = oriRef[:ptr1] + "</bibl>" + oriRef[ptr1:]
	
		oriRef, case1 = self._separateSemicolonBibl(oriRef, includedLabels)
		if not case1 : oriRef = self._separateNonbiblBibl(oriRef, includedLabels)

		return oriRef
	
	
	def _separateSemicolonBibl(self, oriRef, includedLabels):
		"""
		Separate multiple references in a detected reference zone using semicolons
		"""
		validLabels = includedLabels
		toRemove = ['nolabel', 'nonbibl', 'w', 'bookindicator']
		toAdd = ['title_m', 'title_a', 'title_j', 'title_t', 'title_u', 'title_s']
		for k in toRemove : 
			if k in validLabels : del validLabels[k]
		for k in toAdd : validLabels[k] = 1
		separateLabels = copy.deepcopy(validLabels)
		nameck = ['surname', 'forename', 'namelink', 'genname', 'author']
		for k in nameck : 
			if k in separateLabels : del separateLabels[k]
		
		'case 1 : find semicolons and verify if they are used for the reference separation'
		case1 = False
		tmp_soup = BeautifulSoup(oriRef)
		sub_soup = tmp_soup.find('bibl')
		parsed_bs = ''
		if sub_soup : parsed_bs = ''.join(sub_soup.findAll(text = True))
		if parsed_bs.find(';') > 0 :
			ptr0 = oriRef.find('<bibl>') +len('<bibl>')
			ptr2 = oriRef.find('</bibl>')
			'find semiconlon'
			ptr1 = oriRef.find(";", ptr0, ptr2)
			ckend = oriRef.find("<", ptr1, ptr2)
			while ptr1 > 0 : 
				centre = BeautifulSoup(oriRef[ptr0:ptr1])
				if not oriRef[ckend:].find('</') == 0 :
					sepBibl = False
					for cen in centre.find_all() :
						if cen.name in separateLabels : sepBibl = True
					if sepBibl :
						st, ed, preTagName = tagtool._closestPreTag(oriRef, ptr1)
						if preTagName[1:] in validLabels : #check if previous tag name is in valid label list
							tmpRef = oriRef[:ed] + '</bibl>' + oriRef[ed:]
							st = tmpRef.find('<', ed+len('</bibl>'))
							ed = tmpRef.find('>', st)
							postTagName = tmpRef[st+1:ed]
							'check if post tag name is in valid label list. if not search again'
							while postTagName not in validLabels and st > 0 :
								st = tmpRef.find('<', ed)
								ed = tmpRef.find('>', st)
								postTagName = tmpRef[st+1:ed]
							if postTagName in validLabels :
								'And if it has sufficient tags in current bloc. if only names, stop'
								tmpPtr = tmpRef.find(";", ed, ptr2) # find next ;
								if tmpPtr < 0 : tmpPtr = ptr2
								tmpCentre = BeautifulSoup(tmpRef[st:tmpPtr])
								sepBibl = False
								for tcen in tmpCentre.find_all() :
									if tcen.name in separateLabels : sepBibl = True
								if sepBibl :
									tmpRef = tmpRef[:st] + '<bibl>' + tmpRef[st:]
									ptr1 = st
									oriRef = tmpRef
									case1 = True								
				ptr0 = ptr1+1	
				ptr1 = oriRef.find(";", ptr1+1, ptr2)
				
		return oriRef, case1
	
	
	def _separateNonbiblBibl(self, oriRef, includedLabels):
		"""
		separate multiple references in a detected reference zone using <nonbibl> fields
		"""
		validLabels = includedLabels
		toRemove = ['nolabel', 'nonbibl', 'w', 'bookindicator']
		for k in toRemove : 
			if k in validLabels : del validLabels[k]
		separateLabels = copy.deepcopy(validLabels)
		nameck = ['surname', 'forename', 'namelink', 'genname', 'author']
		for k in nameck : 
			if k in separateLabels : del separateLabels[k]
		
		'case 2'
		case2 = False
		tmp_soup = BeautifulSoup(oriRef)
		sub_soup = tmp_soup.find('bibl')
		if sub_soup : 
			for ss in sub_soup.findAll() :
				if ss.name == 'nonbibl' : case2 = True
			if case2 :
				case2 = False
				st1, limit1, limit2, ed2 = tagtool._findTagPosition(oriRef, 'bibl', 0)
				st1, ed1, st2, ed2 = tagtool._findTagPosition(oriRef, 'nonbibl', limit1)
				while st1 > 0 :
					'check if previous zone is sufficient for a reference if not stop'
					preSoup = BeautifulSoup(oriRef[limit1:st1])
					sepBibl = False
					c = 0
					for ps in preSoup.find_all() :
						if ps.name in separateLabels : c+=1
					if c > 1 : sepBibl = True
					if sepBibl :
						st, ed, preTagName = tagtool._closestPreTag(oriRef, st1)
						if preTagName[1:] in validLabels :
							tmpRef = oriRef[:ed] + '</bibl>' + oriRef[ed:]
							st = tmpRef.find('<', ed2)
							ed = tmpRef.find('>', st)
							postTagName = tmpRef[st+1:ed]
							while postTagName not in validLabels and st > 0 :
								st = tmpRef.find('<', ed)
								ed = tmpRef.find('>', st)
								postTagName = tmpRef[st+1:ed]
							if postTagName in validLabels :
								'And if it has sufficient tags in current bloc. if only names, stop'
								tmpPtr, ed1, st2, ed2 = tagtool._findTagPosition(tmpRef, 'nonbibl', ed)
								if tmpPtr < 0 : tmpPtr = limit2
								tmpCentre = BeautifulSoup(tmpRef[st:tmpPtr])
								sepBibl = False
								c = 0
								for tcen in tmpCentre.find_all() :
									if tcen.name in separateLabels : c+= 1
								if c > 1 : sepBibl = True
								if sepBibl :
									tmpRef = tmpRef[:st] + '<bibl>' + tmpRef[st:]
									st1 = st
									oriRef = tmpRef
									case2 = True
					st1, ed1, st2, ed2 = tagtool._findTagPosition(oriRef, 'nonbibl', st1+1)
				
		return oriRef
	
	
	def _getName(self):
		"""
		Return the file name without the complete path
		"""
		chemin = self.nom.split("/")
		return chemin.pop()
	

	def convertToUnicode(self, chaine):
		"""
		Convert a string to unicode
		"""
		try:
			if isinstance(chaine, str):
				chaine = unicode(chaine, sys.stdin.encoding)
		except:
			chaine = unicode(chaine, 'ascii')
		return chaine

	