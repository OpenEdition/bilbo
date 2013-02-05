
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
 Wapiti
------------------------
http://wapiti.limsi.fr/

------------------------
 SVM light
------------------------
http://svmlight.joachims.org/

------------------------
 lxml for BeautifulSoup
------------------------
http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

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

Usage: python src/bilbo/Main.py [options] <input data folder> <output data folder>
e.g. training: python src/bilbo/Main.py -T -t bibl Data/train/ Result/train/
     labeling: python src/bilbo/Main.py -L -t bibl -d Data/test/ Result/test/
Options
(mode)
  -T : --Training
	 Bilbo training, default='False'
  -L : --Labeling
	 Data labeling, default='False'
(training, labeling)
  -t : --typeref <string>
	 Input reference type
	  bibl => bibliography with a heading, wrapped by <bibl></bibl> (default)
	  note => notes wrapped by <note></note>
	  impl => implicit citations
  -i : --informat <string>
	 Input reference format
	  tei => xml following tei guidelines including manual annotation (default)
	  xml => simple xml without tree in manual annotation
	  plain => plain text (for labeling only)
  -m : --model <string>
	 Bilbo model name, default='revues'
	 create a folder under "model/" folder and save models when training / load models when labeling
  -g : --gradetag <string>
	 Grade of tag detail when using tei (option -f or -o)
	  simple => simple title and biblscope (default)
	  detail => detailed title and biblscope
  -k : --keeptmp <string>
	 Decide which temp files are kept, among those created for svm crf training or test
	  none => keep nothing (default)
	  primary => keep primary temp files
	  all => keep all files
  -s : --svmfilt
	 Training a svm model or classifying notes to filter out non-bibliographical notes, default='False'
(labeling)
  -o : --outformat <string>
	 Output data format
	  tei => xml following tei guidelines (default)
	  xml => simple xml 
  -d : --doi
	 Digital object identifier (doi) extraction via crossref site, default='False'
  -e : --exterdata
	 Labeling data different from training set. Do not use svm filtering when using this option. default='False'
Arguments
  arg1 : <string>
	 input data folder where the data files are (training or labeling)
  arg2 : <string>
	 output data folder where the result files are saved


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


------------------------
 others.txt
------------------------
This file contains other configurations about TEI extraction (username of crossref site)
and TEI output format. As Bilbo label reference with its own tags, a change rule from
own tags to TEI is necessary. It is used in the functions of identifier.py called from
File::buildReferences.



========================
 Class
========================


------------------------
 Bilbo
------------------------
A machine Bilbo that trains a CRF (and a SVM) model and automatically labels new references.
Created in Main.py
Description in doc/documentation/Bilbo.html

------------------------
 CRF
------------------------
CRF object is created in a Bilbo object
CRF model learning and test
Description in doc/documentation/CRF.html

------------------------
 Corpus
------------------------
A corpus containing a set of training (or test) references.
Description in doc/documentation/CRF.html

------------------------
 File
------------------------
A file calss containing all references in a file
Description in doc/documentation/File.html


------------------------
 Extract
------------------------
A class to extract training and test data according to a set of predefined criteria
Base class of Extract_crf and Extract_svm
Description in doc/documentation/Extract.html

------------------------
 Extract_crf
------------------------
A class to extract training and test data for CRF
Sub class of Extract
Description in doc/documentation/Extract_crf.html



------------------------
 ListReference
------------------------
This class contains references.

Attributes :
listReferences : Reference object list
corpus : data type indicator

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










