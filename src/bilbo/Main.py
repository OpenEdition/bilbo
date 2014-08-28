# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on April 20, 2012

@author: Young-Min Kim, Jade Tavernier

This is Main.py that creates bilbo object to learn and label reference data.

"""
import sys
import os

"""
Add paths to the package
"""
main = os.path.realpath(__file__).split('/')
rootDir = "/".join(main[:len(main)-3])
srcDir = os.path.join(rootDir, 'src')
sys.path.append(srcDir)


from bilbo.Bilbo import Bilbo
from bilbo.utils import *

if __name__ == '__main__':
	parser = defaultOptions()
	options, args = parser.parse_args(sys.argv[1:])
	
	if len(args) < 2 or ((not options.T) and (not options.L)) :
		print "--------------------------------------"
		print " BILBO : automatic reference labeling"
		print "--------------------------------------"
		print "Usage: python src/bilbo/Main.py [options] <input data folder> <output data folder>"
		print "e.g. training: python src/bilbo/Main.py -T -t bibl Data/train/ Result/train/"
		print "     labeling: python src/bilbo/Main.py -L -t bibl -d Data/test/ Result/test/"
		print "Options"
		print "(mode)"
		print "  -T : --Training"
		print "\t Bilbo training, default='False'"
		print "  -L : --Labeling"
		print "\t Data labeling, default='False'"

		print "(training, labeling)"
		print "  -t : --typeref <string>"
		print "\t Input reference type"
		print "\t  bibl => bibliography with a heading, wrapped by <bibl></bibl> (default)"
		print "\t  note => notes wrapped by <note></note>"
		print "\t  impl => implicit citations"
		
		print "  -i : --informat <string>"
		print "\t Input reference format"
		print "\t  tei => xml following tei guidelines including manual annotation (defalut)"
		print "\t  xml => simple xml without tree in manual annotation"
		print "\t  plain => plain text (for labeling only)"
		
		print "  -m : --model <string>"
		print "\t Bilbo model name, default='revues'"
		print "\t create a folder under \"model/\" folder and save models when training / load models when labeling"

		print "  -g : --gradetag <string>"
		print "\t Grade of tag detail when using tei (option -f or -o)"
		print "\t  simple => simple title and biblscope (default)"
		print "\t  detail => detailed title and biblscope"

		print "  -k : --keeptmp <string>"
		print "\t Decide which temp files are kept, among those created for svm crf training or test"
		print "\t  none => keep nothing (default)"
		print "\t  primary => keep primary temp files"
		print "\t  all => keep all files"

		print "  -v : --validatexml <string>"
		print "\t Decide if we validate files, "
		print "\t  none => do not validate (default)"
		print "\t  input => validate input files with tei_all.dtd"
		print "\t  output => validate output files with tei_openedition3.xsd"
		print "\t  all => validate input and output files"

		print "  -s : --svmfilt"
		print "\t Training a svm model or classifying notes to filter out non-bibliographical notes, default='False'"

		print "  -u : --undopuncsep"
		print "\t Undo punctuation separation, default='False'"
		
		print "(labeling)"
		print "  -o : --outformat <string>"
		print "\t Output data format"
		print "\t  tei => xml following tei guidelines (default)"
		print "\t  xml => simple xml"
		print "\t  simple => only labeled references without article contents or original tags"
		print "  -d : --doi"
		print "\t Digital object identifier (doi) extraction via crossref site, default='False'"
		print "  -e : --exterdata"
		print "\t Labeling data different from training set. Do not use svm filtering when using this option. default='False'"
		
		print "Arguments"
		print "  arg1 : <string>"
		print "\t input data folder where the data files are (training or labeling)"
		print "  arg2 : <string>"
		print "\t output data folder where the result files are saved\n"

	else:
		if options.g == "simple" :
			bilbo = Bilbo(str(args[1]), options, "crf_model_simple")
		elif options.g == "detail" :
			bilbo = Bilbo(str(args[1]), options, "crf_model_detail")
			
		dtype = options.t
		if dtype == "bibl" : typeCorpus = 1
		elif dtype == "note" : typeCorpus = 2
		dirModel = os.path.join(rootDir, 'model/corpus')+str(typeCorpus)+"/"+options.m+"/"
		if not os.path.exists(dirModel): os.makedirs(dirModel)
		
		if options.T : #training
			bilbo.train(str(args[0]), dirModel, typeCorpus)
		elif options.L : #labeling
			if dtype == "note" and options.e:
				bilbo.annotate(str(args[0]), dirModel, typeCorpus, 1)
			else :
				bilbo.annotate(str(args[0]), dirModel, typeCorpus)
		else :
			print "Please choose training(-T option) or labeling(-L option)"

	#simpleLabeling("Y.-M. KIM et al., An Extension of PLSA for Document Clustering, In Proceedings of ACM 17th Conference on Information and Knowledge Management, 2008.")

