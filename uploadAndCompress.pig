--uploads from {currentdir}/stage, does a distinct to clean up all the copies
-- from the inneficient downloading and gzip's them up for better storage.
-- a copy is then kept locally in {currentdir}/cl/ for manual cleanup/archive.

REGISTER /usr/lib/pig/piggybank.jar

set output.compression.enabled true;
set output.compression.codec org.apache.hadoop.io.compress.GzipCodec;

a = LOAD 'stage/' using PigStorage('\t') as (url:chararray, post:chararray, date:chararray, price:chararray, seller:chararray, location:chararray);
d = DISTINCT a;

store d into 'cl/$OUTDIR' using PigStorage();

