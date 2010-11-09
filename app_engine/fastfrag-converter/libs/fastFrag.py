## inspired by https://github.com/apgwoz/hiccup
## clj version up next... fastFrag JSON (idl?)


try:
    import json
except:
    import simplejson as json
    
import logging
import datetime
from xml.etree import ElementTree


class fastFrag(object):
    
    @classmethod
    def create(self, json_structure=None, create_element_tree=False):
        
        if not json_structure:
            logging.info("no structure...")
            raise Exception("no-structure", "no structure")
        
        if type(json_structure) == dict:
            # hrmmm
            if create_element_tree:
                ## create an actual element tree and return it
                logging.info("not implemented")
                return
            
            pass
        elif type(json_structure) == list:
            ##yup
            logging.info("no root node found, creating string only")
            ## for list as root structure, have to make a string
            pass
        else:
            raise Exception("json", "not json, json required")
        
        pass
    
    @classmethod
    def parse(self, html_string=None):
        ## add the html_converter here
        pass    



class fastFragAssembler(object):
    
    def __init__(self):
        self.html_string=""
    
    def assembleHTML(self, params):
        curr_type = type(params)
        if curr_type == dict:
            self._create_node(self, params)
            
        elif curr_type == list:
            pass
        pass
    
    def _make_attributes(self, attributes=None):
        pass
    
    def _create_node(self, params):
        if params.get("text"):
            self.html_string += params.get("text")
        elif params.get("content"):
            elem_type = (params.get("type") or "div").lower()
            elem_content = params.get("content")
            elem_params = params.get("attrs") or params.get("attr") or params.get("attributes")
            if not elem_params:
                self.html_string += "<%s>" % elem_type
            else:
                ## add attributes to string
                elem_attr = self._make_attributes( elem_params )
                self.html_string += "<%s %s>" % (elem_type, elem_attr)
                