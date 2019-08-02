# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/9/7
    Desc    :   基础接口
"""
from handlers import BaseHandler
from client import terrace as ter

appid = "wx3991025d0ed19xxx"
openid = "ojulPw40VZVGyRDQtlPBTxxx"
# 推送模板消息
class PushTemplateMsgHander(BaseHandler):

    def get(self):
        res = ter.Terrace(self.session, appid).web_access_token()
        self.write(res)

# JsTicket
class JsTicketHander(BaseHandler):
    def get(self):
        pass


# 获取用户信息
class UserInfoHander(BaseHandler):
    def get(self):
        print self.request
        res = ter.Terrace(self.session, appid).get_user_info(openid)
        self.write(res)


# 同步微信用户信息
class SyncUserInfoHander(BaseHandler):
    def post(self):
        pass

# 生成永久类型的二维码
class Create_Qrcode(BaseHandler):
    def get(self):
        res = ter.Terrace(self.session, appid).create_qrccode("agokara")
        self.write(str(res))
