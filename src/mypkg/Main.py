'''
Created on 19 avr. 2012

@author: jade
	argv[1] => repertory with file to annotate 
	argv[2] => repertory where build result file (initial : Result)

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
	prof = hotshot.Profile('Result/perf.prof')
	prof.start()
	

	if len(sys.argv) < 2:
		print "argument:\n1 : 1 => annote corpus 1, 2 => annote corpus 2, 11 => train corpus 1, 22 => train corpus 2,\n2 : repertory with file to annotate,\n3 : repertory where build result file (initial : Result)\n"
	else:	
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
	prof.stop()
	prof.close()
	#	bilbo.annoter("/Users/jade/Documents/jade/labo/comparaison_bilbo/analyse/repertoire/Niveau1/originaux/etnografica-869.xml")
		#corpus = Corpus("/Applications/XAMPP/xamppfiles/htdocs/annotationSave/XML_annotated2")
		#corpus.extraireCorpus1()
		#fichier = Corpus("/Applications/XAMPP/xamppfiles/htdocs/WebService/code/fichierRes/fichier_a_annoter.xml")
		