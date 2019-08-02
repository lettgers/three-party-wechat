# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/9/6
    Desc    :   获取公众号信息(access_token and authorizerinfo)
"""
import time,datetime
from utilities import RedisUtils as redis, WechatClient as client, WechatServer as server
from config import cache
from module.models import Service


class Terrace:

    def __init__(self, session, appid):
        self.session = session
        self.appid = appid

    """ 获取公众账号的 access_token """
    def web_access_token(self):
        res = redis.Redis().get(cache.cache.get("web_access_token") + self.appid)
        if res is None:
            res = Service(self.session).getWebAccessToken(self.appid)
        now = int(time.time())
        date = datetime.datetime.now()
        res = eval(res)
        if res["expires_in"] < now:
            com_ticket = server.WxCommon().get_com_ticket()
            wxOpenSDK = server.WxOpenSDK(com_ticket)
            res = wxOpenSDK.get_refresh_authorizer_access_token(self.appid, res["authorizer_refresh_token"])
            web_access_token = dict()
            web_access_token["appid"] = self.appid
            web_access_token["authorizer_access_token"] = res['authorizer_access_token']
            web_access_token["authorizer_refresh_token"] = res['authorizer_refresh_token']
            web_access_token["create_time"] = date.strftime('%Y-%m-%d %H:%M:%S')
            web_access_token["expires_in"] = now+7000
            redis.Redis().setEx(cache.cache.get('web_access_token') + self.appid, web_access_token, 7000)
            Service(self.session).upWebAccessToken(self.appid, res["authorizer_access_token"], res["authorizer_refresh_token"], now + 7000)
        return res["authorizer_access_token"]

    def create_qrccode(self, scene):
        return client.WxClient(self.web_access_token()).create_qrcode(scene)

    def get_user_info(self, openid):
        return client.WxClient(self.web_access_token()).get_user_info(openid)
