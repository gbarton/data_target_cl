#!/bin/bash

export MAHOUT_HEAPSIZE="-Xmx5000m -server -XX:+UseConcMarkSweepGC -XX:ParallelGCThreads=4 -XX:+UseParNewGC "
mahout fpg \
     -i sums/fpgSet/ \
     -o patterns2 \
     -k 50 \
     -method mapreduce \
     -g 50 \
     -regex '[\ ]' \
     -s 50
#     -method sequential \
#     -i sums/fpgSet/part-r-00000 \
