'''
Created on 25 avr. 2012

@author: jade
'''

class Properlist(object):
	'''
	classdocs
	'''


	def __init__(self, fname, nameFeature):
		'''
		Constructor
		'''
		self.targetfeature = nameFeature
		self.properlist = {'0000': 0} #other proper nouns than person names considering whitespaces
		self.m_properlist = {'0000': {'0000': 0}}
	
		self.targetlist = self.properlist
		self.m_targetlist = self.m_properlist
		
		for line in open (fname, 'r') :
			line = line.split('\n')
			line = line[0].split('(')
			line = line[0].split(',')
			line = line[0].split('\t')
			
			st = ''
			for l in line[0].split() :
				st = st+l[0].upper()+l[1:len(l)].lower()+' '
			st = st[:len(st)-1]
			key = st.split()[0]
			
			if key == st :
				self.targetlist[key] = 1
			else :
				if not self.m_targetlist.has_key(key) :
					self.m_targetlist[key] = {st:1}
				else :
					self.m_targetlist[key][st] = 1
		

	def searchProper2(self, tmp_bibl, tr, listname) :
		
		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
		
		self.targetlist = self.properlist
		self.m_targetlist = self.m_properlist
		
		
		
		for i in range(len(tmp_bibl)) :
			token = tmp_bibl[i][0]
			token0 = token
			token2 = token[0]+ token[1:len(token)].lower()
			
			if token != token2 : token = token2
			
			if self.targetlist.has_key(token) :
				#print token
				#raw_input("Press Enter to Exit")
				tmp_bibl[i].insert(len(tmp_bibl[i])-pt, self.targetfeature)
				#print tmp_bibl[i]
				#raw_input("Press Enter to Exit")
				
			elif self.m_targetlist.has_key(token) :
				full_str = ''
				for j in range(i,len(tmp_bibl)) :
					full_str = full_str + tmp_bibl[j][0] + ' '
				
				tokens = ''
				for key in self.m_targetlist[token].keys() :
					if full_str.find(key) >= 0 :
						tokens = key
				
				tokens = tokens.split() 
				for j in range(i,i+len(tokens)) :
					curr = tmp_bibl[j][0]
					if tokens[j-i] == curr :
						tmp_bibl[j].insert(len(tmp_bibl[j])-pt, self.targetfeature)
						#print tokens
						#raw_input("Press Enter to Exit")
					#print tmp_bibl[j]
					#raw_input("Press Enter to Exit")
		return tmp_bibl
	
	def searchProper(self, listReference, tr, listname) :
		
		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
		
		self.targetlist = self.properlist
		self.m_targetlist = self.m_properlist
		
		for reference in listReference.getReferences():
			cpt = 0
			for mot in reference.getWord():
				
				token = mot.nom
				token0 = token
				token2 = token[0]+ token[1:len(token)].lower()
				
				if token != token2 : token = token2
				
				if self.targetlist.has_key(token) :
					#print token
					#raw_input("Press Enter to Exit")
					mot.addFeature(self.targetfeature)
					#print tmp_bibl[i]
					#raw_input("Press Enter to Exit")
					
				elif self.m_targetlist.has_key(token) :
					full_str = ''
					for j in range(cpt,reference.nbWord()) :
						try:
							full_str = full_str + reference.getWordIndice(j).nom + ' '
						except UnicodeDecodeError:
							pass
					
					tokens = ''
					for key in self.m_targetlist[token].keys() :
						if full_str.find(key) >= 0 :
							tokens = key
					
					if len(tokens) > 0:
						tokens = tokens.split() 
						for j in range(cpt,cpt+len(tokens)) :
							curr = reference.getWordIndice(j)
							if tokens[j-cpt] == curr.nom :
								curr.addFeature(self.targetfeature)
				cpt += 1
