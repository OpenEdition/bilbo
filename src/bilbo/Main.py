'''
Created on April 20, 2012

@author: Young-Min Kim, Jade Tavernier
	argv[1] : 1 => annotate corpus 1, 2 => annotate corpus 2, 11 => train corpus 1, 22 => train corpus 2
	argv[2] : directory where the data files are
	argv[3] : directory where the result files are saved (default : Result)

This is Main.py that creates bilbo object to learn and label reference data.

'''
import sys
import os
import optparse

'''
Add paths to the package
'''
directoryTab = os.getcwd().replace("\\", "/").split("/")
last = directoryTab.pop()
if last == "bilbo":
	directoryTab.append(last)
	directoryTab.append("src")
	directory = "/".join(directoryTab)
	sys.path.append(directory)
else:
	print "error: please execute the program from bilbo fold"
	

from bilbo.Bilbo import Bilbo

if __name__ == '__main__':
	
	parser = optparse.OptionParser(
		usage ='%prog [options] <input data folder> <output data folder>'
		'\n  e.g. (training) python src/bilbo/Main.py -T -t bibl Data/train/ Result/train/'
		'\n       (labeling) python src/bilbo/Main.py -L -t bibl -d Data/test/ Result/test/'
		'\n       for more information, type \"python src/bilbo/Main.py\" without --help option' 
					
		)
	parser.add_option('-T', '--Training', dest="T", default=False, action="store_true", help="Bilbo training")
	parser.add_option('-L', '--Labeling', dest="L", default=False, action="store_true", help="Bilbo labeling")
	common_opts = optparse.OptionGroup(
		parser, 'Training and labeling options',
		'These options are for both training and labeling'				
		)
	common_opts.add_option('-t', '--typeref', dest="t", default="bibl", action="store", type='choice', choices=['bibl', 'note', 'impl'], help="Input reference type")
	common_opts.add_option('-i', '--informat', dest="i", default="tei", action="store", type='choice', choices=['tei', 'xml', 'plain'], help="Input reference format")
	common_opts.add_option('-m', '--model', dest="m", default="revues", action="store", help="Bilbo model name")
	common_opts.add_option('-g', '--gradetag', dest="g", default="simple", action="store", type='choice', choices=['simple', 'detail'], help="Grade of tag detail when using tei")
	common_opts.add_option('-k', '--keeptmp', dest="k", default="none", action="store", type='choice', choices=['none', 'primary', 'all'], help="Decide which temp files are kept")
	common_opts.add_option('-s', '--svmfilt', dest="s", default=False, action="store_true", help="Use a svm for training or labeling")
	parser.add_option_group(common_opts)
	label_opts = optparse.OptionGroup(
		parser, 'Labeling options',
		'These options are for labeling only'				
		)	
	label_opts.add_option('-o', '--outformat', dest="o", default="tei", action="store", type='choice', choices=['tei', 'xml'], help="Output reference format")
	label_opts.add_option('-d', '--doi', dest="d", default=False, action="store_true", help="DOI extraction via crossref site")
	label_opts.add_option('-e', '--exterdata', dest="e", default=False, action="store_true", help="Labeling data different from training set")	
	parser.add_option_group(label_opts)
	
	options, args = parser.parse_args(sys.argv[1:])
	
	#bilbo = Bilbo()
	
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
		
		print "  -s : --svmfilt"
		print "\t Training a svm model or classifying notes to filter out non-bibliographical notes, default='False'"

		print "(labeling)"		
		print "  -o : --outformat <string>"
		print "\t Output data format"
		print "\t  tei => xml following tei guidelines (default)"
		print "\t  xml => simple xml"
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
		dirModel = "model/corpus"+str(typeCorpus)+"/"+options.m+"/"
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
			

		