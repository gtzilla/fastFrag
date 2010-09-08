import markdown
import json
import traceback
import sys
from markdown import etree
import logging

STX = u'\u0002'  # Use STX ("Start of text") for start-of-placeholder
ETX = u'\u0003'  # Use ETX ("End of text") for end-of-placeholder


class JSONExtension(markdown.Extension):
    
    
    def extendMarkdown(self, md, md_globals):
        
        md.registerExtension(self)
        
        treeprocessor = JSONTreeProcessor(md)
        md.json_mode = True
        md.treeprocessors.add("json", treeprocessor, ">inline")
    
    
    def reset(self):
        pass


## try and turn the etree into fastFrag JSON
class JSONTreeProcessor( markdown.treeprocessors.Treeprocessor ):
    
    def __init__ (self, md):
        self._md = md
    
    def get_placeholder(self, key):
        return "%swzxhzdk:%d%s" % (STX, key, ETX)
    
    def make_tag_frag(self, elem, elem_content=None):
        attributes=None
        css=None
        if elem.items():
            attributes={}
            for attr in elem.items():
                if attr[0] == "class":
                    css = attr[1]
                    continue
                else:
                    attributes[ attr[0] ] = attr[1]
        params = dict(
            type=elem.tag,            
            content=elem_content or elem.text,
        )
        if css:
            params['css'] = css;
        if attributes:
            params['attributes'] = attributes;
        return params
    
    def run(self, root):
        
        self.depth=0
        def finder(element):
            frag_list = []
            self.depth+=1
            for child in element:
                
                
                #monkey patch this, put the HTML back
                # stick this elsewhere
                #TOOO
                # known error
                """* > The only problem with a democracy is that the idiots get to speak too.
                    <cite>patriot</cite>
                    
                    causes a parser fail.., probaly has something to do with how I am putting HTML back..
                    
                    """
                treat_text_as_xml=False
                if child.text:
                    for i in range(self._md.htmlStash.html_counter):
                        html, safe  = self._md.htmlStash.rawHtmlBlocks[i]
                        if child.text and child.text.find( self.get_placeholder(i) ) > -1:
                            child.text = child.text.replace(self.get_placeholder(i), html)
                            treat_text_as_xml=True
                    
                    if treat_text_as_xml:
                        parser = etree.XMLParser()
                        try:
                            parser.feed( child.text )
                        except:
                            traceback.print_tb(sys.exc_info()[2])                            
                            logging.info("Error with node %s and tag %s" % (child.tag, child.text))
                        
                        results = parser.close()
                        child.text=None
                        child.append(results)
                        child.tag="div"
                        child.text=None
                
                deeper = finder(child)
                
                frag = {}
                
                
                if not deeper:
                    
                    if child.tail and child.tail.strip() is not "":
                        frag = {
                            'text' : child.tail
                        }
                        frag_list.append( self.make_tag_frag( child ) )
                        #frag_list.append( frag )
                    else:
                        frag = self.make_tag_frag( child )

                else:

                    #frag = deeper
                    
                    if child.text and child.text.strip() is not "":
                        node_data = []
                        node_data.append( {'text' : "%s" % (child.text) } )
                        if len(deeper) > 0:
                            node_data.extend( deeper )
                        else:
                            node_data.append( deeper )
                        
                        frag = self.make_tag_frag( child, node_data  )
                            
                    else:
                        frag = self.make_tag_frag( child, deeper )
                
                
                frag_list.append( frag )
            
            
            #
            if len(frag_list) == 1:
                return frag_list[0]
            elif len(frag_list) > 0:
                return frag_list
            
            return frag_list
        
        res = finder(root)

        
        self._md.frag_list = res


def makeExtension(configs=None):
    return JSONExtension(configs=configs)