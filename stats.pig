REGISTER /usr/lib/pig/piggybank.jar

a = LOAD 'cl/' using PigStorage('\t') 
  as (url:chararray, post:chararray, date:chararray, price:chararray, seller:chararray, location:chararray);

--do some cleanup on the post and remove dollar sign from price and hopefully only take the numeric prices
--NOTE: pull out the extra \ before the $ to run interactive
cl = foreach a generate url, 
	LOWER(REPLACE(post,'[\\?|\\.|\\-|\\!\\|=|\\~|\\*|\\"|\\[|\\]|\\:|\\#|\\\$|\\%|\\/|\\+|\\(|\\)]',' ')) as post,
  date, REPLACE(price,'[\\\$]|\\,','') as price,	seller, location;
clean = foreach cl generate url, REPLACE(post,'([ ])+',' ') as post,
  date, REGEX_EXTRACT(price,'([0-9])+',1) as price, seller, location;
--distinct and filter the cleaned up data
d = DISTINCT (filter clean by url is not null and post is not null and date is not null);

--total records seen on ingest
gall = GROUP a all;
tTotal = foreach gall generate COUNT(a);

--total records after deduping
ga = GROUP d all;
tDistinct = foreach ga generate COUNT(d);

--unique normalized post texts
fPost = foreach d generate post;
fPostD = DISTINCT fPost;
fga = GROUP fPostD all;
tUniquePosts = foreach fga GENERATE COUNT(fPostD);

--topics pulled from url
s = foreach d generate url, REPLACE(SUBSTRING(url,INDEXOF(url,'/',7)+1,LAST_INDEX_OF(url,'/')),'([a-z])+/','') as topic, post, date;

--count per topic, per day
gTopic = GROUP s BY (topic,date);
tTopicPerDay = foreach gTopic generate group.topic as topic, group.date as date, COUNT(s) as posts;

--avg post per topic
gavgf = foreach tTopicPerDay generate topic, posts;
gavg = GROUP gavgf by (topic);
tAvgPostsPerTopic = foreach gavg generate group as topic, AVG(gavgf.posts) as avg;


--NOT WORKING

--total posts per topic, per location
tppl = foreach d generate REPLACE(SUBSTRING(url,INDEXOF(url,'/',7)+1,LAST_INDEX_OF(url,'/')),'([a-z])+/','') as topic, location;
t = foreach tppl generate topic;
td = DISTINCT t;
tppld = DISTINCT tppl;
tpplg = group tppld by (topic, location);
tppf = foreach tpplg generate group.topic as topic, group.location as location, SUM(tppld) as count;
totalPostsPerLocationTopic = ORDER (FILTER tppf by location is not null and SIZE(location) > 1 and count > 10) BY count desc;


--id(url numeric portion), post output for Frequent Pattern Growth
--post has stop words removed
--     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such",
--	 "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"
fpg = foreach d generate SUBSTRING(url,LAST_INDEX_OF(url,'/')+1,LAST_INDEX_OF(url,'.')) as url, 
	TRIM(REPLACE(REPLACE(REPLACE(post,'[0-9\\\',]+',''),'\\b(?:i|a|an|and|are|as|at|be|but|by|for|if|in|into|is|it|my|no|not|of|on|or|the|these|this|to|was|we|with|very|you)\\b',' '),'([ ])+',' ')) as post;

rmf sums;

set job.name 'fpg';
STORE fpg into 'sums/fpgSet';
set job.name 'avgPostPerTopic';
STORE tAvgPostsPerTopic into 'sums/tAvgPostsPerTopic';
set job.name 'tTopicsPerDay';
STORE tTopicPerDay into 'sums/tTopicsPerDay';
set job.name 'tDistinctPosts';
STORE tUniquePosts into 'sums/tDistinctPosts';
set job.name 'tDistinctAll';
STORE tDistinct into 'sums/tDistinctAll';
set job.name 'tTotalCollected';
STORE tTotal into 'sums/tTotalCollected';
set job.name 'totalPostsPerLocationTopic';
STORE totalPostsPerLocationTopic into 'sums/totalPostsPerLocationTopic';



