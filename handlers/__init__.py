# -*- coding: UTF-8 -*-
"""
    Created by cpp on 2017/8/7.
"""

import tornado.web
from utilities.database import session

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = session

    def on_finish(self):
        self.session.close()

    def get(self, *args, **kwargs):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            self.write('error:' + str(status_code))
