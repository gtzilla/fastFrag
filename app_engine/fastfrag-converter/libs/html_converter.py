# 
#  html_converter.py
#  fastFrag
#  
#  Created by gregory tomlinson 
#  see README.md for more information
# 
    



from HTMLParser import HTMLParser
import logging
try:
    import json
except:
    import simplejson as json

class FastFragHTMLParser(HTMLParser):
    
    #
    def __init__(self, start_frag_list=None, unclosed_elements=None, max_depth=40):

        if not unclosed_elements:
            unclosed_elements=["col", "img", "input", "br", "hr"]            

        self.unclosed_elements=unclosed_elements           
        self.fragList=start_frag_list
        self.max_depth=max_depth
        
        # kinda private, but not really
        self.active_frag=None
        self.node_depth=0
        HTMLParser.__init__(self)    
    
    
    ## def feed(self):
    ## handled by actual parser
    
    
    def output_json_string(self, pretty_print=True):
        
        if pretty_print:
            out_results = json.dumps( self.fragList, sort_keys=True, indent=4 )
        else:
            out_results = json.dumps( self.fragList )
            
        logging.info("json is being dumped to page")
        return out_results
    
    def output(self):
        return self.fragList    
    
    
    def handle_startendtag(self, tag, attrs):
        self.node_depth+=1
        frag = self._create_basic_frag( tag, attrs )
        # self.active_frag=frag
        self._get_frag_location( frag, self.fragList )
        self.node_depth-=1
        ## decrement self close
        

    def handle_endtag(self, tag):
        ## just move the node counter
        
        self.node_depth-=1
     
    
    
    def handle_data(self,data):
        """this bug: https://github.com/gregory80/fastFrag/issues/#issue/3
        seems to be related to 'data' being triggered, but the active frag is not in the correct location
        """
        if data and data.strip() != "":
            ## add 'text' as an object (dict), 
            ## this is not requrired, could just be a string, make it easier on the parser
            
            ## TODO
            ## Known error: see notes_python_converstion.text ERROR: Images and Text
            text_data_dict = { 'text' : data }
            try:
                curr_node =self.active_frag.get('content')
            except:
                curr_node=None
            
            if type(curr_node) == dict:
                # logging.info("it's a dictionary %s and %s " % (data,curr_node) )
                self.active_frag['content'] = [curr_node,text_data_dict]
            elif type(curr_node) == list:
                logging.info("it's a list %s and %s " % (data,curr_node) )
            elif not curr_node:    
                self.active_frag['content']=text_data_dict

                          
    
    def handle_starttag(self, tag, attrs):
        
        """Note: The method handle_startendtag
        will handle any properly formatted HTML, otherwise, the tag will
        end up here, adjust as need to include more 'shitty' HTML """
        
        if tag in self.unclosed_elements:
            logging.info("shitty HTML for %s found in list" % tag )
            self.handle_startendtag( tag, attrs )
            return
        
        ## Proceed as normal
        self.node_depth+=1
        # fast frag assumes div, skip type for this element
        if self.node_depth > self.max_depth:
            raise Exception('recursion','recursion depth exception, prevent silliness or exploits')
        
        
        frag = self._create_basic_frag( tag, attrs )
        self.active_frag=frag
        if not self.fragList:
            self.fragList = frag
            self.fragList['content'] = {}
        else:
            self._get_frag_location( frag, self.fragList )


    # Pseuo Private handlers
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


    def _get_frag_location(self, frag, start_location):
        self.counter=0
        self._last_elem=None
        
        # Map HTML into fastFrag JSON
        def lookup( frag_el, start_el ):
            
            self.counter+=1
            ## correct location: add frag, adjust existing location as needed
            ## dict -> list, append 'new' (frag_el) item
            if self.counter == self.node_depth:
                self._add_frag_element( frag_el, start_el )
            else:
                # crawl, go deeper and deeper
                self._last_elem,next_el=self._crawler_deeper( start_el )
                                
                ## recurse
                lookup( frag_el, next_el)
            return start_el
        lookup( frag, start_location )

    def _crawler_deeper(self, start_el ):
        parent_elem=None
        future_elem=None
        if type(start_el) == dict:
            parent_elem=start_el
            if not start_el.get("content"):
                start_el['content'] = {}
            future_elem = start_el.get("content")
        
        elif type(start_el) == list:
            # grab the last items
            place_holder_el = start_el[ len(start_el)-1 ]
            
            if not place_holder_el.get('content'):
                place_holder_el['content'] = {}
                ## fuck around here, when no content exists, add one
                parent_elem=place_holder_el
                future_elem=place_holder_el.get('content')
            else:
                parent_elem=place_holder_el
                future_elem = place_holder_el.get('content')
        else:
            future_elem=start_el
            parent_elem=start_el
        
        return parent_elem,future_elem

    ## -- literally append this object to the the growing self.fragList
    def _add_frag_element(self, frag_el, start_el ):
        if self._last_elem:
            #self.active_frag=self._last_elem
            ## last elem is a recursive marker, 
            ## it's the 'parent' node in HTML terms            
            try:
                content = self._last_elem.get('content')
            except Exception,msg:
                logging.warn("excption, the last element has issues: %s" % msg )
                ## this excption is most likely because _last_elem is actuall a LIST object
                ## looks like I am dealing with that case down if elif type(content) == list
                content = self._last_elem
                self._last_elem.append( frag_el )
            
            if type(content) == dict and start_el:
                self._last_elem['content'] = [start_el, frag_el]
            elif type( content ) == dict:
                self._last_elem['content'] = frag_el
            elif type( content ) == list:
                content.append(frag_el)
            else:
                logging.warn("Error trying to add to last ele %s and type of content is %s" % (frag_el, type( content ) ) )

        
        else:
            if type(self.fragList) == dict:
                self.fragList=[start_el,frag_el]
            elif type(self.fragList) == list:
                self.fragList.append(frag_el)
            #self.active_frag=self.fragList               

             


