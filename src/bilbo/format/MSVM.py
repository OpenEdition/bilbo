# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Wed Nov 18 15:02:43 2015

@author: ollagnier
"""

from codecs import open
from subprocess import PIPE
import glob
import os.path
import ntpath
import sys,re
import time
import random
import subprocess, os
import shutil

before = time.clock()

class MSVM(object):

    def __init__(self, dirResult, options={}):
		"""
		Attributes
		----------
		dirResult : string
			directory for result files
		"""
		self.dirResult = dirResult
		self.options = options
		main = os.path.realpath(__file__).split('/')
		self.rootDir = "/".join(main[:len(main)-4])

    def delete_Tag(self, folder):
	list_files = glob.glob (folder+'*/*')
	for file in list_files :
		with open(file, 'r', encoding='utf8') as f:
			for line in f:
				line = re.sub('<[^<]+?>', '', line)
				folderResult =  self.dirResult+f.name
				folderResult = folderResult.split('/')
				pathFolderResult = '/'.join(folderResult[:5])
				if not os.path.exists(pathFolderResult+'/'):
                                	os.makedirs(pathFolderResult+'/')
				output = open(pathFolderResult+'/'+folderResult[5],'w', encoding = 'utf8')
                                output.write(line)
                                output.close()
	    
    def createFolder(self, folderInit, folderResult):
	list_files = glob.glob (folderInit+'*')
	newpath = folderResult 
	if os.path.exists(newpath):
		shutil.rmtree(newpath)	
	os.makedirs(newpath)
	j = 0
	for file in list_files :
		j = j + 1
		with open(file, 'r', encoding='utf8') as f:
			folderPath = 'class_'+str(j)
			classPath = newpath+folderPath
			if not os.path.exists(classPath):
                		os.makedirs(classPath)
			i=0
			for line in f:
				if line.startswith('<impl>'):
					output = open(classPath+'/'+str(i)+".txt",'w', encoding = 'utf8')
					output.write(line)
					output.close()
				i=i+1
    
    def runTrain(self, directoryModel):
        dependencyDir = os.path.join(self.rootDir, 'dependencies')
        command = dependencyDir+'/MSVMpack1.5/trainmsvm '+self.dirResult+'class_mix.train '+directoryModel+'msvm.model -m MSVM2 -a 0.70 -k 1'
        print command        
        process = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE)
        process.wait()

    def concataneFiles(self, folder, output):
        outfile = open(self.dirResult+output, 'a')
        list_files = glob.glob (self.dirResult+'*.dat')
        count_lines = []
        for file in list_files :
            with open (file, "r") as myfile:
                data=myfile.readline()
                if len(data) != 0:
                    lines = int(data)
                    count_lines.append(lines)
        line_number = sum(count_lines)
        outfile.write(str(line_number))
        outfile.write('\n')
        for file in list_files :
            with open (file, "r") as f:
                lines=f.readlines()
        outfile.write(lines[1])
        for file in list_files :
            with open (file, "r") as myfile:
                data=myfile.read().splitlines(True)
                outfile.writelines(data[2:])
        outfile.close()
                
    def mixLines(self, inputFile, output, directoryModel):
        output = open(directoryModel+output, 'w')
        with open(self.dirResult+inputFile) as f:
            lines = f.readlines()
            output.write(lines[0])
            output.write(lines[1])
            lines = lines[2:]
            random.shuffle(lines)
        output.writelines(lines)
        f.close()
  
    def count (self, listWord, folder, output):
        with open(listWord) as f:
            attributes = f.read().splitlines()
            list_files = glob.glob (folder+'*')
            feature_file = open(self.dirResult+output, "w")
            count_line= 0
            for file in list_files :
                with open (file, "r") as myfile:
                    data=myfile.read()
                    i = 0
                    count_attribut = 0
                    for attribute in attributes:
                        i = i+1
                        if attribute in data:
                            count_attribut = count_attribut + 1
                        else:
                            count_attribut = count_attribut + 1
                    count_line = count_line +1
        feature_file.write(str(count_line))
        feature_file.write("\n")
        feature_file.write(str(count_attribut))
        feature_file.write("\n")


    def transform (self, listWord, folder, output, className):
    
        with open(listWord) as f:
            attributes = f.read().splitlines()
            list_files = glob.glob (folder+'*')
            feature_file = open(self.dirResult+output, "a")
            feature_lines = []
            
            for file in list_files :
                try:
                
                    line = ""
                    with open (file, "r") as myfile:
                            data=myfile.read()
                            
                    char_nbr = len(data)
                    words_nbr = len(data.split())
                    
                    i = 0
                    count_attribut = 0
                    for attribute in attributes:
                        
                        i = i+1
                         
                        if attribute in data:
                            line = line + "1 "
                        else:
                            line = line + "0 "
    
                    line = line + className
                    feature_file.write(str(line))
                    feature_file.write("\n")
                
                except Exception as e:
                    print ("\n Exception :", e)
                    feature_lines.append("# error 'utf-8' encoding")
