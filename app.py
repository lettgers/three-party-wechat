# -*- coding: UTF-8 -*-
"""
    Created by cpp on 2017/8/7.
"""

import os.path
from tornado import web, ioloop
from tornado.httpserver import HTTPServer
import tornado.options
from handlers import Wechat as wx,Welcome as we,Basic as basic

class Application(web.Application):
    def __init__(self):
        handlers = [
            # (r"/", we.IndexHander),
            (r"/", wx.IndexHander),
            (r"/auth/event", wx.WechatHander),
            (r"/([a-zA-Z0-9-]+)/event", wx.AuthHander),
            (r"/appid", basic.PushTemplateMsgHander),
            (r"/qrcode", basic.Create_Qrcode),
            (r"/userinfo", basic.UserInfoHander),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=False,
            autoreload=True,
            default_handler_class=wx.BaseHandler
        )
        super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(8888)
    ioloop.IOLoop.current().start()
