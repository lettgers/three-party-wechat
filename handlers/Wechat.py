# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/9/7
    Desc    :   微信三方平台接口
"""
from handlers import BaseHandler
from config import logger as log
from utilities import WechatServer
from client import third, reply
from module.models import Service


class IndexHander(BaseHandler):
    # def get(self):
    #     result = Service(self.session).getWebAccessToken('wx399181b3084d12f5')
    #     return self.write(str(result))
    # def get(self):
    #    a = Service(self.session).save("cccccccc","xxxx","aaaaa")
    #    return self.write(str(a))
    # def get(self):
    #     res = Service(self.session).getAuthorizerInfoByAppId("wx399181b3084d12f5")
    #     return self.write(str(res))
    def get(self):
        # res = Service(self.session).getUserInfoByAid("905284997085265930")
        res = Service(self.session).getUserInfoByOpenIdAndAid(2, 905284997085265930)
        return self.write(res)
    # def get(self):
    #     res = Service(self.session).saveUserInfo(905284997085265930, '2', '2', False, False, 2, 2, 2, 2)
    #     print res
    #     return self.write("ok")
#  服务号授权控制器
class WechatHander(BaseHandler):
    def get(self):
        auth_code = self.get_argument('auth_code', '')
        expires_in = self.get_argument('expires_in', '')
        if len(auth_code) > 10 and int(expires_in) > 60:
            return self.write('License success!')
        url = third.auth_page()
        log.Logger().getLogger().info('>>>>>>>>>>>>>url %s' % url)
        self.render("auth.html", page=str(url))

    def post(self):
        msg_signature = self.get_argument('msg_signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        log.Logger().getLogger().info('event get msg_signature: %s, timestamp: %s, nonce: %s' % (msg_signature, timestamp, nonce))
        encrypt_xml = self.request.body
        log.Logger().getLogger().info('encrypt_xml is : %s' % encrypt_xml)
        if encrypt_xml.find('ToUserName') == -1:
            encrypt_xml = encrypt_xml.replace('AppId', 'ToUserName')
        decrypt_xml = WechatServer.XmlUtils().get_decrypt_xml(encrypt_xml, msg_signature, timestamp, nonce)
        log.Logger().getLogger().info('get the ticket decryp_xml: %s' % decrypt_xml)
        if decrypt_xml.find('error') == -1:
            third.ticket(self.session, decrypt_xml)
        self.write('success')


# 公众号消息与事件接收URL
class AuthHander(BaseHandler):
    def post(self, appid):
        if appid.find('wx') != 0:
            return self.write('request not appid')
        log.Logger().getLogger().info("request appid is :%s " % appid)
        msg_signature = self.get_argument('msg_signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        log.Logger().getLogger().info('message event get msg_signature: %s, timestamp: %s, nonce: %s' % (msg_signature, timestamp, nonce))
        encrypt_xml = self.request.body.decode('utf-8')
        decrypt_xml = WechatServer.XmlUtils().get_decrypt_xml(encrypt_xml, msg_signature, timestamp, nonce)
        log.Logger().getLogger().info('get the message decryp_xml: %s' % decrypt_xml)
        if decrypt_xml.find('error') == -1:
            if appid == 'wx570bc396a51b8ff8':
                return third.whole(decrypt_xml, nonce, self)
            result = reply.reply(decrypt_xml, nonce, appid,self)
            self.write(str(result))
