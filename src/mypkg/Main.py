'''
Created on 19 avr. 2012

@author: Young-min Kim, Jade Tavernier
	argv[1] => 1 => annote corpus 1, 2 => annote corpus 2, 11 => train corpus 1, 22 => train corpus 2
	argv[2] => directory with file to annotate 
	argv[3] => directory where build result file (initial : Result)

'''
import sys
import os

'''
ajoute au path le package
'''
directoryTab = os.getcwd().replace("\\", "/").split("/")
last = directoryTab.pop()
if last == "bilbo":
	directoryTab.append(last)
	directoryTab.append("src")
	directory = "/".join(directoryTab)
	sys.path.append(directory)
else:
	print "erreur: veuillez lancer le programme depuis le directory bilbo"
	

from mypkg.bilbo.Bilbo import Bilbo
import hotshot

if __name__ == '__main__':
	pass


	if len(sys.argv) < 2:

		print "$ python src/mypkg/Main.py <arg 1> <arg 2> <arg 3>"
		print " <arg 1> : integer \n\t 11 => train corpus 1, \n\t 22 => train corpus 2, \n\t 1 => annotate reference corpus 1, \n\t 2 => annotate reference corpus 2, \n\t 21 => annotate corpus 2 with external data."
		print " <arg 2> : string \n\t input directory where the data files are (training or test)"
		print " <arg 3> : string \n\t output directory where the built result files are saved (initially \"Result/\" directory)"

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
			#bilbo.train("KB/data/corpus1/XML_annotated2", "model/corpus1/", 1)
			bilbo.train(str(sys.argv[2]), "model/corpus1/", 1)
		elif int(sys.argv[1]) == 22:
			#bilbo.train("KB/data/corpus2/alldata_added", "model/corpus2/", 2)
			bilbo.train(str(sys.argv[2]), "model/corpus2/", 2)
		elif int(sys.argv[1]) == 21:
			bilbo.annotate(str(sys.argv[2]), "model/corpus2/", 2, 1)
			

	#	bilbo.annoter("/Users/jade/Documents/jade/labo/comparaison_bilbo/analyse/repertoire/Niveau1/originaux/etnografica-869.xml")
		#corpus = Corpus("/Applications/XAMPP/xamppfiles/htdocs/annotationSave/XML_annotated2")
		#corpus.extraireCorpus1()
		#fichier = Corpus("/Applications/XAMPP/xamppfiles/htdocs/WebService/code/fichierRes/fichier_a_annoter.xml")
		