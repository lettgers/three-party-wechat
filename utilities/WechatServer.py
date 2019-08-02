# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/7
    Desc    :   微信第三方服务端业务
"""
import json
import os
import time
from WXBizMsgCrypt import WXBizMsgCrypt
from config import component as com, logger as log, cache as cache
from utilities import HttpUtils as http, RedisUtils as redis


class XmlUtils:
    def __init__(self):
        self.token = com.component.get('token')
        self.key = com.component.get('key')
        self.appid = com.component.get('appid')
    # 加密XML
    def get_encrypt_xml(self, reply_xml, nonce):
        reply_xml = reply_xml.encode('utf-8')
        encrypt = WXBizMsgCrypt(self.token, self.key, self.appid)
        ret_encrypt, encrypt_xml = encrypt.EncryptMsg(reply_xml, nonce)
        if ret_encrypt == 0:
            return encrypt_xml
        else:
            return str(ret_encrypt) + ' error'
    # 解密XML
    def get_decrypt_xml(self, encrypt_xml, msg_signature, timestamp, nonce):
        decrypt = WXBizMsgCrypt(self.token, self.key, self.appid)
        ret_decrypt, decrypt_xml = decrypt.DecryptMsg(encrypt_xml, msg_signature, timestamp, nonce)
        if ret_decrypt == 0:
            return decrypt_xml
        else:
            return str(ret_decrypt) + ' error'

""" 提供获取文件读取公共方法"""
class WxCommon:

    def __init__(self):
        pass

    """ 获取本地component_verify_ticket"""
    def get_com_ticket(self):
        ticket = redis.Redis().get(cache.cache.get("com_verify_ticket"))
        if ticket is None:
            if os.path.exists('com_ticket.json'):
                json_file = open('com_ticket.json')
                data = json.load(json_file)
                json_file.close()
                ticket = data['ComponentVerifyTicket']
        return ticket

    """ 更新本地文件中的component_verify_ticket"""
    def set_com_ticket(self, data):
        redis.Redis().setEx(cache.cache.get("com_verify_ticket"), data['ComponentVerifyTicket'], 550)
        json_file = open('com_ticket.json', 'w')
        json_file.write(json.dumps(data))
        json_file.close()

    """ 获取本地文件中的预授权码 """
    def get_pre_auth_code(self):
        if os.path.exists('pre_auth_code.json'):
            json_file = open('pre_auth_code.json')
            data = json.load(json_file)
            json_file.close()
            return data
        else:
            log.Logger().getLogger().info('%s file does not exist' % 'pre_auth_code.json')
        return ''

    """ 获取第三方com_access_token """
    def get_com_access_token(self):
        com_acess_token = redis.Redis().get(cache.cache.get("com_access_token"))
        if com_acess_token is None:
            if os.path.exists('com_access_token.json'):
                json_file = open('com_access_token.json')
                data = json.load(json_file)
                json_file.close()
                return data
            else:
                log.Logger().getLogger().info('%s file does not exist' % 'com_access_token.json')
        return eval(com_acess_token)

    """ 更新本地文件中的第三方com_access_token """
    def set_com_access_token(self, data):
        redis.Redis().setEx(cache.cache.get("com_access_token"), data, 7000)
        json_file = open('com_access_token.json', 'w')
        json_file.write(json.dumps(data))
        json_file.close()

class WxOpenSDK:
    def __init__(self, ticket):
        self.component_appid = com.component.get('appid')
        self.component_appsecret = com.component.get('appsecret')
        self.ticket = ticket
    """获取第三方component_access_token"""
    def com_access_token(self):
        data = WxCommon().get_com_access_token()
        component_access_token = data['component_access_token']
        now = int(time.time())
        if data['expire_time'] < now:
            url = com.component.get('url').get('com_token')
            pams = {'component_appid': self.component_appid,
                    'component_appsecret': self.component_appsecret,
                    'component_verify_ticket': self.ticket}
            result = http.HttpClient().post(url, pams)
            log.Logger().getLogger().info('--------请求获取第三方component_access_token的结果:%s' % result)
            component_access_token = json.loads(result)['component_access_token']
            data['component_access_token'] = component_access_token
            data['expire_time'] = now + 7000
            WxCommon().set_com_access_token(data)
        return component_access_token

    """获取预授权码"""
    def pre_auth_code(self):
        url = com.component.get('url').get('pre_auth_code') + self.com_access_token()
        pams = {"component_appid": self.component_appid}
        result = http.HttpClient().post(url, pams)
        log.Logger().getLogger().info('--------请求预授权码的结果:%s' % result)
        result = json.loads(result)
        return result['pre_auth_code']

    """获取公众号的调用凭据和授权信息"""
    def get_authorizer_access_token(self, authorization_code):
        url = com.component.get('url').get('authorizer_access_token') + self.com_access_token()
        pams = {
            "component_appid": self.component_appid,
            "authorization_code": authorization_code
        }
        result = http.HttpClient().post(url, pams)
        log.Logger().getLogger().info('--------请求获取公众号的调用凭据和授权信息的结果:%s' % result)
        result = json.loads(result)
        return result['authorization_info']

    """（刷新）授权公众号接口调用凭据"""
    def get_refresh_authorizer_access_token(self, authorizer_appid, authorizer_refresh_token):
        url = com.component.get('url').get('refresh_authorizer_access_token') + self.com_access_token()
        pams = {
            "component_appid": self.component_appid,
            "authorizer_appid": authorizer_appid,
            "authorizer_refresh_token": authorizer_refresh_token,
        }
        result = http.HttpClient().post(url, pams)
        log.Logger().getLogger().info('--------请求（刷新）授权公众号接口调用凭据的结果:%s' % result)
        result = json.loads(result)
        return result

    """获取授权方的帐号基本信息"""
    def get_authorizer_info(self, authorizer_appid):
        url = com.component.get('url').get('authorizer_info') + self.com_access_token()
        pams = {
            "component_appid": self.component_appid,
            "authorizer_appid": authorizer_appid
        }
        result = http.HttpClient().post(url, pams)
        log.Logger().getLogger().info('--------请求获取授权方的帐号基本信息的结果:%s' % result)
        result = json.loads(result)
        return result['authorizer_info']

# if __name__ == "__main__":
#     now = int(time.time())
#     print now