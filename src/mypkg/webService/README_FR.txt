##########################

installer outils externe :

fpconst:
$ cd src/dependencies/fpconst-0.7.2
$ python setup.py install

pyXML:
$ cd src/dependencies/PyXML-0.8.4
$ python setup.py install

SOAPpy:
$ cd src/dependencies/SOAPpy-0.12.0
$ python setup.py install

more information:
http://diveintopython.adrahon.org/soap_web_services/install.html#d0e29990

###############################
Mise en marche

modifier les chemins présents dans le fichier WebService.py :
	dossier_fichier_out = # dossier sortie : resultat
	dossier_fichier_in =  # dossier ou l'on crée le fichier à annoter (ce dossier doit contenir que les fichier a annoter)
	dossier_code = 		  # dossier ou l'on retrouve le code objet python de BILBO:  dossier bilbo


###############################
SERVICES

********
annotateText : permet d'annoter une référence
Arguments :
	type : int : type de corpus 1, 2 ou 3
	texte : string : le texte est concideré comme une référence

exemple : annotateText(1, "référence")


********	
annotateFile : permet d'annoter les références d'un fichier tei
arguments :
	type : int : type de corpus 1, 2 ou 3
	texte : string : texte complet d'un fichier xml tei

exemple : annotateFile(1, "xml - tei")


********	
annotateAllFiles : permet d'annoter plusieur fichier xml - tei
Arguments :
	type : int : type de corpus 1, 2 ou 3
	texte : tableau - string : tableau composé de plusieurs texte complet de fichier xml a annoté
	
exemple : annotateAllFiles(1, "[xml - tei- 1, xml - tei - 2, ...]")