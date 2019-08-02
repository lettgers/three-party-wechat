# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/12
    Desc    :   微信客户端业务
"""
import json
from utilities import HttpUtils as http
from config import component as com, logger as log


class WxClient:
    def __init__(self, access_token):
        self.access_token = access_token

    """获取用户信息"""
    def get_user_info(self, openid):
        url = com.component.get("web").get("user_info") % (self.access_token, openid)
        result = http.HttpClient().get(url)
        result = json.loads(result)
        log.Logger().getLogger().info('--------用户已经关注拉取到的用户信息:%s' % result)
        return result

    """同步微信用户信息"""
    def get_sync_user_info(self):
        pass

    """获取当前服务号的js_ticket"""

    def get_js_ticket(self):
        pass

    """推送模板消息"""

    def push_template_msg(self):
        pass

    """生成永久二维码"""

    def create_qrcode(self, scene):
        pams = {
            "action_name": "QR_LIMIT_STR_SCENE",
            "action_info": {
                "scene": {
                    "scene_str": scene
                }
            }
        }
        url = com.component.get("web").get("create_qrcode") + self.access_token
        result = http.HttpClient().post(url, pams)
        result = json.loads(result)
        log.Logger().getLogger().info('--------生成的永久二维码结果:%s' % result)
        return result
