# encoding: utf-8
'''
Created on 2 mai 2012

@author: Young-min Kim, Jade Tavernier
'''
import sys

class GenerateXml(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		self.labels =  {'.':0, ',':0, '(':0, ')':0, ':':0, ';':0, '«':0, '»':0, '-':0, '“':0, '”':0, '{':0, '}':0, '[':0, ']':0,  '!':0, '?':0}
		
	def simpleComp(self, truefile, estfile, indicator, outfile):
	
		est = []
		for line in open (estfile, 'r') :
			line = line.split()
			if len(line) != 0 :
				est.append(line[0])
				
		fout = open(outfile, "w")
	
		num = 0
		j = 0
		preLabel = 'start'
		preckIt = 0
		fout.write('<listBibl>\n\n')
		for line in open (truefile, 'r') :
			if preLabel == 'start' :
				num += 1
				fout.write('<bibl>\n')
				
			line = line.split()
			if len(line) != 0 :
				currToken = line[0]
				currLabel = line[len(line)-1]
				ckIt = 0 # if you don't want to insert italic attribute, run it
				if self.labels.has_key(currLabel) : currLabel = 'c'
				estLabel = est[j]
				if self.labels.has_key(estLabel) : estLabel = 'c'
				
				if indicator == 2 : currLabel = estLabel
				
				if (preLabel == currLabel) :
					if preckIt == ckIt :
						tmp_str = currToken+' '
					elif ckIt == 1 :
						tmp_str = '<hi rend="italic"> '+currToken+' '
					elif ckIt == 0 :
						tmp_str = '</hi> '+currToken+' '
					fout.write(tmp_str)
	
				else :
					if not preLabel == 'start' :
						if preckIt == 0 :
							tmp_str = '</'+preLabel+'>\n'
						else : 
							tmp_str = '</hi></'+preLabel+'>\n'
						fout.write(tmp_str)
					if ckIt == 0 :
						tmp_str = '<'+currLabel+'> '+currToken+' '
					else :
						tmp_str = '<'+currLabel+'><hi rend="italic"> '+currToken+' '
					fout.write(tmp_str)
					
				preLabel = currLabel
				preckIt = ckIt
				j += 1
			else :
				if preckIt == 0 :
					if preLabel == 'start' :
						tmp_str = '</bibl>\n\n'
					else:
						tmp_str = '</'+preLabel+'>\n</bibl>\n\n'
				else :
					if preLabel == 'start' :
						tmp_str = '</bibl>\n\n'
					else:
						tmp_str = '</hi></'+preLabel+'>\n</bibl>\n\n'
				fout.write(tmp_str)
				preLabel = 'start'
				
		fout.write('\n</listBibl>\n\n')
		fout.close()
			
		return