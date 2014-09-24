#!/bin/bash

# utilisation : ./eval.sh dirCorpus numberOfpartition prefix percentOfTest [percentOfTest…] -- bilbo options
# exemple     : ./eval.sh Corpus 10 huhu 10 20 30 40 50 -- -u
# it will
#  train on Corpus folder
#  do 10 partitions
#  in Corpus-eval-huhu folder
#  doing 10% 20% 30% 40% 50% of test
# with option -u for bilbo

dirCorpus=${1/\//}
shift
numberOfpartition=$1
shift
prefix=$1
shift
dirEval=${dirCorpus}-eval-${prefix}

args="$@"
percents=${args%%--*}
bilboOptions=${args##*--}
if [ "$percents" == "$bilboOptions" ]; then
	bilboOptions=
fi

for percentOfTest in $percents; do
	echo "Evaluation for ${percentOfTest}% of test data with $numberOfpartition partition"
	echo "Bilbo options : $bilboOptions"
	echo "  partitionning…"
	python src/bilbo/evaluation/partition.py ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
	echo "  training…"
	python src/bilbo/evaluation/bilboTrain.py $bilboOptions ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
	echo "  annotating…"
	python src/bilbo/evaluation/bilboAnnotate.py $bilboOptions ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
	echo "  evaluating…"
	python src/bilbo/evaluation/bilboEval.py ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
done;

# Création du fichier global de l'évaluation
globalEvalFile=${dirEval}/evaluation.tsv
head -n 1 ${dirEval}/${percents%% *}%/evaluation.tsv | sed "s/^/% of test data\t/" > $globalEvalFile
for percentOfTest in $percents; do
	tail -n 1 ${dirEval}/${percentOfTest}%/evaluation.tsv | sed "s/^/${percentOfTest}%\t/" >> $globalEvalFile
	echo >> $globalEvalFile
done;
