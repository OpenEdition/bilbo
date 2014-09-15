#!/bin/bash

# usage
#  put xml to be labeled in Label/ folder
#  put labeled xml in Train/train.xml
#  evaluation/evaluate.sh [dirResult]

if [ $1 != "" ]; then
	dirResult=$1
else
	dirResult=Result/
fi
labeledXML=Train/train.xml

echo "Go Bilbo"
python src/bilbo/Main.py -L -k all -t bibl  Label/ ${dirResult}

bilboXML=`ls -dt ${dirResult}tmp*|head -n 1`/testEstCRF.xml

echo "python src/bilbo/output/formatEvalBilbo.py $bilboXML"
python src/bilbo/output/formatEvalBilbo.py $bilboXML > ${dirResult}testEval.txt
echo "python src/bilbo/output/formatEvalBilbo.py $labeledXML"
python src/bilbo/output/formatEvalBilbo.py $labeledXML > ${dirResult}testEval-source.txt

echo "python src/bilbo/output/tokenAccuracyEval.py ${dirResult}testEval.txt ${dirResult}testEval-source.txt"
python src/bilbo/output/tokenAccuracyEval.py ${dirResult}testEval.txt ${dirResult}testEval-source.txt