
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
                if not frag.get('attrs'):
                    frag['attrs']={}
                frag.get('attrs')[ key ] = value
        
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
        
        """Note: The method handle_startendtag 
        will handle any properly formatted HTML, otherwise, the tag will 
        end up here, adjust as need"""
        
        if tag == "img" or tag=="input" or tag == "br":
            logging.info("shit HTML headed in")
            self.node_depth+=1 
            frag = self._create_basic_frag( tag, attrs )
            self._get_frag_location( frag, self.fragList )
            self.node_depth-=1             
            return            

        self.node_depth+=1    
        # fast frag assumes div, skip type for this element
        frag = self._create_basic_frag( tag, attrs ) 
        self.active_frag=frag       
        if not self.fragList:
            self.fragList = frag
            self.fragList['content'] = {}
        else:    
            self._get_frag_location( frag, self.fragList )

        
    def _frag_appender(self, frag=None):
        if type( frag ) == dict:
            pass
        elif type( frag ) == list:
            pass
        elif type(frag) == str:
            pass
        else:
            logging.warn("fail, not a dict or list or str... is this where I make one?")
        
            
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
                    except Exception,msg:
                        logging.warn("excption, the last element has issue: %s" % msg )
                        ## this excption is most likely because 
                        ##_list_elem is actuall a LIST object, which has no method get
                        ## looks like I am dealing with that case down if elif type(content) == list
                        content = self._last_elem
                        self._last_elem.append( frag_el )
                        
                    if type(content) == dict and start_el:
                        self._last_elem['content'] = [start_el, frag_el]
                    elif type( content ) == dict:
                        self._last_elem['content'] = frag_el
                    elif type( content ) == list:
                        logging.info("content is list, last elem is dict. List %s and last %s and frag is %s" % (content, self._last_elem, frag_el))
                        content.append(frag_el)
                    else:
                        logging.warn("Error trying to add to last ele %s and type of content is %s" % (frag_el, type( content ) ) )
                    # elif type(content) == list:
                    #     if type( self._last_elem ) == dict:
                    #         self._last_elem['content'] = [start_el, frag_el]
                    #     elif type( self._last_elem ) == list:
                    #         self._last_elem.append(frag_el)                        

                else:
                    if type(self.fragList) == dict:
                        logging.info("changing the original fraglist, alter dict --> list %s" % frag_el)
                        self.fragList=[start_el,frag_el]
                    elif type(self.fragList) == list:
                        self.fragList.append(frag_el)
                
            else:
                logging.info("location %s and last is %s" % (start_el, self._last_elem ))
                if type(start_el) == dict:
                    self._last_elem=start_el
                    if not start_el.get("content"):
                        start_el['content'] = {}                        
                    
                    next_el = start_el.get("content")             

                elif type(start_el) == list:
                    place_holder_el = start_el[ len(start_el)-1 ]
                    
                    logging.info("digging and found a list... want to use this %s and add %s" % (place_holder_el, frag_el))
                    
                    if not place_holder_el.get('content'):
                        place_holder_el['content'] = {}
                        ## fuck around here, when no content exists                    
                        self._last_elem=place_holder_el
                        next_el=place_holder_el.get('content')
                    else:
                        logging.info("no content element fall throw, contine crawl.. %s" % place_holder_el )
                        self._last_elem=place_holder_el
                        next_el = place_holder_el.get('content')
                else:
                    next_el=start_el
                    self._last_elem=start_el
                    logging.warn("start el is %s |w00t| %s |and umm| %s" % (start_el, next_el, frag_el) )


                lookup( frag_el, next_el)
            
            return start_el
        
        lookup( frag, start_location )


    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        ## this is probably where I need to adjust the data constucts. 
        ## Like if I find a content that is a list with one item, change that shit back
        
        #print "Encountered the end of a %s tag" % tag

    def output_json(self, pretty_print=True):
        
        if pretty_print:
            out_results = json.dumps( self.fragList, sort_keys=True, indent=4 )
        else:
            out_results = json.dumps( self.fragList )
        logging.info(out_results)
        return out_results
    
    def __init__(self):
        self.fragList=None
        self.active_frag=None
        self.attach_target=None
        self.node_depth=0
        self.allFrags=[]
        HTMLParser.__init__(self)