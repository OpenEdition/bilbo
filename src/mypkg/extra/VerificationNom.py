'''
Created on 25 avr. 2012

@author: jade
'''

class VerificationNom(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		self.namelist = {'0000': {'000': 0}}
		self.multi_namelist = {'0000': {'0000': 0}} #when surname is more than a word
		self.forenamelist = {'0000': 0}
		self.placelist = {'0000': 0}
		
		self.properlist = {'0000': 0} #other proper nouns than person names considering whitespaces
		self.m_properlist = {'0000': {'0000': 0}}
		
		self.properlist_surname = {'0000': 0} #do not count the cooccurrence with forename
		self.m_properlist_surname = {'0000': {'0000': 0}}
		self.properlist_forename = {'0000': 0} #do not count the cooccurrence with forename
		self.m_properlist_forename = {'0000': {'0000': 0}}
		
		
	def load_name(self, fname) :

		for line in open (fname, 'r') :
			line = re.sub(' ', ' ', line)
			line = string.replace(line, '‑','-')
			#line = string.replace(nline, '.','')
			line = line.split('/')
			fname = line[0].split()
			sname = line[1].split()
			f_st = ''
			if len(fname) > 0 :
				for n in fname : f_st = f_st+n+' '
				f_st = f_st[:len(f_st)-1]	
		
			s_st = ''
			if len(sname) > 0 :
				for n in sname : s_st = s_st+n+' '
				s_st = s_st[:len(s_st)-1]
				
			if namelist.has_key(s_st) :
				namelist[s_st][f_st] = 1
			else :
				namelist[s_st] = {f_st:1}
			
			if len(s_st.split()) > 1 :
				start_sname = s_st.split()[0]
				if multi_namelist.has_key(start_sname) :
					multi_namelist[start_sname][s_st] = 1
				else :
					multi_namelist[start_sname] = {s_st:1}
				
			forenamelist[f_st] = 1
