#/usr/bin/python
from HTMLParser import HTMLParser
from datetime import datetime
import csv
import sys

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

class CLPost:
  "url,post,date,price,seller,location"
  def __init__(self):
    self.url = ""
    self.post = ""
    self.date = ""
    self.price = ""
    self.seller = ""
    self.location = ""
  def tsv(self):
    return [self.url,self.post,self.date,self.price,self.seller,self.location]


post = CLPost()

currDate = ""

#output file
outName = datetime.today().strftime('%Y%m%d%H%M%S%f')
with open(outName,'wb') as f:
  writer = csv.writer(f,delimiter='\t')

  for line in sys.stdin:
    line = line.strip()
    if len(line) == 0:
      continue
    #date (comes in as Mon Feb 11)
    if "class=\"ban\"" in line:
      parser = MyHTMLParser()
      parser.feed(line)
      dateObj = datetime.strptime(`datetime.today().year`+ " " +  parser.val,'%Y %a %b %d')
      print "date converted: ", dateObj.strftime('%Y/%m/%d')
      currDate = dateObj.strftime('%Y/%m/%d')
    #find starting block
    if "<p class=\"row\"" in line:
      state = True;
      post.date = currDate
    elif state and "</p" in line:
      state = False;
      print ""
      print "post: ",post.post
      writer.writerow(post.tsv())
      post = CLPost()
    #posting, url
    if state and line.startswith("<a href"):
      parser = MyHTMLParser()
      parser.feed(line)
      post.post = parser.val
      for attr in parser.attrs:
        if attr[0] == "href":
          post.url = attr[1]
    #price
    elif state and "class=\"itempp\"" in line:
      parser = MyHTMLParser()
      parser.feed(line)
      post.price = parser.val
    #location
    elif state and "class=\"itempn\"" in line:
      parser = MyHTMLParser()
      parser.feed(line)
      post.location = parser.val
    #seller
    elif state and "class=\"itemcg\"" in line:
      parser = MyHTMLParser()
      parser.feed(line)
      post.seller = parser.val
