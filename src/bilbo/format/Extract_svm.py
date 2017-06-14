# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on June 17, 2012

@author: Young-Min Kim, Jade Tavernier
"""
from codecs import open
from bilbo.format.Extract import Extract
import codecs
import numpy, os

class Extract_svm(Extract):
    
    def __init__(self, options={}):
        Extract.__init__(self, options)
        self.tokens = []
        self.idf = []	
        self.features = []
        self.doc_tokens = {'0000':0}
        self.doc_features = {'0000':0}
        self.options = options
        main = os.path.realpath(__file__).split('/')
        self.rootDir = "/".join(main[:len(main)-4])
        self.valid_features = {'punc':0, 'nopunc':0, 'onepunc':0, 'twopunc':0, 'nonumbers':0, 'dash':0,
						'noinitial':0, 'startinitial':0, 'posspage':0, 'weblink':0, 'posseditor':0, 'italic':0}


    def extract (self, filename, ndocs, tr, filename_ori, file_out) :
        i = 0
        indices = range(ndocs)
        flagEndRef = 0
        
        if tr == 1 :
            for i in range(len(indices)) :
                indices[i] = 1
        else :
            for i in range(len(indices)) :
                indices[i] = tr
            self.load_ID(self.tokens, self.features)
                
        token_data = []
        feature_data = []
        bibls = range(int(ndocs*1.0))
        
        i = 0
        for line in open (filename, 'r') :
            line = line.split()
            
            if len(line) != 0:
                if line[0] == '1' or line[0] == '-1' :
                    self.fill_data(line[1:], self.tokens, token_data, tr)
                    bibls[i] = line[0]
                else :
                    flagEndRef += 1
                    self.fill_data(line, self.features, feature_data, tr)
                    
            else :
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
        
    def extractP (self, filename, ndocs, tr, filename_ori, file_out) :
        i = 0
        indices = range(ndocs)
        flagEndRef = 0
        
        if tr == 1 :
            for i in range(len(indices)) :
                indices[i] = 1
        else :
            for i in range(len(indices)) :
                indices[i] = tr
            self.load_ID_P(self.tokens, self.features)
                
        token_data = []
        feature_data = []
        bibls = range(int(ndocs*1.0))
        
        i = 0
        for line in open (filename, 'r') :
            line = line.split()
            
            if len(line) != 0:
                if line[0] == '1' or line[0] == '-1' :
                    self.fill_data(line[1:], self.tokens, token_data, tr)
                    bibls[i] = line[0]
                else :
                    flagEndRef += 1
                    self.fill_data(line, self.features, feature_data, tr)
                    
            else :
                if flagEndRef == 1:
                    i += 1
                    flagEndRef = 0
                else:
                    feature_data.append({})
                    flagEndRef += 1
                    
        self.insert_lineFeatures(feature_data, tr)
        self.print_output(token_data, feature_data, bibls, tr, indices, file_out)
        if tr == 1 : self.save_ID_P(self.tokens, self.features)
            
        return


    def fill_data(self, line, input, data, tr) :
        self.doc_tokens.clear()
        for n in line :
            if input.count(n.lower()) == 0 :
                if tr == 1 : 
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
        puncnt = 0
        
        if tr == 1 :
            self.features.extend(['nopunc', 'onepunc', 'twopunc', 'nonumbers', 'noinitial'])
            
        for i in range(len(feature_data)) :
            new_features = []
            try:
                id = self.features.index('punc')
                if id in feature_data[i] :
                    puncnt = feature_data[i][id]
                    if puncnt == 1 : new_features.append('onepunc')
                    elif puncnt == 2 : new_features.append('twopunc')
                else :
                    puncnt == 0
                    new_features.append('nopunc')
                    
                if not feature_data[i].has_key(self.features.index('numbers')) and not feature_data[i].has_key(self.features.index('allnumbers')) :
                    new_features.append('nonumbers')
                if not feature_data[i].has_key(self.features.index('initial')) :
                    new_features.append('noinitial')
                    
                if feature_data[i].has_key(self.features.index('startinitial')) : new_features.append('startinitial')
                for nf in new_features :
                    id = self.features.index(nf)
                    feature_data[i][id] = 1
            except ValueError:
                pass


    def print_output(self, token_data, feature_data, bibls, tr, indices, fileOut) :
        fich = codecs.open(fileOut, "w", encoding="utf-8")
        i = 0
        adding = self.adding_fId(len(self.tokens), feature_data)
        
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
        flagEndRef = 0
        fouttr = open(os.path.join(self.rootDir, "Result/original_train.txt"), "w")
        fouttst = open(os.path.join(self.rootDir, "Result/original_test.txt"), "w")
        
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
        fname = "model/corpus2/"+self.options.m+"/inputID.txt"
        f = open(os.path.join(self.rootDir, fname), 'w')
        for k in tokens :
            f.write(str(k))
            f.write('\n')
        f.close()
        
        fname = "model/corpus2/"+self.options.m+"/featureID.txt"
        f = open(os.path.join(self.rootDir, fname), 'w')
        for k in features :
            f.write(str(k))
            f.write('\n')
        f.close()
        return


    def load_ID(self, tokens, features) :
        del tokens[:]
        fname = "model/corpus2/"+self.options.m+"/inputID.txt"
        for line in open(os.path.join(self.rootDir, fname), 'r', encoding='utf8') :
            n = line.split('\n')
            tokens.append(n[0])
            
        del features[:]
        fname = "model/corpus2/"+self.options.m+"/featureID.txt"
        for line in open(os.path.join(self.rootDir, fname), 'r', encoding='utf8') :
            n = line.split('\n')
            features.append(n[0])
        del self.idf[:]
        self.idf = numpy.zeros(len(tokens))
        
        return
        
    def save_ID_P(self, tokens, features) :
        fname = "model/corpus3/"+self.options.m+"/inputID.txt"
        f = open(os.path.join(self.rootDir, fname), 'w')
        for k in tokens :
            f.write(str(k))
            f.write('\n')
        f.close()
        
        fname = "model/corpus3/"+self.options.m+"/featureID.txt"
        f = open(os.path.join(self.rootDir, fname), 'w')
        for k in features :
            f.write(str(k))
            f.write('\n')
        f.close()
        return


    def load_ID_P(self, tokens, features) :
        del tokens[:]
        fname = "model/corpus3/"+self.options.m+"/inputID.txt"
        for line in open(os.path.join(self.rootDir, fname), 'r', encoding='utf8') :
            n = line.split('\n')
            tokens.append(n[0])
            
        del features[:]
        fname = "model/corpus3/"+self.options.m+"/featureID.txt"
        for line in open(os.path.join(self.rootDir, fname), 'r', encoding='utf8') :
            n = line.split('\n')
            features.append(n[0])
        del self.idf[:]
        self.idf = numpy.zeros(len(tokens))
        
        return
