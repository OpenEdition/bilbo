#!/bin/bash

# utilisation : ./eval.sh dirCorpus percentOfTest numberOfpartition

dirCorpus=${1/\//}

rm -rf ${dirCorpus}-evaluation

python src/bilbo/evaluation/partition.py ${dirCorpus}/ $2 $3 ;
python src/bilbo/evaluation/bilboTrain.py ${dirCorpus}/ $2 $3 ;
python src/bilbo/evaluation/bilboAnnotate.py ${dirCorpus}/ $2 $3 ;
python src/bilbo/evaluation/bilboEval.py ${dirCorpus}/ $2 $3 ;
