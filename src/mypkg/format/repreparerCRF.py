#!/usr/bin/env python
# encoding: utf-8
"""
repreparerCRF.py

Created by Young-Min Kim on 2011-09-28.

For the re-extraction of data

e.g.
python repreparerCRF.py ./ ../../Experiments/V5/e5_best/correction/ train_true_correction_ym.xml 1
python repreparerCRF.py ./ ../../Experiments/V5/e5_best/correction/ test_true_correction_ym.xml 0


"""

import sys
import subprocess



def run(codedirname, dirname, filename, indicator) :

	process = subprocess.Popen('echo "'+filename+'" > tmp.txt', shell=True, stdout=subprocess.PIPE)
	
	process.wait()
	
	print 'Start generating the primary data from xml files...'
	command = 'python '+str(codedirname)+'dataGenerator.py '+dirname+' tmp.txt > tmp_result.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'end of generation.\n'
	
	
	print 'Start reorganizing the primary data...'
	command = 'python '+str(codedirname)+'puncOrganizer.py tmp_result.txt > tmp_result2.txt'
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'end of reorganization.\n'
	
	print 'Start extracting training or test data...'
		
	if indicator == 0 or indicator == 20:
		command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 0 2 > newdata_CRF.txt'
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 2 > newdatawithlabel_CRF.txt'
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -2 2 > newdataonlylabel_CRF.txt'
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		if indicator == 20 :
			#command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 1 6 > trainingdata_rich_CRF2.txt' # 6:extract input and label 
			#process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			#process.wait()
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 5 > newdata_rich_CRF.txt'	# 5: extract input
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()
			command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt -1 6 > newdatawithlabel_rich_CRF.txt'
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			process.wait()

	elif indicator == 1 :
		command = 'python '+str(codedirname)+'extractor.py tmp_result2.txt 1 2 > trainingdata_CRF2.txt'
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
	
	
	print 'end of extraction.'
	
		
	#process = subprocess.Popen('rm tmp.txt', shell=True, stdout=subprocess.PIPE)
	process = subprocess.Popen('rm tmp.txt tmp_result.txt tmp_result2.txt', shell=True, stdout=subprocess.PIPE)
	process.wait()
	
	return



def main() :

	if len(sys.argv) != 5 :
		#print '** RE-Extraction of data file from a corrected xml file **'
		#print 'python repreparerCRF.py (dirname including codes) (dirname including the corrected file) (the corrected xml filname) (1:training, 0:test)'
		print '** RE-Extraction of data file from new xml file **'
		print 'python repreparerCRF.py (dirname including codes) (dirname including new file) (new xml filname) (1:training, 0:test(new), 20:all new data with rich feature files)'

		sys.exit(1)
		
	codedirname = str(sys.argv[1])
	dirname = str(sys.argv[2])
	filename = str(sys.argv[3])
	indicator = int(sys.argv[4])
		
	run(codedirname, dirname, filename, indicator)


if __name__ == '__main__':
	main()
