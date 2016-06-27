# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 17:57:50 2015

@author: Amal
"""

import subprocess
from bs4 import BeautifulSoup
import time
from lxml import etree
import os
import re
import sys

def bilbo():
    #command = "python /home/amal/Bureau/lrec_2016/demoLrec2016/bilbo/bilbo-master/src/bilbo/Main.py -L -t note -k all /home/amal/Bureau/lrec_2016/demoLrec2016/bilbo/bilbo-master/Data/test /home/amal/Bureau/lrec_2016/demoLrec2016/bilbo/bilbo-master/Result/test"
    command = "python ../../src/bilbo/Main.py -L -t note -k all ../../Data/test ../../Result/test"
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

def addBibl(path,ourFile):

    #read the result
    #bibl = open("/home/amal/Bureau/lrec_2016/demoLrec2016/bilbo/bilbo-master/Result/test/svm_predictions_all","r").readlines()
    #bibl_newfile = open("/home/amal/Bureau/lrec_2016/demoLrec2016/compareSVM/"+ourFile,"w")
    bibl = open("../../Result/test/svm_predictions_all","r").readlines()
    bibl_newfile = open("../../../../compareSVM/"+ourFile,"w")

    dataToShow=""

    content=open(path+"/"+ourFile,'r').read()
    soup1 = BeautifulSoup(content)
    texts = soup1.findAll("p") 
    i=-1
    x=-1
    new_bibl=["" for s in range(len(bibl))]
    string=""
    #print str(len(bibl)) + "-----------------------------------------------------------------"
    #fix our predicted list
    #
    for x in range(len(bibl)-1):
      
    	#for text in texts:
	x=x+1
	#print bibl[x][0]
 	if (x+2 < len(bibl) and x-2 >=0) and (bibl[x][0] == "0" and bibl[x-1][0] == "1" and bibl[x-2][0] == "1" and bibl[x+2][0] == "1" and bibl[x+1][0] == "1"):
		new_bibl[x] = "1"
	elif (x+2 < len(bibl) and x-2 >=0) and (bibl[x][0] == "1" and bibl[x-1][0] == "0" and bibl[x-2][0] == "0" and bibl[x+2][0] == "0" and bibl[x+1][0] == "0"):
		new_bibl[x] = "0"
	#elif bibl[x][0] == "1" and (len(text.getText()) < 50 or len(text.getText()) > 300):
		#new_bibl[x] = "0"
	else:
    		new_bibl[x] = bibl[x][0]

    for f in range(len(new_bibl)):	
	string = string + new_bibl[f] + "\n"
    bibl_newfile.write(string)
    bibl_newfile.close()
	
    #
    #look for the biggest list of ones, it should seperated from other ones by many zeros
    #
    a_max=0
    z_max=0
    taille_max=0

    a=0
    z=0
    taille=0

    firstPass=True
    countOfP=0
    firstFilled=False

    for y in range(len(new_bibl)):
	if new_bibl[y] == "1":
		if firstPass==True:
			a=y
			firstPass=False
			countOfP=0
                        taille=taille+1
			if firstFilled==False:
				a_max=a
				firstFilled=True	
		else:
			z=y
                        taille=taille+1
			countOfP=0
			
	elif new_bibl[y] == "0": 
		if countOfP < 2 :
			countOfP=countOfP+1
		else:
			firstPass=True
			countOfP=0
			taille=0

    	if taille>taille_max:
		taille_max=taille
		a_max=a
		z_max=z
   
  
    content=open(path+"/"+ourFile,'r').read()
    soup = BeautifulSoup(content)
    texts = soup.findAll("p") 
    i=-1
    

    for text in texts:	
        i=i+1
	if i<=len(new_bibl):
		if i == a_max:
			text.name = 'firstBibl'
			dataToShow =  dataToShow + "<bibl>"+ re.sub('<[^>]*>', '', text.text) + "</bibl>\n"
		elif i == z_max+1:
			text.name = 'lastBibl'
			dataToShow = dataToShow + "<bibl>"+ re.sub('<[^>]*>', '', text.text) + "</bibl>\n"
		#elif new_bibl[i]=="1":
		elif i > a_max and i <= z_max:
			text.name = 'bibl'
			dataToShow = dataToShow + "<bibl>"+ re.sub('<[^>]*>', '', text.text) + "</bibl>\n"
    '''
    content=open("getDataSolr/"+ourFile,'r').read()
    soup = BeautifulSoup(content)
    texts = soup.findAll("p") 
    i=-1	

    for text in texts:
        i=i+1
	
	if bibl[i][0]=="1":
		text.name = 'bibl'
    '''

    newdata = str(soup.prettify)
    #temp_file = open("/home/amal/Bureau/lrec_2016/demoLrec2016/files_RES/"+ourFile,"w")
    temp_file = open("../../../../files_RES/"+ourFile,"w")
    temp_file.write(newdata)
    temp_file.close()

    #show_file = open("/home/amal/Bureau/lrec_2016/demoLrec2016/bilbo/bilbo-master/src/web-api/tmp/out/"+ourFile,"w")
    show_file = open("tmp/out/"+ourFile,"w")
    dataToShow = dataToShow.encode('utf-8')
    show_file.write(dataToShow)
    show_file.close()

#After bilbo .. check who's have autor and title
def fileProcessing(path,ourFile):


    #File####################################################################################
    content=open(path+"/"+ourFile,'r').read()
    soup = BeautifulSoup(content)
    texts = soup.findAll("p")   

    #look for biblio
    #texts.next()
    #continue
    
    #pred_file=open("/home/amal/Bureau/lrec_2016/demoLrec2016/bilbo/bilbo-master/Result/test/svm_predictions_all", "w")
    pred_file=open("../../Result/test/svm_predictions_all", "w")

    for text in texts:

                #send a part of the file in text.txt
                divFile = open("../../Data/test/text.txt","w") 

		myText = re.sub('<[^>]*>', '', text.getText())
 		if len(text.getText()) > 20 and len(text.getText()) < 500 :
                	divFile.write("<note>"+str(text.getText().encode('utf-8'))+"</note>")
		else:
			divFile.write("<note> not bibliographie </note>")

                divFile.close()
		
           	bibl = []

                #call bilbo to detect the bibl parts
                bilbo()
                time.sleep(1)

    pred_file.close()
    #sys.stdout.flush()

    ### here  the addBibl ...
    addBibl(path,ourFile)


################################################# 
#fileProcessing("files","files_test.xml") 
#################################################

    
