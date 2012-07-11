
BILBO : Automatic annotation of bibliographic reference

(C) Copyright 2012 by Young-Min Kim and Jade Tavernier.
written by Young-Min Kim, modified by Jade Tavernier.

BILBO is an open source software for automatic annotation of bibliographic reference.
It provides the segmentation and tagging of input string. It is principally based on
Conditional Random Fields (CRFs), machine learning technique to segment and label
sequence data. As external softwares, Mallet is used for CRF learning and inference
and SVMlight is used for sequence classification. BILBO is licensed under a Creative
Commons Attribution-NonCommercial-ShareAlike 2.5 Generic License (CC BY-NC-SA 2.5).


==============================================
External tool installation
==============================================

------------------------
 Mallet
------------------------
http://mallet.cs.umass.edu/

------------------------
 SVM light
------------------------
http://svmlight.joachims.org/

------------------------
 SOAPpy
------------------------
$ cd dependencies/SOAP
$ sudo python setup.py install

------------------------
 fpconst
------------------------
$ cd dependencies/fpconst
$ sudo python setup.py install

==============================================
 Execute
==============================================

command:
$ cd bilbo
$ python src/mypkg/Main.py <arg 1> <arg 2> <arg 3>

	<arg 1> : integer
		 11 => train corpus 1, 
		 22 => train corpus 2,
		 1 => annotate reference corpus 1, 
		 2 => annotate reference corpus 2.
		 
	<arg 2> : string
		data file (training or test)
		
	<arg 3> : string
		output directory where the build result files are saved
		(initial : Result Directory ???)
		
==============================================
 Structure of directory
==============================================

------------------------
 src directory
------------------------
BILBO source code
	
------------------------
 dependencies directory
------------------------
External tools used by BILBO.
For example : mallet CRF or SVM light
	
------------------------
 doc directory
------------------------	
Document files to explain the architecture, operation and conception of BILBO

------------------------
 KB (Knowledge base) directory
------------------------	
config directory :
	Configuration file for BILBO

data directory :
	Training corpus

------------------------
 model directory
------------------------
Model created and used by BILBO

------------------------
 result directory
------------------------	
Annotated files



***********************
 For more information
***********************

==============================================
 Description
==============================================

Execute BILBO from command line :
Move to the directory BILBO then,
python src/mypkg/Main.py 

========================
 Configuration files
========================

------------------------
 externalList
------------------------
External proper noun lists used to improve proper noun tagging. Any proper noun list
can be used, for example, common name list in the world or world city list.

------------------------
 balise.txt
------------------------
This file contains the tag replacement information. Several tags in original training
data are too detailed, so they are replaced with simple tags. 
e.g. 'meeting' tag is replaced with 'booktitle'

FILE FORMAT
<tag name to be replaced> <space> <replacing tag name>
...


------------------------
 lexique.txt
------------------------
This file contains lexical features to be added to specific words. It is used by Rule
class. ???

FILE FORMAT

# <rule name> <space> <feature> <space> <feature> ….
word
word
...
# <rule name> <space> <feature> <space> <feature> ….
word
word
...

EXAMPLE :
# editor nonimpcap posseditor
ed
eds
ed.
eds.
-> if a word 'ed' is a input token, 'nonimpact' and 'posseditor' features are added.
??? how about capitalized characters?

------------------------
 features.txt
------------------------
This file contains basic information about feature names to be assigned and some rules
about tag names to be excluded or included. It is used by Extract class.

# features : valid features during data extraction
# nonLabels : invalid tags as label during data extraction. This is to eliminate some
meaningless tags in CRF learning. (*)importance 0:totally invalid tag, 1:can be 
attached to token when it does not have any tags attached.
# bookindicator : indicator words for book, journal, or etc. that includes the referred 
article.

Remark:
Other rules like 'bookindicator' can be added using same format with 'bookindicator'.

FILE FORMAT
# features
feature
feature
...
# nonLabels
tag <0 or 1>
tag <0 or 1>
...
# bookindicator
in
dans
...


========================
 Class
========================

------------------------
 Corpus
------------------------
class qui correspond a un repertoire contenant un corpus

attributs :
repertoire : chemin du repertoire
fichiers : liste des noms de fichier du corpus

methodes :


------------------------
 Fichier
------------------------
Class qui correspond à un fichier du corpus.

Attributs :
nom : nom du fichier
referencesCorpus1 : liste des references corpus 1 presentes dans ce fichier (objet listReference)

methodes :


------------------------
 listReference
------------------------
Class qui regoupe les references

Attributs :
listReferences : liste d'objet Reference
corpus : determine a quel corpus appartient cette liste de reference

methodes :

------------------------
 reference
------------------------
Class qui regoupe les mots d'une reference

Attributs :
num : numero de la reference
mots : list des mots contenu dans la reference : objet Mots
train : permet de savoir si cette reference doit etre utilisé pour l'apprentissage ou le test (1 : apprentissage, 0 : test, -1 : nonBibl)

methodes :

------------------------
 Mots
------------------------
Class qui regoupe les balises et les caracteristiques de chaque mot

Attributs :
balise : liste d'objet Balise
caracteristique : liste d'objet Caracteristique
nom : mot
item : indique si le mot fait partie d'une sous reference (0 : non, 1 : oui)

methodes :

------------------------
 Caracteristique et Balise
------------------------
Class qui contient le nom des balises ou caracteristique

Attributs :
nom : nom de la balise (ou caracteristique)

methodes :

=========
------------------------
 Nettoyer
------------------------
Class qui permet de nettoyer les références

Attributs :

methodes :
####
processing : cette methode nettoie les références et parcourt le xml pour créer les objets Balise, Mot, Réference... il retourne donc un objet Listreference
	parametre :
		fname : chemin et nom du fichier
		typeCorpus : c'est la balise de depart des références en fonction du type de corpus

####
_construireMot : permet de construire les objet Mots, Balise...
	parametre : 
		dicMots : tableau des mots qui contient leurs caracteritiques et leurs balises

------------------------
 Regle
------------------------
Class qui permet de modifier les caracteristique des mots en fonction des regles statique et des régles se trouvant dans le fichier de configuration : lexique.txt

Attributs :

methodes :
####
reorganizing : cette methode separe la ponctuation et ajoute les caracteristique en fonction des regles
	parametre :
		listReference : objet ListReference

------------------------
 Extract
------------------------
Class qui permet de modifier les balises des mots en fonction des regles statique et des régles se trouvant dans le fichier configuration : features.txt

Attributs :

methodes :
####
extractor : cette methode ajoute les balises en fonction des regles

	
------------------------
 Name
------------------------
Class qui permet de verifier si le nom ou le prenom correspond a un nom connu ou non en fonction des fichier se trouvant dans externalList

Attributs :

methodes :
####
searchName : cette methode regarde si le mot est present dans les listes, si oui alors elle ajoute les caracteristique correspondant : Namelist ou Surnamelist
	
------------------------
 Place
------------------------
Class qui permet de verifier si le mot correspond a un lieu connu ou non en fonction des fichier se trouvant dans externalList

Attributs :

methodes :
####
searchPlace : cette methode regarde si le mot est present dans les listes, si oui alors elle ajoute les caracteristique correspondant : Placelist
	
	
------------------------
 ProperList
------------------------
Class qui permet de verifier si le mot correspond a a une liste present dans le  connu ou non en fonction des fichier se trouvant dans externalList

Attributs :

methodes :
####
searchPlace : cette methode regarde si le mot est present dans les listes, si oui alors elle ajoute les caracteristique correspondant : Placelist
	
------------------------
 CRF
------------------------
Class qui permet de 
Attributs :

methodes :
####
extractor : cette methode ajoute les balises en fonction des regles
	
------------------------
 Bilbo
------------------------
Class qui permet de 

Attributs :

methodes :
####
extractor : cette methode ajoute les balises en fonction des regles
	

















