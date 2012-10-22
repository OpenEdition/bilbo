
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
		 1 => test reference corpus 1, 
		 2 => test reference corpus 2.
		 21 => test corpus 2 with external data (If data is not from CLEO).
		 
	<arg 2> : string
		input directory where the data files are (training or test)
		
	<arg 3> : string
		output directory where the build result files are saved
		(initial : "Result" directory)
	(Source file format for automatic annotation)
 	To automatically annotate references, wrap <bibl></bibl> tags for each reference in source files.
 	To automatically annotate notes, wrap <note></note> tags for each note in source files.

		
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
class. 

FILE FORMAT

# <rule name> <space> <feature> <space> <feature> É.
word
word
...
# <rule name> <space> <feature> <space> <feature> É.
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
This class corresponds to a directory containing a corpus.

Attributes :
repertoire : directory path
fichiers : list of filenames in a corpus

Methods :

------------------------
 File
------------------------
This class corresponds to a file in a corpus.

Attributes :
nom : name of the file 
referencesCorpus1 : list of level 1 references included in the file (listReference object)

Methods :

------------------------
 ListReference
------------------------
This class contains references.

Attributes :
listReferences : Reference object list
corpus : an indicator determine a quel corpus appartient cette liste de reference ????? level

Methods :

------------------------
 Reference
------------------------
This class contains words in a reference

Attributes :
num : reference number 
word : word list included in the reference - Word object
train : an indicator if this reference should be used for training or test (1 : learning, 0 : test, -1 : nonBibl)

Methods :

------------------------
 Word
------------------------
This class contains tags and each word's features.

Attributes :
tag : Balise object list
feature : Feature object list
nom : word name
item : indicator of sub-reference (0 : no, 1 : yes)

Methods :

------------------------
 Feature and Balise
------------------------
These classes contain feature name or tag name.

Attributes :
nom : Feature (or tag) name

Methods :

=========
------------------------
 Clean
------------------------
This class cleans input references

Attributes :

Methods :
####
processing : this method cleans references and reads the xml files to extract Balise, Word, Reference objects etc. at the end it returns a ListReferences object.
	parameter :
		fname : path and file name
		typeCorpus : corpus type indicator coming from references

####
__buildWords : this method constructs Word, Balise objects etc.
	parameter : 
		dicWord : word dictionaries containing their features and tags: [word, caracteristique] & [word, balise]

------------------------
 Rule
------------------------

This class extracts word features using some static rules and other rules written in a configuration file : lexique.txt

Attributes :

Methods :
####
reorganizing : this method tokenizes input words by separating punctuation and extract features from rules.
	parameter :
		listReference : ListReference object

------------------------
 Extract
------------------------
This class modifies tags and features using some detailed static rules and other rules written in a configuration file : features.txt

Attributes :

Methods :
####
extractor : this method add tags with given rules
	
------------------------
 Name
------------------------
This class verifies if a given word corresponds to a surname or a forename in a name list in the "externalList" directory.

Attributes :

Methods :
####
searchName : this method checks if the entered word is found in the name list and if yes, it adds a feature : SURNAMELIST or FORENAMELIST

------------------------
 Place
------------------------
This class verifies if a given word corresponds to a place in a list in the "externalList" directory.

Attributes :

Methods :
####
searchPlace : this method checks if the entered word is found in the place list and if yes, it adds a feature : PLACELIST
	
------------------------
 ProperList
------------------------
This class verifies if a given word corresponds to a proper noun in a list in the "externalList" directory.

Attributes :

Methods :
####
searchPlace : this method checks if the entered word is found in the place (for the moment) list and if yes, it adds a feature : PLACELIST (for the moment)

------------------------
 CRF
------------------------
This class 

Attributes :

Methods :
####
extractor : this method add tags with given rules ...
	
------------------------
 Bilbo
------------------------
This class 

Attributes :

Methods :
####
extractor : this method add tags with given rules ...
	








