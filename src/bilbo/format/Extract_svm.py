# -*- coding: utf-8 -*-
'''
Created on June 17, 2012

@author: Young-Min Kim, Jade Tavernier
'''

from bilbo.format.Extract import Extract
import codecs
import numpy

class Extract_svm(Extract):
	'''
	A class to extract training and test data for SVM
	Sub class of Extract
	'''

	def __init__(self, options={}):
		'''
		Attributes
		----------	
		tokens : List of String
			tokens[k] -> TOKEN STRING with token id 'k'
		idf : List of int
			idf[k] -> document frequency of token id 'k'
		features : List of String
			features[k] -> FEATURE STRING with feature id 'k'
		doc_tokens : dict
			tmp document represented by token strings and their counts
		doc_features : dict 
			tmp document represented by feature strings and their counts
		valid_features : dict
			*IMPORTANT* valid features to be considered for the svm classification 
		'''			
		Extract.__init__(self, options)
		self.tokens = []	# tokens[k] : TOKEN STRING with token id 'k'
		self.idf = []		# idf[k] : document frequency of token id 'k'
		self.features = []	# features[k] : FEATURE STRING with feature id 'k'
		self.doc_tokens = {'0000':0}	# tmp document represented by token strings and their counts
		self.doc_features = {'0000':0}	# tmp document represented by feature strings and their counts
		self.options = options

		self.valid_features = {'punc':0, 'nopunc':0, 'onepunc':0, 'twopunc':0, 'nonumbers':0, 'dash':0,
						'noinitial':0, 'startinitial':0, 'posspage':0, 'weblink':0, 'posseditor':0, 'italic':0}
		
		
	def extract (self, filename, ndocs, tr, filename_ori, file_out) : # tr=1 : training, tr=0 : test
		'''
		Extract training and test data in numerical format from source input file which has been 
		extracted from previous process Extract_crf::prepareTest 

		Parameters
		----------	
		filename : String
			input file name containing source information of data
		ndocs : int
			number of instances
		tr : int, {1, 0}
			check if training (1) or test data (0)
		filename_ori : String
			original file name keeping the original string of input data
			it's used to check the classification error.
			for the moment it's same as "filename", but can be modified.
		file_out : String
			output file name. this file will be used as training or test data for SVM light
		'''			
		i = 0
		indices = range(ndocs)
		flagEndRef = 0
		
		# IN FACT WE DON'T NEED IT ANY MORE BUT FOR THE MODIFICATION WE KEEP IT
		if tr == 1 : # Now we don't split data into learning/test data. So for test, we need to load features and tokens
			for i in range(len(indices)) :
				indices[i] = 1
		else : # when extracting new data
			for i in range(len(indices)) :
				indices[i] = tr
			self.load_ID(self.tokens, self.features)
		
		token_data = []		# TOTAL DATA for tokens, token_data[i] = i_th document DICT containing token ids and token counts
		feature_data = []	# TOTAL DATA for features, feature_data[i] = i_th document DICT containing feature ids and feature counts
		bibls = range(int(ndocs*1.0))
		
		i = 0
		for line in open (filename, 'r') :
			line = line.split()
			
			if len(line) != 0:
				if line[0] == '1' or line[0] == '-1' : #input tokens
					self.fill_data(line[1:], self.tokens, token_data, tr)
					bibls[i] = line[0]
				else :	# local features
					flagEndRef += 1
					self.fill_data(line, self.features, feature_data, tr)
	
			else : # end of a block, a note		
				if flagEndRef == 1:
					i += 1
					flagEndRef = 0
				else:
					feature_data.append({})
					flagEndRef += 1

		self.insert_lineFeatures(feature_data, tr)
		self.print_output(token_data, feature_data, bibls, tr, indices, file_out)
		if tr == 1 : self.save_ID(self.tokens, self.features)
		
		return
	
	
	def fill_data(self, line, input, data, tr) : # line[1:], tokens, token_data / line, features, feature_data
		'''
		Read data in numerical format
		'''
		self.doc_tokens.clear()
		for n in line :
			if input.count(n.lower()) == 0 :
				if tr == 1 : ##### added 291012
					input.append(n.lower())
					self.idf.append(1)
					self.doc_tokens[n.lower()] = 1
			else :
				id = input.index(n.lower())
				if not self.doc_tokens.has_key(n.lower()) :
					self.idf[id] += 1
					self.doc_tokens[n.lower()] = 1
				else :
					self.doc_tokens[n.lower()] += 1
					
		data.append([])
		data[len(data)-1] = {-1:-1}
		for key in self.doc_tokens.keys() :
			id = input.index(key)
			data[len(data)-1][id] = self.doc_tokens[key]
		del data[len(data)-1][-1]
		
		return
	
	
	# 
	def insert_lineFeatures(self, feature_data, tr) :
		'''
		Insert new FEATURES related with global character of reference : NOPUNC, ONEPUNC, NONUMBERS, NOINITIAL
		'''
		puncnt = 0
		#extended featues
		if tr == 1 :
			self.features.extend(['nopunc', 'onepunc', 'twopunc', 'nonumbers', 'noinitial'])
		
		
		for i in range(len(feature_data)) :
			new_features = [] # list for newly added features for the corresponding document
			
			#puncutation marks check
			try:
				id = self.features.index('punc')
				if id in feature_data[i] :
					puncnt = feature_data[i][id]
					if puncnt == 1 : new_features.append('onepunc')
					elif puncnt == 2 : new_features.append('twopunc')
				else : 
					puncnt == 0
					new_features.append('nopunc')
					
				#All data count
				'''
				allcnt = 0.
				keylist = feature_data[i].keys()
				for key in keylist:
					allcnt += feature_data[i][key]
				'''

				#'numbers', 'allnumbers', 'initial' check 
				if not feature_data[i].has_key(self.features.index('numbers')) and not feature_data[i].has_key(self.features.index('allnumbers')) :
					new_features.append('nonumbers')
				if not feature_data[i].has_key(self.features.index('initial')) : 
					new_features.append('noinitial')
	
				#we can also append some important featues to the new_features list for weighting them 
				if feature_data[i].has_key(self.features.index('startinitial')) : new_features.append('startinitial')
				
				#now update features representation of the document with previously found features
				for nf in new_features :
					id = self.features.index(nf)
					feature_data[i][id] = 1#*len(feature_data[i]) # !!!!!!! VALIDE CONSIDERATION OF VECTOR SIZE !				
			except ValueError:
				pass
		
		
	def print_output(self, token_data, feature_data, bibls, tr, indices, fileOut) :
		'''
		Print final svm data file
		'''
		fich = codecs.open(fileOut, "w", encoding="utf-8")

		i = 0
		adding = self.adding_fId(len(self.tokens), feature_data)
		#adding = len(tokens) + 1
		
		
		for i in range(len(token_data)) :
			keylist = token_data[i].keys()
			keylist.sort()
			
			if indices[i] == tr :
				try:
					fich.write( unicode(bibls[i], "utf-8")+" ")
				except:
					fich.write( str(bibls[i])+" ")

			for key in keylist:
				if indices[i] == tr :
					fich.write( str(key+1)+':'+str(token_data[i][key])+" ")
			
			if len(feature_data) > 0 :
				keylist = feature_data[i].keys()
				keylist.sort()
				for key in keylist:
					if indices[i] == tr :
						if self.valid_features.has_key(self.features[key]) :
							fich.write( str(key+adding+1)+':1'+" ")
							
			if indices[i] == tr :
				fich.write("\n")
	
		return
		
	
	#for the counting of input tokens
	def adding_fId(self, tokens_len, feature_data) :
		i = 10
		while i < tokens_len :
			i = i*10
		return i
	
	
	def load_original(self, filename_ori, indices) :
		'''
		Create files having original text form for the verification
		'''
		flagEndRef = 0
		fouttr = open("Result/original_train.txt", "w")
		fouttst = open("Result/original_test.txt", "w")
		
		i = 0
		j=0
		for line in open(filename_ori, 'r') :
			if len(line.split()) != 0 :
				if indices[i] == 1 :
					if j == 0 : fouttr.write(line.split('\n')[0])
					else : fouttr.write(line)
				else :
					flagEndRef += 1
					if j == 0 : fouttst.write(line.split('\n')[0])
					else : fouttst.write(line)
				j += 1
			else : 
				if flagEndRef == 1:
					i += 1
					j=0
				else:
					flagEndRef = 0
		
		fouttr.close()
		fouttst.close()
	
		return


	def save_ID(self, tokens, features) :
		'''
		Save input(token) id list and feature id list for new data
		'''
		f = open("model/corpus2/"+self.options.m+"/inputID.txt", 'w')
		for k in tokens :
			f.write(str(k))
			f.write('\n')
		f.close()
		
		f = open("model/corpus2/"+self.options.m+"/featureID.txt", 'w')
		for k in features :
			f.write(str(k))
			f.write('\n')
		f.close()
		return


	def load_ID(self, tokens, features) :
		'''
		Load input(token) id list and feature id list for new data
		'''
		#load input(token) id list for new data
		del tokens[:]
		for line in open("model/corpus2/"+self.options.m+"/inputID.txt", 'r') :
			n = line.split('\n')
			tokens.append(n[0])
		#load feature id list for new data
		del features[:]
		for line in open("model/corpus2/"+self.options.m+"/featureID.txt", 'r') :
			n = line.split('\n')
			features.append(n[0])
		del self.idf[:]
		self.idf = numpy.zeros(len(tokens))
		
		return
