
from HTMLParser import HTMLParser
try:
    import json
except:
    import simplejson as json

class FastFragHTMLParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        self.node_depth+=1
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
                            continue # magic, forward to next element
                        
                        if type(content) == dict:
                            content['content']=[frag]
                        else:
                            # print "appending frag %s" % frag
                            content.append( frag )
                        processer=False
                    
                    elif type(content) == list:
                        if counter < self.node_depth:
                            content = content[ len(content)-1 ].get('content') or content[ len(content)-1 ]
                        else:
                            processer=False
                            content.append(frag)
            ## fix for non close tags... like image
            if tag == "img" or tag == "input" or tag == "hr" or tag == "meta":
                self.node_depth-=1
    
    def handle_endtag(self, tag):
        # print self.fragList
        self.node_depth-=1
        #print "Encountered the end of a %s tag" % tag

    def output_json(self):
        return json.dumps( self.fragList, sort_keys=True, indent=4 )
    
    def __init__(self):
        self.fragList=None
        self.node_depth=0
        self.allFrags=[]
        HTMLParser.__init__(self)