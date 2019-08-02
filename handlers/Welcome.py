# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/9/4
    Desc    :  欢迎页
"""
from handlers import BaseHandler


class IndexHander(BaseHandler):
    def get(self):
        self.render("index.html")
