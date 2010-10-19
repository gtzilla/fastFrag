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

# from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import libs.html_converter


class BaseHandler( tornado.web.RequestHandler  ):
    
    def process_html_string(self, html_string):
        parser = libs.html_converter.FastFragHTMLParser()
        parser.feed(html_string)
        string_out = parser.output_json()
        
        return string_out
        
        

class MainHandler(BaseHandler):
    def get(self):
        self.render("main.html")
        
    def post(self):
        text_string = self.get_argument("html_string")
        if not text_string:
            self.render("main.html")
            return
        string_out=""
        try:
            string_out = self.process_html_string( text_string  )
        except Exception,msg:
            print msg
        
        self.write(string_out)
        self.finish()
        
        
        
        
class APIHandler(BaseHandler):
    
    def get(self):
        pass



##
settings = {
    "blog_title": u"Tornado Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    # "ui_modules": {"Entry": EntryModule},
    # "xsrf_cookies": True,
}
application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    # (r"/archive", ArchiveHandler),
    # (r"/feed", FeedHandler),
    # (r"/entry/([^/]+)", EntryHandler),
    # (r"/compose", ComposeHandler),
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)
    # application = webapp.WSGIApplication([('/', MainHandler)],
    #                                      debug=True)
    # util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
