
==============================================
 dossier config
==============================================

------------------------
 externalList
------------------------
FR:
Ce sont les fichiers permettant d'ameliorer l'annotation des lieu, nom et prenom.
Ce sont par exemple des listes de nom et prenom repandu dans le monde.

EN:
It is file that improve the annotation of place, name or forename
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

