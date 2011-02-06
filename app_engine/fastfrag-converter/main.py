#!/usr/bin/env python
#
#  main.py
#  fastFrag
#
#  Created by gregory tomlinson.
#  Original sample code from google applied to their app server, converted to tornado
#

import re
import os
import tornado.web
import tornado.wsgi
import unicodedata
import logging
import tornado.escape

import wsgiref.handlers
import logging
try:
    import json
except:
    import simplejson as json

import libs.html_converter

from page_samples import page_samples


class BaseHandler( tornado.web.RequestHandler  ):
    
    @property
    def frag_samples(self):
        frag_samples={}
        for k in page_samples:
            try:
                json_data = json.loads( page_samples[k] )
                frag_samples[k] = [json_data, page_samples[k] ]
            except:
                logging.warn("bad json?? %s" % page_samples[k] )
                continue
                pass
        
        return frag_samples
    
    
    @property
    def sample_html(self):
        return """<div id="my_id" class="my_class"><a href="/" class="my_class">fastFrag HTML => JSON</a></div>"""
    
    def process_html_string(self, html_string, pretty_print=True):
        try:
            parser = libs.html_converter.FastFragHTMLParser()
            parser.feed(html_string)
            
            string_out = parser.output_json_string( pretty_print )
        except Exception,msg:
            string_out=""
            logging.exception("max recursion depth error?! %s " % msg)
        return string_out
    
    def convert_fastFrag( self ):
        
        ## turn JSON into HTML... a string I suppose and output
        pass
        
    
    def output_page(self, frag_string, method_type="get", error=False):
        
        self.render("output.html", data_output=frag_string, method_type=method_type, samples=self.frag_samples, error=error)
    
    def _test_frag_output(self, frag_json_string):
        try:
            
            json_frag = json.loads(frag_json_string)
        except:
            self.output_page( "frag_json_string", error=True, method_type="post" )
            return
        
        self.render("render_test.html", frag_test_data=json_frag, samples=self.frag_samples, data_output=frag_json_string )
    
    
    def get_render_args(self):
        return {
        
        }
    
    def render(self, *args, **kwargs):
        """ pass in extra values to templates
        an easy spot to set the X-UA-Compatible header if this is a html response """
        new_kwargs = self.get_render_args()
        if not kwargs.get("error"):
            kwargs['error'] = False
        new_kwargs.update(kwargs)
        self.set_header("Cache-Control", "no-cache, no-store, max-age=0, must-revalidate")
        self.set_header("Pragma", "no-cache")
        # turn on google chrome frame when available
        if 'chromeframe' in self.request.headers.get('User-Agent', []):
            self.set_header("X-UA-Compatible","chrome=1")
        return super(BaseHandler, self).render(*args, **new_kwargs)



class MainHandler(BaseHandler):
    
    def get(self):
        
        self.render("main.html", placeholder=self.sample_html)
    
    def post(self):
        text_string = self.get_argument("html_string", None)
        sample_test = self.get_argument("sample_test", None)
        pretty_print = self.get_argument("pretty_print", None)
        frag_text_output = self.get_argument("frag_text_output", None)
        
        
        if frag_text_output:
            self._test_frag_output( frag_text_output )
            return
        
        if not pretty_print:
            pretty_print=False
        else:
            pretty_print=True
        

        
        if sample_test:
            ## convert the sample
            string_out=""
            try:
                string_out = self.process_html_string( self.sample_html, pretty_print  )
            except:
                pass
            
            self.output_page( string_out )
            return
        
        if not text_string:
            self.render("main.html", placeholder=self.sample_html)
            return
        string_out=""
        try:
            string_out = self.process_html_string( text_string, pretty_print  )
        except Exception,msg:
            logging.exception("error %s" % msg )
        
        self.output_page( string_out )


class FragJSONTestHandler(BaseHandler):
    
    def get(self):
        
        self.output_page("")
    
    
    def post(self):
        frag_text_output = self.get_argument("frag_text_output", None)
        if not frag_text_output:
            self.output_page("")
            return
        
        
        self._test_frag_output( frag_text_output )

class FragHandler(BaseHandler):
    
    def get(self, filename=None):
        if not filename:
            ## lazy quick static file server
            raise tornado.web.HTTPError(404)
            return
        try:
            self.render("rad/%s.html" % filename)
        except Exception,msg:
            logging.warn("error rendering template %s" % msg)
            raise tornado.web.HTTPError(404)

class GenericModuleLoader(tornado.web.UIModule):

    def render(self, name):
        if not name:
            return ""
            
        return self.render_string("modules/%s.html" % name)

settings = {
    "blog_title": u"fastFrag",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "xsrf_cookies": True,
    "ui_modules": {"stat_mod": GenericModuleLoader },
}
application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/frag", FragJSONTestHandler),
    (r"/rad/(.*)", FragHandler),
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)
    logging.info("start app")
if __name__ == '__main__':
    main()
