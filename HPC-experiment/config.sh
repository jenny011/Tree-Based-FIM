#!/usr/bin/bash

HOME="/gpfsnyu/home/jz2915"
DIR="$HOME/$experiment"

experiment="CanTree"
expsnum=11

dataset="retail"
datasettype=".txt"
ALLDATADIR="$HOME/datasets"
data="$ALLDATADIR/$dataset$datasettype"

EXPDIR="$DIR/exp"
performance="$EXPDIR/performance/$dataset"
memory="$EXPDIR/memory/$dataset"
result="$EXPDIR/result/$dataset"
perf="$performance/perf"
mem="$memory/mem"
result="$result/result"

script="$DIR/run.py"
batch="$DIR/batch.slurm"
