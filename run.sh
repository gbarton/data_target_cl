#!/bin/bash

if [[ ! -d "data/posting" ]]; then
 mkdir -pv "data/posting";
fi

r=0
while [ true ]
do
  python pullLatest.py
  r=$(( r + 1 ))
  if [[ $r == 1 ]]; then
    r=0;
    ./upload.sh;
  fi
  echo "sleeping"
  #half hour, based on it takes ~25 minutes to pull everything
  sleep 1800
done
