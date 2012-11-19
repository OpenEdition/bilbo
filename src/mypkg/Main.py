'''
Created on 19 avr. 2012

@author: Young-Min Kim, Jade Tavernier
	argv[1] : 1 => annotate corpus 1, 2 => annotate corpus 2, 11 => train corpus 1, 22 => train corpus 2
	argv[2] : directory where the data files are
	argv[3] : directory where the result files are saved (default : Result)

This is Main.py that create bilbo object to learn and annotate reference data.

'''
import sys
import os

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
	

from mypkg.bilbo.Bilbo import Bilbo

if __name__ == '__main__':
	pass


	if len(sys.argv) < 2:

		print "$ python src/mypkg/Main.py <arg 1> <arg 2> <arg 3>"
		print " <arg 1> : integer \n\t 11 => train corpus 1 (references), \n\t 22 => train corpus 2 (notes), \n\t 1 => annotate(test) reference corpus 1, \n\t 2 => annotate reference corpus 2, \n\t 21 => annotate corpus 2 with external data."
		print " <arg 2> : string \n\t input directory where the data files are (training or test)"
		print " <arg 3> : string \n\t output directory where the result files are saved (initially \"Result/\" directory)"
		
		print "\n (Source file format for automatic annotation)"
		print " To automatically annotate references, wrap <bibl></bibl> tags for each reference in source files."
		print " To automatically annotate notes, wrap <note></note> tags for each note in source files.\n"
		
		print " !! In case of extracting empty notes (corpus 2) because of less arranged tags, use at first :"
		print " \t $ python src/mypkg/format/noteExtractor.py <arg 1> \n\t <arg 1> is input directory where the data files are \n\t then use the printed result instead of the original files. \n"

	else:	
		if len(sys.argv) < 4:
			bilbo = Bilbo()
		else:
			bilbo = Bilbo(str(sys.argv[3]))

		
		if int(sys.argv[1]) == 1:
			bilbo.annotate(str(sys.argv[2]), "model/corpus1/", 1)
		elif int(sys.argv[1]) == 2:
			bilbo.annotate(str(sys.argv[2]), "model/corpus2/", 2)
		elif int(sys.argv[1]) == 11:
			bilbo.train(str(sys.argv[2]), "model/corpus1/", 1)
		elif int(sys.argv[1]) == 22:
			bilbo.train(str(sys.argv[2]), "model/corpus2/", 2)
		elif int(sys.argv[1]) == 21:
			bilbo.annotate(str(sys.argv[2]), "model/corpus2/", 2, 1)
			

		