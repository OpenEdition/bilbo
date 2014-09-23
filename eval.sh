#!/bin/bash

# utilisation : ./eval.sh dirCorpus numberOfpartition prefix percentOfTest [percentOfTest…]
# exemple     : ./eval.sh Corpus 10 huhu 10 20 30 40 50
# it will
#  train on Corpus folder
#  do 10 partitions
#  in Corpus-eval-huhu folder
#  doing 10% 20% 30% 40% 50% of test


dirCorpus=${1/\//}
shift
numberOfpartition=$1
shift
prefix=$1
shift

for percentOfTest in $@; do
	echo "Evaluation for ${percentOfTest}% of test data"
	echo "  partitionning…"
	python src/bilbo/evaluation/partition.py     ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
	echo "  training…"
	python src/bilbo/evaluation/bilboTrain.py    ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
	echo "  annotating…"
	python src/bilbo/evaluation/bilboAnnotate.py ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
	echo "  evaluating…"
	python src/bilbo/evaluation/bilboEval.py     ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
done;