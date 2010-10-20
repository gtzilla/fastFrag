
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
        if data and data.strip() != "":
            logging.info("is this the text? %s for frag %s" % (data, self.active_frag ) )
            #self.active_frag['content'] = "%s" % data
    
    def handle_starttag(self, tag, attrs):
        
        ## notes, I need a switch for possible self closed tags like images
        ## properly closed, causes an error.
        ## add a flag to check if this tag will be closed.... somehow...
        
        self.node_depth+=1
        # fast frag assumes div, skip type for this element
        frag = self._create_basic_frag( tag, attrs ) 
        self.active_frag=frag       
        if not self.fragList:
            self.fragList = frag
            self.fragList['content'] = {}
        else:    
            self._get_frag_location( frag, self.fragList )
        # else:
        #     self._get_frag_location( frag, self.fragList )
            
    def _get_frag_location(self, frag, start_location):
        #logging.info("thing type is %s" % type(start_location) )

        self.counter=0
        self._last_elem=None
        def lookup( frag_el, start_el ):
            logging.info("goingdeep  to %s and %s depth %d" %  ( frag_el, start_el, self.node_depth  )  )
            self.counter+=1
            if self.counter == self.node_depth:
                logging.info("depth math %s" % frag_el)
            else:
                try:
                    next_el = start_el.get("content")
                except Exception, msg:
                    logging.info("hehhe %s" % msg )
                    pass
                self._last_elem=start_el
                lookup( frag_el, next_el)
            # #logging.info(" elem type %s for frag %s" % (type(start_el), frag_el ) )
            # next_el = start_el and start_el.get('content')
            # #logging.info("frag %s  start %s next %s" % ( frag_el, start_el, next_el ) )
            # if self.node_depth < self.counter:
            #     logging.info("goingdeep  to %s and %s next el %s" %  ( frag_el, start_el, next_el  )  )
            #     self.counter+=1                 
            #     lookup( frag_el, next_el )
            # else:
            #     if start_el and self.node_depth == self.counter:
            #         logging.info("start...")
            #         start_el['content'] = frag_el
            #     elif next_el:
            #         if type(next_el) == dict:
            #             start_el['content'] = [next_el, frag_el]
            #         elif type(next_el) == list:
            #             logging.info("its a list now")
            #             next_el.append(frag_el)
            # 
            #             
            #         logging.info("weird case to %s and %s next el %s" % ( frag_el, start_el, next_el  ) )
            # 
            #     logging.info("all to %s and %s next el %s" % ( frag_el, start_el, next_el  ) )
            # 
            # 
            # return start_el
        
        lookup( frag, start_location )


    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        #print "Encountered the end of a %s tag" % tag

    def output_json(self):
        return json.dumps( self.fragList, sort_keys=True, indent=4 )
    
    def __init__(self):
        self.fragList=None
        self.active_frag=None
        self.attach_target=None
        self.node_depth=0
        self.allFrags=[]
        HTMLParser.__init__(self)