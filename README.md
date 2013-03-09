data_target_cl
==============

Uses Python/Pig to play with Craigslist postings.
Wanted to learn python better so this was a good excuse.
Wanted to learn Mahout, so also a good excuse!
Wanted to play with pig more, last and best excuse. :)

How to use
----------
1. checkout Project
2. install cloudera's version of Hadoop (hdfs,mr1,pig).
3. run to grab all US sites in craigslist (- a few that have different date formats)
    ./getStates.sh
4. kickoff the run script which will run forever, uploading once a day roughly into HDFS.
    ./run.sh

At this point you have data pouring into HDFS.  stats.pig has some initial fun things to use and play with, check it out.

