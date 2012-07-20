##########################

installer outil :

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