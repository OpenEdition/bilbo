==============================================
Install tools
==============================================

------------------------
 mallet
------------------------

------------------------
 SVM light
------------------------

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
 Launch
==============================================

command:
$ cd bilbo
$ python src/mypkg/Main.py <arg 1> <arg 2> <arg 3>

	<arg 1> : integer
		 1 => annotate reference corpus 1, 
		 2 => annotate reference corpus 2, 
		 11 => train corpus 1, 
		 22 => train corpus 2,
		 
	<arg 2> : string
		repertory with annotate file,
		
	<arg 3> : string
		repertory where build result file (initial : Repertory Result)
		
==============================================
 Structure of directory
==============================================

------------------------
 src directory
------------------------
Its BILBO code
	
------------------------
 dependencies directory
------------------------
Its tools used by BILBO.
For exemple : mallet CRF or SVM light
	
------------------------
 doc directory
------------------------	
Its document file to explain architecture, operation and conception of BILBO

------------------------
 KB (Knowledge base) directory
------------------------	
config directory :
	configuration file for BILBO

data directory :
	Train corpus

------------------------
 model directory
------------------------
model used and create by BILBO

------------------------
 result directory
------------------------	
annotated file

