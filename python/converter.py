

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
        print "Encountered the beginning of a %s tag" % tag

    def handle_endtag(self, tag):
        print "Encountered the end of a %s tag" % tag


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
    
    parser.feed( body_string )

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
    parser.add_option("-b", "--file", dest="remote_url",
                      help="scrape a url, get only 'html' body element", metavar="URL")
                      
    parser.add_option("-r", dest="remote_url", type="string", 
                        help="scrape a url", metavar="URL")                      
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")


    ## (options, args) = 
    options,args = parser.parse_args()
    
    
    if options.remote_url:
        fetch_and_scrape( options.remote_url )
    
    print options,args
    


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