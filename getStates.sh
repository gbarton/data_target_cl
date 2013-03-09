#!/bin/bash

#pull latest site page

if [[ ! -d "data" ]]; then
 mkdir -pv "data"
fi

rm -rf data/sites
rm -rf data/stateUrls
wget -O data/sites http://www.craigslist.org/about/sites

cat data/sites | python extractSites.py


