#!/bin/bash

# usage
#  put xml to be labeled in Label/ folder
#  put labeled xml in Train/train.xml
#  evaluation/evaluate.sh [dirResult]

if [ "$1" != "" ]; then
	dirResult=$1
else
	dirResult=Result/
fi
labeledXML=Train/train.xml

echo "python src/bilbo/Main.py -L -k all -t bibl  Label/ ${dirResult}"
python src/bilbo/Main.py -L -k all -t bibl  Label/ ${dirResult}

bilboXML=`ls -dt ${dirResult}tmp*|head -n 1`/testEstCRF.xml

echo "python src/bilbo/output/formatEvalBilbo.py $bilboXML"
python src/bilbo/output/formatEvalBilbo.py $bilboXML > ${dirResult}testEval.txt
echo "python src/bilbo/output/formatEvalBilbo.py $labeledXML"
python src/bilbo/output/formatEvalBilbo.py $labeledXML > ${dirResult}testEval-source.txt

echo "python src/bilbo/output/tokenAccuracyEval.py ${dirResult}testEval.txt ${dirResult}testEval-source.txt"
python src/bilbo/output/tokenAccuracyEval.py ${dirResult}testEval.txt ${dirResult}testEval-source.txt > ${dirResult}evaluation.txt

echo "wc -l ${dirResult}testEval.txt ${dirResult}testEval-source.txt"
wc -l ${dirResult}testEval.txt ${dirResult}testEval-source.txt

# Mais non c'est ça qu'il faut faire :
# un dossier avec des fichiers annotés et des bibl dedans
# faitmoitout 
#
# => dossier 10%
# prend aléatoirement x% test / y% (100-x) train de fichier
# pour x (de 10 à 50) => 
# 	reprendre le process pour créer 10 partions aléatoire de x%
# 	création de 10 fichiers only_bibl_clean et un fichier train
# 
# k-folder-cross-validation
# 
# 	-- changer les paramètres (feature, …)
# =>
# 	entrainer (10 fois) => dossier/10%/ => enregistrer le model dans chacun des partitions

# => dossier/10%/
# 	annoter et évaluer 10 evaluations sur chacun des 10 fichiers de test, en utilsant le model fabriqué par le train
# 
# dossier annoté de test
#  - 5 partitions
#    - 10 partitions
#      - un fichier train
# 
# 100 fichiers
# 20%
# 10 dossiers-20% :
#  - test/20 fichiers de test choisis aléatoirement parmis les 100
#    train/80 fichier de train choisis aléatoirement parmis les 100
#    test-clean/
#  - 20 fichiers de test choisis aléatoirement parmis les 100
#    80 fichier de train choisis aléatoirement parmis les 100
#  - 20 fichiers de test choisis aléatoirement parmis les 100
#    80 fichier de train choisis aléatoirement parmis les 100
#  - 20 fichiers de test choisis aléatoirement parmis les 100
#    80 fichier de train choisis aléatoirement parmis les 100
