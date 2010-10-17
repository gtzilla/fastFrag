

import os
import sys
import json
import xml.sax.saxutils
import urllib2
import urllib
import getopt
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
        # print self.get_starttag_text()
        frag = { 'type' : tag }
        frag['attributes']={}
        
        for key,value in attrs:
            if key == "id":
                frag[key] = value
            elif key == "class":
                frag["css"] = value
            elif key:
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
                            continue
                            
                        if type(content) == dict:
                            content['content']=[frag]
                        else:
                            # print "appending frag %s" % frag
                            content.append( frag )
                        processer=False
                            
                    elif type(content) == list:
                        if counter < self.node_depth:
                            content = content[ len(content)-1 ]
                        else:
                            processer=False
                            content.append(frag)

    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        #print "Encountered the end of a %s tag" % tag

    
    def close(self):
        print json.dumps( self.fragList )
        HTMLParser.close(self)
    
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
        raise Usage( msg )
        return 2
    
    body_string=json_data.get("content")
    parser= MyHTMLParser()
    # print "starts with %s" % body_string
    print "::JSON ready"
    response = parser.feed( body_string )
    parser.close()

def fetch_url( page_url ):
    response = urllib2.urlopen( page_url )    
    print response.read()








### entry point    
def handle_args( commandline_opts ):
    print commandline_opts
    for a,opt in commandline_opts:
        if a == "-b":
            print "fetch and scrape body remote url: " + opt
            fetch_and_scrape( opt )
            break
        elif a == "-r":
            print "check out" + opt
            fetch_url( opt )
        elif a == "-h":
            print "not helpful"
        # print opt
        # print a
        
    


##


if __name__ == '__main__':


    parser = OptionParser()
    parser.add_option("-b", dest="remote_url",
                      help="Scrape 'html' body element structure (no text, only tags and attributes)", metavar="URL")
                      
    parser.add_option("-r", dest="remote_url", type="string", 
                        help="scrape a url", metavar="URL")                      
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")


    ## (options, args) = 
    options,args = parser.parse_args()
    
    
    if options.remote_url:
        fetch_and_scrape( options.remote_url )
    
    


# ## Generic? sorta... keep working on it, define handle_args
# class Usage(Exception):
#     def __init__(self, msg):
#         self.msg = msg
# 
# def main(argv=None):
#     if argv is None:
#         argv = sys.argv
#     try:
#         try:
#             opts, args = getopt.getopt(argv[1:], "rb:h", ["help"])
#         except getopt.error, msg:
#              raise Usage(msg)
#         # more code, unchanged
#         handle_args( opts )
#     except Usage, err:
#         print >>sys.stderr, err.msg
#         print >>sys.stderr, "for help use --help"
#         return 2
# 
# if __name__ == "__main__":
#     sys.exit(main())   