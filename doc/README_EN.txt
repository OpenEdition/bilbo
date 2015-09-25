
BILBO : Automatic reference labeling

(C) Copyright 2013 by Young-Min Kim and Jade Tavernier.
written by Young-Min Kim, modified by Jade Tavernier.

BILBO is an open source software for automatic annotation of bibliographic reference.
It provides the segmentation and tagging of input string. It is principally based on
Conditional Random Fields (CRFs), machine learning technique to segment and label
sequence data. As external softwares, Wapiti is used for CRF learning and inference
and SVMlight is used for sequence classification. BILBO is is released under the terms
of the GPL version 2.


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

==============================================
 Execute
==============================================

command:
$ cd bilbo
$ python src/bilbo/Main.py 		(help full ver.)
$ python src/bilbo/Main.py -h 	(help simple ver.)


Usage: python src/bilbo/Main.py [options] <input data folder> <output data folder>
e.g. training: python src/bilbo/Main.py -T -t bibl Data/train/ Result/train/
		python src/bilbo/Main.py -i xml -T -t impl TrainRefImplBibl/ Result/train/
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
	  tei => xml following tei guidelines including manual annotation (defalut)
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
  -v : --validatexml <string>
	 Decide if we validate files, 
	  none => do not validate (default)
	  input => validate input files with tei_all.dtd
	  output => validate output files with tei_openedition3.xsd
	  all => validate input and output files
  -s : --svmfilt
	 Training a svm model or classifying notes to filter out non-bibliographical notes, default='False'
  -u : --undopuncsep
	 Undo punctuation separation, default='False'
(labeling)
  -o : --outformat <string>
	 Output data format
	  tei => xml following tei guidelines (default)
	  xml => simple xml
	  simple => only labeled references without article contents or original tags
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

validation directory :
	xml validation files

------------------------
 model directory
------------------------
Model created and used by BILBO

------------------------
 result directory
------------------------	
Result files



***********************
 For more information
***********************

==============================================
 Description
==============================================



========================
 Configuration files
========================

------------------------
 externalList directory
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
(tag name to be replaced) (space) (replacing tag name)
...


------------------------
 lexique.txt
------------------------
This file contains lexical features to be added to specific words. It is used by Rule
class. There are two types of lexical features : [including] and [matching]
[including] means check if the corresponding word is INCLUDED in the input token
[matching] means check if the corresponding word is exactly matching the input token
e.g. (January), string should de verified as [including] feature     

FILE FORMAT
[including]
# (rule name) (space) (feature) (space) (feature) É.
word
word
...
# (rule name) (space) (feature) (space) (feature) É.
word
word
...
[matching]
# (rule name) (space) (feature) (space) (feature) É.
word
word
...
# (rule name) (space) (feature) (space) (feature) É.
word
word
...

EXAMPLE :
[including]
# editor nonimpcap posseditor
ed
eds
ed.
eds.
-> if a word 'ed' is a input token, 'nonimpcap' and 'posseditor' features are added.


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
File::buildReferences. Lines starting with # are ignored.
[tei] is for replacement of tags for the rewrite of result in TEI format
  (old tag) = (new tag)
  if new tag is NONE, it means that the corresponding old tag will be ignored in TEI format


FILE FORMAT
[tei]
nonbibl = NONE
nolabel = NONE
bookindicator = NONE
w = NONE
#surname = 
#forename =
#publisher = 
#abbr
#date
title_m = title level="m"
title_a = title level="a"
title_j = title level="j"
title_t = title level="a"
title_u = title level="u"
title_s = title level="s"
biblscope_pp = biblScope unit="pp"
biblscope_i = biblScope unit="issue"
biblscope_v = biblScope unit="vol"
biblscope_pa = biblScope unit="part"
biblscope_c = biblScope unit="chap"
biblscope = NONE
É



------------------------
 pattern_ref
------------------------
Wapiti pattern configuration for feature extraction




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
Description in doc/documentation/format/CRF.html

------------------------
 SVM
------------------------
SVM object is created in a Bilbo object
SVM model learning and test
Description in doc/documentation/format/SVM.html

------------------------
 Corpus
------------------------
A corpus containing a set of training (or test) references.
Description in doc/documentation/reference/Corpus.html

------------------------
 File
------------------------
A file class containing all references in a file
Description in doc/documentation/reference/File.html

------------------------
 Extract
------------------------
A class to extract training and test data according to a set of predefined criteria
Base class of Extract_crf and Extract_svm
Description in doc/documentation/format/Extract.html

------------------------
 Extract_crf
------------------------
A class to extract training and test data for CRF
Sub class of Extract
Description in doc/documentation/format/Extract_crf.html

------------------------
 Extract_svm
------------------------
A class to extract training and test data for SVM
Sub class of Extract
Description in doc/documentation/format/Extract_svm.html

------------------------
 Clean
------------------------
A class that tokenizes xml input data. Navigates the xml tree and extracts tokens, features and labels.
It concerns the first step of tokenization such that words are separated by whitespace but not by punctuation 
marks. A clean object is created in a File object ("extract" method).
Description in doc/documentation/format/Clean.html

------------------------
 CleanCorpus1
------------------------
A class that tokenizes xml input data for corpus 1 (references).
Sub class of Clean
Description in doc/documentation/format/CleanCorpus1.html

------------------------
 CleanCorpus2
------------------------
A class that tokenizes xml input data for corpus 2 (notes).
Sub class of Clean
Description in doc/documentation/format/CleanCorpus2.html

------------------------
 Rule
------------------------
A class that reorganizes tokens according to the predefined rules. ("lexique.txt" is loaded)
Especially the punctuation marks are separated and new Word objects are created.
Features about initial expression, capitalized token etc. are verified and attached.
Description in doc/documentation/format/Rule.html

------------------------
 ListReferences
------------------------
A class containing a list of reference objects and corpus type information.
Description in doc/documentation/format/ListReferences.html

------------------------
 Reference
------------------------
A class corresponding to a reference. It contains, word objects. 
Reference object is first created in CleanCorpus1 and CleanCorpus2.
Description in doc/documentation/format/Reference.html

------------------------
 Word
------------------------
A class corresponding to a word in a reference. It contains word name, features, tags etc.
Word object is first created in CleanCorpus1 and CleanCorpus2.
Description in doc/documentation/format/Word.html

------------------------
 Feature and Balise
------------------------
These classes contain feature name or tag name.


=========
	
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



========================
 OTHERS
========================

------------------------
 Main.py
------------------------

Main creates Bilbo object to train or to label reference


------------------------
 utils.py
------------------------

utils.py provides APIs to process simple string for labeling.
It also contains default option setting function, which is called in main.

There are two functions that we can execute :
- simpleLabeling : for labeling with a simple CRF model (having less number of labels)
- detailLabeling : for labeling with a detailed CRF model (having labels for TEI)

You can test simply this function at the directory src.

e.g. Labeling a reference
$cd src
$python
>>> from bilbo.utils import *
>>> detailLabeling("Y.-M. KIM et al., An Extension of PLSA for Document Clustering, In Proceedings of ACM 17th Conference on Information and Knowledge Management, 2008.")

Result
First author :   KIM  	Start of title :   An Extension of PLSA for Document Clustering 
DOI : 10.1145/1458082

'<listBibl>\n<bibl> <author><forename>Y.-M.</forename> <surname>KIM</surname></author> et al., <title level="a">An Extension of PLSA for Document Clustering</title><idno type="DOI">http://dx.doi.org/10.1145/1458082</idno>, <meeting>In Proceedings of ACM 17th Conference on Information and Knowledge Management</meeting>, <date>2008</date>. </bibl>\n</listBibl>\n'

The result is also saved in a file tmp.xml in the current directory.
We can also test it in Main.py (an example in comments in this file)

To label a note, we just add "note" as second parameter.
e.g.
>>> detailLabeling("For more information see, Y.-M. KIM et al., An Extension of PLSA for Document Clustering, In Proceedings of ACM 17th Conference on Information and Knowledge Management, 2008.", "note")
