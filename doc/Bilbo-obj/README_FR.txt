BILBO : Automatic annotation of bibliographic reference

(C) Copyright 2012 by Young-Min Kim and Jade Tavernier.
written by Young-Min Kim, modified by Jade Tavernier.

BILBO et un logiciel open source pour annoter automatiquement des références bibliographique.

BILBO is an open source software for automatic annotation of bibliographic reference.
Il fait une segmentation et l'etiquettage d'une chaine. Il est principalement basé sur Conditional Random Fields (CRFs),
technique d'apprentissage pour segmenter et etiquetter des séquences de données.
Les logiciels externe, Mallet est utilisé pour CRF apprentissage et SVMLight est utilisé pour la classification.
BILBO est distribué sous license Commons Attribution-NonCommercial-ShareAlike 2.5 Generic License (CC BY-NC-SA 2.5).


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
		 11 => corpus d'apprentissage 1, 
		 22 => corpus d'apprentissage 2,
		 1 => annoter reference corpus 1, 
		 2 => annoter reference corpus 2.
		 
	<arg 2> : string
		repertoire fichier de donnée (apprentissage ou test)
		
	<arg 3> : string
		repertoire de sortie où les fichiers annotés sont sauvegardé
				(initial : Result Directory ???)
		
==============================================
 Structure of directory
==============================================

------------------------
 src directory
------------------------
code source BILBO
	
------------------------
 dependencies directory
------------------------
outils externe utilisé par BILBO.
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

Lancer en ligne de commande:

se placer dans le dossier bilbo puis:
python src/mypkg/Main.py 

==============================================
 dossier config
==============================================

------------------------
 externalList
------------------------
FR:
Ce sont les fichiers permettant d'ameliorer l'annotation des lieux, nom et prenom.
Ce sont par exemple des listes de nom et prenom repandu dans le monde.

EN:
it is a file that improve the annotation of place, name or forename
for exemple one list of forename and surname known around the world
------------------------
 balise
------------------------
FR:
Ce fichier est necessaire pour la mise en forme "normalisé" des fichiers
Permet de remplacer certain nom de balise par un autre (par exemple on remplace la balise meeting par booktitle)

EN:
This file is necessary for shaping "normalyze" files
is used to replace some tag name for another (for exmple to replace the meeting tag for booktitle tag) 

FORMAT FICHIER
<nom balise> <espace> <nouveau nom de balise>
...

------------------------
 lexique
------------------------
FR:
Ce fichier est necessaire pour ajouter des caracteristiques à certains mots s'ils repondent aux regles presentes dans ce fichier.
Il est utilisé par la classe Regle

EN
This file is used for add features to some words, if words meet the rules presented in this file.
It is used by a Rule class 

FORMAT FICHIER
# <nom regle> <espace> <caracteristique> <espace> <caracteristique2> ....
regle 1
regle 2
...
# <nom regle numero 2> <espace> <caracteristique> <espace> <caracteristique2> ....
regle 1 
...

EXEMPLE :

	# editor nonimpcap posseditor
	ed
	eds
	ed.
	eds.
Donc si le mot et "ed" alors on ajoutera les caracteristique nonimpcap et posseditor a ce mot.

------------------------
 features
------------------------
FR:
Ce fichier regroupe les caracteristiques générale permettant d'attribuer un nom de balise a un mot en fonctions des regles.
il est utilisé par la classe Extract


feature : permet de determiner les caracteristiques que l'on doit concerver pour la phase d'apprentissage
nonLabels : permet de determiner les balises correspondant a des nonLabels (nonLabel : des balises pas importante)
			importance : determine si la balise peut etre une balise attribué à un mot, 0 non et 1 oui(peut etre attribué)
bookindicator : permet de lister les mots qui peuvent montrer que l'on est dans bookindicator 

Remarque:
Des regle comme bookindicator peuvent etre ajouter a la suite de se fichier sous le meme format que bookindicator

EN:
This file includes general features to assign a tag name has a word in fonction the rules
It is used by Extract Class

feature : used to determinate features that schould be saved fro a train
nonLabels : used to determinate tags corresponding nonLabel (nonLabel : it is a tag not used)
		importance: determined if tag can be tag assigned to a word, 0 non an 1 yes
bookindicator : ised to list they words wich may show that one is in bookindicator

FORMAT FICHIER
# features
features1
features2
...
# nonLabels
balise1 <importance 0 ou 1>
balise2 <importance 0 ou 1>
...
# bookindicator
mot
mot
in
dans
...


==============================================
 Class
==============================================

------------------------
 Corpus
------------------------
class qui correspond a un repertoire contenant un corpus

attributs :
repertoire : chemin du repertoire
fichiers : liste des noms de fichier du corpus

methodes :


------------------------
 File
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
 Word
------------------------
Class qui regoupe les balises et les caracteristiques de chaque mot

Attributs :
balise : liste d'objet Balise
caracteristique : liste d'objet Caracteristique
nom : mot
item : indique si le mot fait partie d'une sous reference (0 : non, 1 : oui)

methodes :

------------------------
 Feature et Balise
------------------------
Class qui contient le nom des balises ou caracteristique

Attributs :
nom : nom de la balise (ou caracteristique)

methodes :

=========
------------------------
 Clean
------------------------
Class qui permet de nettoyer les références
deux class herite:
	- CleanCorpus1
	- CleanCorpus2
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
 Rule
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
Deux class qui herite :
	=> ExtractCorpus1 
	=> ExtractCorpus2

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
Class qui permet de générer les fichiers pour l'outils CRF
Attributs :

methodes :
####
extractor : cette methode ajoute les balises en fonction des regles
	
------------------------
 Bilbo
------------------------
Class qui permet de lancer l'annotation ou l'apprentissage

Attributs :

methodes :
####

	








