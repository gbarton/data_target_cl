#/usr/bin/python
from HTMLParser import HTMLParser
from datetime import datetime
import csv
import sys

# Works on the main craigslist sites page, looking for just
# the US sites. 

class MyHTMLParser(HTMLParser):
  val = ""
  attrs = []
  def getVal(self):
    return self.val;
  def handle_starttag(self, tag, attrs):
#      print "Encountered a start tag:", tag
      self.attrs += attrs
#      for attr in attrs:
#        print "     attr:", attr
#  def handle_endtag(self, tag):
#      print "Encountered an end tag :", tag
  def handle_data(self, data):
#      print "got data", data
      self.val =  data

state = False

with open('data/stateUrls','wb') as f:
  writer = csv.writer(f,delimiter='\t')

  for line in sys.stdin:
    line = line.strip()
    if len(line) == 0:
      continue
    #start of US section
    if "<a name=\"US\"></a>US" in line:
      state = True;
    #end of US section, header that didnt match US
    elif state and "<h1 class=\"continent_header\">" in line:
      state = False;
    #posting, url
    if state and "<li><a href=" in line:
      parser = MyHTMLParser()
      parser.feed(line)
      url = ""
      city = parser.val
      for attr in parser.attrs:
        if attr[0] == "href":
           url = attr[1]
      #different date formats
      if not city in ['guam-micronesia','puerto rico','U.S. virgin islands']:
        writer.writerow([url, city])

