

import os
import sys
import json
import urllib2
import urllib
from HTMLParser import HTMLParser
from optparse import OptionParser

# http://viewtext.org/api/text?url=extension.fm&format=json
# grab the body content from a remote url, and turn it into fastfrag



## options
# -s "<div>raw string</div>"   # a string of html
# -f (open a file of html), output to sys
# -b (scrape a remore url, filter via viewtext.org)
# -r scrape the entire source of a remote url

"""Flow:
    
    1. accept a command from command line
    2. set in action 'fetching' of html
    3. hand string of HTML to converter
    4. parse HTML using xml.sax (hopefully)
    5. translate to JSON in accordance with fastFrag specifications
        (css for class, element attributes for everything but id and css, including in attribute)
        type : (element.nodeNode)
        content : (content of child element (string for textnode, object or dictionary))

"""

class MyHTMLParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        self.node_depth+=1
        # fast frag assumes div, skip type for this element
        if tag != "div":
            frag = { 'type' : tag }
        else:
            frag = {}
        
        for key,value in attrs:
            if key == "id":
                frag[key] = value
            elif key == "class":
                frag["css"] = value
            elif key:
                if not frag.get('attributes'):
                    frag['attributes']={}
                frag.get('attributes')[ key ] = value
                
        
        if not self.fragList:
            self.fragList = frag
        else:
            content = self.fragList
            processer=True
            if content:
                counter = 0
                while processer:
                    counter+=1
                    
                    if type(content) == dict:
                        if content.get('content'):
                            content=content.get('content')
                            continue # magic, forward to next element
                        
                        if type(content) == dict:
                            content['content']=[frag]
                        else:
                            # print "appending frag %s" % frag
                            content.append( frag )
                        processer=False
                    
                    elif type(content) == list:
                        if counter < self.node_depth:
                            content = content[ len(content)-1 ].get('content') or content[ len(content)-1 ]
                        else:
                            processer=False
                            content.append(frag)
            ## fix for non close tags... like image
            if tag == "img" or tag == "input":
                self.node_depth-=1
    
    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        #print "Encountered the end of a %s tag" % tag
    
    
    def close(self):
        print json.dumps( self.fragList )
        try:
            HTMLParser.close(self)
        except Exception,msg:
            print "\n possible error: %s " % msg
            pass
    
    def __init__(self):
        self.fragList=None
        self.node_depth=0
        self.allFrags=[]
        HTMLParser.__init__(self)


def fetch_and_scrape( remote_url ):
    print "fetching and scraping body of %s" % remote_url
    params=dict(
        format="json",
        url=remote_url,
    )
    
    response = urllib2.urlopen( "http://viewtext.org/api/text", urllib.urlencode( params ) )
    try:
        json_data= json.loads( response.read() )
    except Exception,msg:
        return 2
    
    body_string=json_data.get("content")
    _parse_string( body_string )

def fetch_url( page_url ):
    response = urllib2.urlopen( page_url )
    html_string = response.read()
    _parse_string( html_string )


def _parse_string( html_string  ):
    parser= MyHTMLParser()
    # print "starts with %s" % body_string
    print "--JSON ready: \n"
    response = parser.feed( html_string )
    parser.close()    

def handle_raw_string(  html_string  ):
    if not html_string or html_string == "":
        return
    _parse_string( html_string )
    
def open_and_parse_file( filename ):
    file_string=""
    with open(filename, 'r') as f:
        file_string = f.read()
        f.close()
    _parse_string( file_string )
    


if __name__ == '__main__':
    
    parser = OptionParser()
    # parser.add_option("-b", dest="remote_scrape_url",
    #                   help="Scrape 'html' body element structure (no text, only tags and attributes)", metavar="URL")
    
    parser.add_option("-r", dest="remote_url", type="string",
                        help="scrape a remote url", metavar="URL")
    
    parser.add_option("-f", dest="file_location", type="string",
                        help="open file and read contents", metavar="FILE")
    
    parser.add_option("-s", dest="string_html", type="string",
                        help="a raw string of HTML", metavar="STR")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    
    options,args = parser.parse_args()
    
    
    # if options.remote_scrape_url:
    #     fetch_and_scrape( options.remote_url )
    
    if options.remote_url:
        fetch_url( options.remote_url )
    
    if options.string_html:
        handle_raw_string( options.string_html )
    
    if options.file_location:
        print "read a file @ %s" % options.file_location
        open_and_parse_file( options.file_location )
    
    
