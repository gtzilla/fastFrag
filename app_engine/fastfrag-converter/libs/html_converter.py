
from HTMLParser import HTMLParser
import logging
try:
    import json
except:
    import simplejson as json

class FastFragHTMLParser(HTMLParser):
    
    
    def _create_basic_frag(self, tag, attrs):
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
        
        return frag        
    
    def handle_startendtag(self, tag, attrs):

        frag = self._create_basic_frag( tag, attrs )        
        
        logging.info("start_endtag %s and  %s" % (tag, frag) )        
        ## decrement self close
        ## no action for sel closed?
        
    def handle_data(self,data):
        logging.info("data? is this the text? %s" % data )
    
    def handle_starttag(self, tag, attrs):
        
        ## notes, I need a switch for possible self closed tags like images
        ## properly closed, causes an error.
        ## add a flag to check if this tag will be closed.... somehow...
        
        self.node_depth+=1
        # fast frag assumes div, skip type for this element
        frag = self._create_basic_frag( tag, attrs )        
        if not self.fragList:
            self.fragList = frag
        else:
            self._get_frag_location( frag, self.fragList )
            
    def _get_frag_location(self, frag, start_location):
        logging.info("thing type is %s" % type(start_location) )
        logging.info(self.getpos() )
        if start_location.get('content'):
            self._get_frag_location( frag, start_location.get('content') )
        else:
            start_location['content'] = frag
            
            
            
    
    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        #print "Encountered the end of a %s tag" % tag

    def output_json(self):
        return json.dumps( self.fragList, sort_keys=True, indent=4 )
    
    def __init__(self):
        self.fragList=None
        self.attach_target=None
        self.node_depth=0
        self.allFrags=[]
        HTMLParser.__init__(self)