
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

        self._get_frag_location( frag, self.fragList )        

        
        logging.info("start_endtag %s and  %s" % (tag, frag) )        
        ## decrement self close
        ## no action for sel closed?
        
    def handle_data(self,data):
        if data and data.strip() != "":
            logging.info("is this the text? %s for frag %s" % (data, self.active_frag ) )
            #self._get_frag_location( { 'text' : data }, self.fragList )            
            self.active_frag['content'] = { 'text' : data }
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
            
            self.counter+=1
            if self.counter == self.node_depth:
                
                if self._last_elem:
                    try:
                        content = self._last_elem.get('content')
                    except:
                        content = self._last_elem
                    if type(content) == dict:
                        if start_el:
                            self._last_elem['content'] = [start_el, frag_el]
                        else:
                            if type( content ) == dict:
                                self._last_elem['content'] = frag_el
                            elif type( content ) == list:
                                self._last_elem.append(frag_el)
                            else:
                                logging.warn("Error trying to add to last ele %s" % frag_el )
                    elif type(content) == list:
                        if type( self._last_elem ) == dict:
                            self._last_elem['content'] = [start_el, frag_el]
                        elif type(self._last_elem) == list:
                            self._last_elem.append(frag_el)                        

                else:
                    if type(self.fragList) == dict:
                        self.fragList=[start_el,frag_el]
                    elif type(self.fragList) == list:
                        self.fragList.append(frag_el)
                
            else:
                if type(start_el) == dict:
                    next_el = start_el.get("content")
                elif type(start_el) == list:
                    next_el= start_el[ len(start_el)-1 ]
                else:
                    next_el=start_el
                    logging.warn("start el is %s" % start_el)

                self._last_elem=start_el
                lookup( frag_el, next_el)
            
            return start_el
        
        lookup( frag, start_location )


    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        ## this is probably where I need to adjust the data constucts. 
        ## Like if I find a content that is a list with one item, change that shit back
        
        #print "Encountered the end of a %s tag" % tag

    def output_json(self):
        out_results = json.dumps( self.fragList, sort_keys=True, indent=4 )
        logging.info(out_results)
        return out_results
    
    def __init__(self):
        self.fragList=None
        self.active_frag=None
        self.attach_target=None
        self.node_depth=0
        self.allFrags=[]
        HTMLParser.__init__(self)