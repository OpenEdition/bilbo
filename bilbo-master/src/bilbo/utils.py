# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on March 7, 2013

@author: Young-Min Kim

This is utils.py providing APIs to process simple string for labeling.
It also contains default option setting function, which is called in main.

"""
import sys
import os
import optparse

"""
Add paths
"""
main = os.path.realpath(__file__).split('/')
rootDir = "/".join(main[:len(main)-3])
srcDir = os.path.join(rootDir, 'src')
sys.path.append(srcDir)

from bilbo.Bilbo import Bilbo


def simpleLabeling(line, type='bibl'):
	"""
	Label input string with simple annotation
	"""
	if type == 'bibl' : optStr = '-T -t bibl -d '
	elif type == 'note' : optStr = '-T -t note -d '
	parser = defaultOptions()
	options, args = parser.parse_args(optStr.split())
	result = labeling(line, 'crf_model_simple', options)
	return result


def detailLabeling(line, type='bibl'):
	"""
	Label input string with detailed annotation
	"""
	if type == 'bibl' : optStr = '-T -t bibl -d '
	elif type == 'note' : optStr = '-T -t note -d '
	parser = defaultOptions()
	options, args = parser.parse_args(optStr.split())
	result = labeling(line, 'crf_model_detail', options)
	return result


def labeling(line, modelname, options):
	"""
	Label input sting. Called by simpleLabeling or detailLabeling
	"""
	tmpDir = rootDir+'/simpletmp'
	resDir = os.getcwd() #current working directory
	
	dtype = options.t
	if dtype == "bibl" : typeCorpus = 1
	elif dtype == "note" : typeCorpus = 2
	dirModel = os.path.join(rootDir, 'model/corpus')+str(typeCorpus)+"/"+options.m+"/"
	
	bilbo = Bilbo(resDir, options, modelname)
	if not os.path.exists(tmpDir):
		os.makedirs(tmpDir)
	else : #delete all existing files
		for dir_name, sub_dirs, files in os.walk(tmpDir):
			for f in files : os.unlink(os.path.join(dir_name, f))
	#tmp file generation
	filename = os.path.join(tmpDir, 'tmp.xml')
	tmpFile = open(filename, "w")
	tmpFile.write('<list'+dtype.title()+'>\n')
	tmpFile.write('<'+dtype+'> '+str(line)+' </'+dtype+'>')
	tmpFile.write('\n</list'+dtype.title()+'>\n')
	tmpFile.close()
	
	if options.t == "note" and options.e: bilbo.annotate(tmpDir, dirModel, typeCorpus, 1)
	else : bilbo.annotate(tmpDir, dirModel, typeCorpus)
	
	tmp_str = ''.join(open(os.path.join(resDir, 'tmp.xml')).readlines())
	
	os.unlink(filename)
	os.rmdir(tmpDir)
	
	return tmp_str


def defaultOptions():
	"""
	Set default options. Called in Main.py
	"""
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
	common_opts.add_option('-v', '--validatexml', dest="v", default="none", action="store", type='choice', choices=['none', 'input', 'output', 'all'], help="XML schema validation")
	common_opts.add_option('-s', '--svmfilt', dest="s", default=False, action="store_true", help="Use a svm for training or labeling")
	common_opts.add_option('-u', '--undopuncsep', dest="u", default=False, action="store_true", help="undo punctuation separation")
	parser.add_option_group(common_opts)
	label_opts = optparse.OptionGroup(
		parser, 'Labeling options',
		'These options are for labeling only'
		)
	label_opts.add_option('-o', '--outformat', dest="o", default="tei", action="store", type='choice', choices=['tei', 'xml', 'simple'], help="Output reference format")
	label_opts.add_option('-d', '--doi', dest="d", default=False, action="store_true", help="DOI extraction via crossref site")
	label_opts.add_option('-e', '--exterdata', dest="e", default=False, action="store_true", help="Labeling data different from training set")
	parser.add_option_group(label_opts)
	
	return parser
