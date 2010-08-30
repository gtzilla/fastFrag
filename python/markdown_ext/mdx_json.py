import markdown
import json
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
        #md.set_output_format()




# class JSONPostProcess( markdown.postprocessors.Postprocessor ):
#
#     def run():

## try and turn the etree into fastFrag JSON
class JSONTreeProcessor( markdown.treeprocessors.Treeprocessor ):
    
    def __init__ (self, md):
        self._md = md
    
    def get_placeholder(self, key):
        return "%swzxhzdk:%d%s" % (STX, key, ETX)
    
    def run(self, root):
        # something
        print "rocking %d " % self._md.htmlStash.html_counter

        
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
                            logging.info("Error with node %s and tag %s" % (child.tag, child.text))
                            
                        results = parser.close()
                        child.text=None
                        child.append(results)
                        child.tag="div"
                        child.text=None

                deeper = finder(child)

                frag = {}
                if deeper:

                    frag = deeper
                    
                    if child.text and child.text.strip() is not "":
                        node_data = []
                        node_data.append( {'text' : "%s" % (child.text) } )
                        if len(deeper) > 0:
                            node_data.extend( deeper )
                        else:
                            node_data.append(deeper)
                        
                        frag = {
                            'type' : child.tag,
                            'content': node_data
                        }
                        if child.items():
                            attributes={}
                            for attr in child.items():
                                attributes[ attr[0] ] = attr[1]
                            frag['attributes'] = attributes
                            
                    
                    else:
                        frag = {
                            'type' : child.tag,
                            'content' : deeper
                        }
                        if child.items():
                            attributes={}
                            for attr in child.items():
                                if attr[0] == "class":
                                    frag['css'] = attr[1]
                                    continue
                                else:
                                    attributes[ attr[0] ] = attr[1]
                            frag['attributes'] = attributes                       
                    

                
                else:
                    if child.text and child.text.strip() is not "":
                        frag = {
                            'type' : child.tag,
                            'content' : "%s" % (child.text)
                        }
                        if child.items():
                            attributes={}
                            for attr in child.items():
                                attributes[ attr[0] ] = attr[1]
                            frag['attributes'] = attributes
                    
                    if child.tail and child.tail.strip() is not "":

                        frag_list.append( frag )
                        frag = {
                            'text' : child.tail
                        }
                    elif not child.text:

                        frag = {
                            'type' : child.tag,
                            'content' : ''
                        }
                        if child.items():
                            attributes={}
                            for attr in child.items():
                                attributes[ attr[0] ] = attr[1]
                            frag['attributes'] = attributes
                    
                
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