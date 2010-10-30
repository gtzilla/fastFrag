#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import os
import tornado.web
import tornado.wsgi
import unicodedata
import wsgiref.handlers
import logging
try:
    import json
except:
    import simplejson as json

# from google.appengine.ext import webapp
import libs.html_converter


class BaseHandler( tornado.web.RequestHandler  ):
    
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
    
    def output_page(self, frag_string):
        self.render("output.html", data_output=frag_string, error=False)
    
    def _test_frag_output(self, frag_json_string):
        try:
            json_frag = json.loads(frag_json_string)
        except:
            logging.info("error, not json?")
            self.render("output.html", data_output=frag_json_string, error=True)
            return
        
        self.render("render_test.html", frag_test_data=json_frag, data_output=frag_json_string )



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
        
        logging.info("pretty print JSON is %s" % pretty_print)
        if sample_test:
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


##
settings = {
    "blog_title": u"Fast Frag",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "xsrf_cookies": True,
    # "ui_modules": {"Entry": EntryModule},
    # "xsrf_cookies": True,
}
application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/rad/(.*)", FragHandler),
    # (r"/feed", FeedHandler),
    # (r"/entry/([^/]+)", EntryHandler),
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)
    logging.info("start app")
if __name__ == '__main__':
    main()
