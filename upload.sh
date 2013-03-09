#!/bin/bash

if [[ ! -d "data/posting" ]]; then
 mkdir -pv "data/posting";
fi

hadoop fs -put data/posting/* stage/
rm -rf /data/posting/*;

pig -param OUTDIR=`date +%Y%m%d%H%M%S` -f uploadAndCompress.pig

hadoop fs -rm -r "stage/*"
