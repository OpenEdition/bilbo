'''
Created on 19 avr. 2012

@author: Young-min Kim, Jade Tavernier
	argv[1] => 1 => annote corpus 1, 2 => annote corpus 2, 11 => train corpus 1, 22 => train corpus 2
	argv[2] => repertory with file to annotate 
	argv[3] => repertory where build result file (initial : Result)

'''
import sys
import os

'''
ajoute au path le package
'''
repertoireTab = os.getcwd().replace("\\", "/").split("/")
last = repertoireTab.pop()
if last == "bilbo":
	repertoireTab.append(last)
	repertoireTab.append("src")
	repertoire = "/".join(repertoireTab)
	sys.path.append(repertoire)
else:
	print "erreur: veuillez lancer le programme depuis le repertoire bilbo"
	

from mypkg.bilbo.Bilbo import Bilbo
import hotshot

if __name__ == '__main__':
	pass


	if len(sys.argv) < 2:
<<<<<<< HEAD
		print "argument:\n1 : 1 => annote corpus 1, 2 => annote corpus 2, 11 => train corpus 1, 22 => train corpus 2,\n2 : repertory with file to annotate,\n3 : repertory where build result file (initial : Result)\n"
	else:
=======
		print "$ python src/mypkg/Main.py <arg 1> <arg 2> <arg 3>"
		print " <arg 1> : integer \n\t 11 => train corpus 1, \n\t 22 => train corpus 2, \n\t 1 => annotate reference corpus 1, \n\t 2 => annotate reference corpus 2."
		print " <arg 2> : string \n\t input directory where the data files are (training or test)"
		print " <arg 3> : string \n\t output directory where the built result files are saved (initially \"Result/\" directory)"
	else:	
>>>>>>> b27a639e8c80a7103e332e88466e22059b3b7e21
		if len(sys.argv) < 4:
			bilbo = Bilbo()
		else:
			bilbo = Bilbo(str(sys.argv[3]))
		
		if int(sys.argv[1]) == 1:
			bilbo.annoter(str(sys.argv[2]))
		elif int(sys.argv[1]) == 2:
			bilbo.annoterCorpus2(str(sys.argv[2]))
		elif int(sys.argv[1]) == 11:
			bilbo.apprentissage("KB/data/corpus1/XML_annotated2")
		elif int(sys.argv[1]) == 22:
			bilbo.apprentissageCorpus2("KB/data/corpus2/alldata_added")

	#	bilbo.annoter("/Users/jade/Documents/jade/labo/comparaison_bilbo/analyse/repertoire/Niveau1/originaux/etnografica-869.xml")
		#corpus = Corpus("/Applications/XAMPP/xamppfiles/htdocs/annotationSave/XML_annotated2")
		#corpus.extraireCorpus1()
		#fichier = Corpus("/Applications/XAMPP/xamppfiles/htdocs/WebService/code/fichierRes/fichier_a_annoter.xml")
		