'''
Created on 25 avr. 2012

@author: jade
'''

class Place(object):
	'''
	classdocs
	'''


	def __init__(self, fname):
		'''
		Constructor
		'''
		self.placelist = {'0000': 0}
		
		'''
		load fichier lexique
		'''
		for line in open (fname, 'r') :
			line = line.split('\n')[0]
			self.placelist[line] = 1
	
	
	'''
	searchPlace: 
	'''
	def searchPlace2(self, tmp_bibl, tr) :

		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
	
		for i in range(len(tmp_bibl)) :
			st = tmp_bibl[i][0]
			
			if self.placelist.has_key(st.upper()) :
				tmp_bibl[i].insert(len(tmp_bibl[i])-pt, 'PLACELIST')
			
		return tmp_bibl
	
	'''
	searchPlace: 
	listReference objet ListReference
	'''
	def searchPlace(self, listReference, tr) :

		if tr == 1 or tr == -1 :	pt = 1
		elif tr == 0 :	pt = 0
	
		for reference in listReference.getReferences():
			for mot in reference.getWord():
				if self.placelist.has_key(mot.nom.upper()):
					mot.addFeature('PLACELIST')
		