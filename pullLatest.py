#/usr/bin/python
from HTMLParser import HTMLParser
from datetime import datetime
import time
import csv
import sys
import urllib2

class MyHTMLParser(HTMLParser):
  val = ""
  attrs = []
  def restart(self):
    self.val = ""
    self.attrs = []
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
      self.val =  " ".join(data.split())

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
  def reset(self):
    __init__(self)
  def tsv(self):
    return [self.url,self.post,self.date,self.price,self.seller,self.location]


#output file
outName = "./data/posting/" + datetime.today().strftime('%Y%m%d%H%M%S%f')

pages = 0

#total posts found
totalCount = 0

def msNow():
  return int(round(time.time()*1000))

tDL = 0;
tStrip = 0;
tDate = 0;
tState = 0;
tPost = 0;

#html parser
parser = MyHTMLParser()

with open(outName,'wb') as f:
 writer = csv.writer(f,delimiter='\t')
 with open('data/stateUrls', 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  for row in reader:
    for col in ['.html']:#,'100.html','200.html','300.html','400.html','500.html']:
      pages += 1
      t = msNow()
      web = ""
      got = False
      #cl hangs sometimes, this should get around it.
      tries = 0
      while got == False and tries < 8:
        try:
          print "getting: ", `pages` + " " + row[0] + "/sss/index" + col
          web = urllib2.urlopen(row[0]+ "/sss/index" + col, timeout = 30)
          got = True;
          tDL += msNow() - t
    #      print "tDL:    ",tDL
    #      print "tStrip: ",tStrip
    #      print "tDate:  ",tDate
    #      print "tState:  ",tState
    #      print "tPost:  ",tPost
          #init first poting
          post = CLPost()
          #date holder TODO: will be wrong come Jan 1st
          currDate = ""
          #count of posts found for this page
          count = 0

          for line in web:
            t = msNow()
            line = line.strip()
            tStrip += msNow() - t
            if len(line) == 0:
              continue
            t = msNow()
            #date (comes in as Mon Feb 11)
            if "class=\"ban\"" in line:
              parser.restart()
              parser.feed(line)
              dateObj = datetime.strptime(`datetime.today().year`+ " " +  parser.val,'%Y %a %b %d')
              currDate = dateObj.strftime('%Y/%m/%d')
            tDate += msNow() - t
            t = msNow()
            #find starting block
            if line.startswith("<p class=\"row\""):
              state = True;
              post.date = currDate
            elif state and line.startswith("</p>"):
              state = False;
              writer.writerow(post.tsv())
              count+= 1
              post = CLPost()
            tState += msNow() - t
            t = msNow()
            #posting, url
            if state and line.startswith("<a href"):
              parser.restart()
              parser.feed(line)
              post.post = parser.val
              for attr in parser.attrs:
                if attr[0] == "href":
                  post.url = attr[1]
                  break
            #price
            elif state and line.startswith("<span class=\"itempp\""):
              parser.restart()
              parser.feed(line)
              post.price = parser.val
            #location
            elif state and line.startswith("<span class=\"itempn\""):
              parser.restart()
              parser.feed(line)
              post.location = parser.val
            #seller
            elif state and line.startswith("<span class=\"itemcg\""):
              parser.restart()
              parser.feed(line)
              post.seller = parser.val
            tPost += msNow() - t
          totalCount += count
          print "total loaded: ", totalCount
#        except urllib2.URLError as e:
#          tries += 1
        except KeyboardInterrupt: 
          print "keyboard interupt detected, exiting"
          sys.exit()
        except:
          tries += 1
          print "failed attempt: " + `tries` + "/8"


