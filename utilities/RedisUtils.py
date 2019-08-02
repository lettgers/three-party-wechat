# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/9/5
    Desc    :   操作redis
"""

import redis
import json
import time
from config import cache, logger as log


class Redis:
    def __init__(self):
        pool = redis.ConnectionPool(host='10.10.0.20', port=6379, password='12345', db=1)
        self.redis = redis.Redis(connection_pool=pool)

    # return result true
    def set(self, name, val):
        try:
            return self.redis.set(name, val)
        except Exception as e:
            log.Logger().getLogger().info(
                '@@@@@@@@向Str:redis中添加name:[%s];val:[%s];@@@发生异常:[%s]' % (name, val, e.message))
        return False

    def get(self, name):
        try:
            return self.redis.get(name)
        except Exception as e:
            log.Logger().getLogger().info('@@@@@@@@获取Str:redis中name:[%s];@@@发生异常:[%s]' % (name, e.message))
        return None

    # return result true
    def setEx(self, name, val, time):
        try:
            return self.redis.setex(name, val, time)
        except Exception as e:
            log.Logger().getLogger().info(
                '@@@@@@@@向EX;redis中添加name:[%s];val:[%s];time:[%s];@@@发生异常:[%s]' % (name, val, time, e.message))
        return False

    # return result 1
    def setHash(self, name, key, val):
        try:
            return self.redis.hset(name, key, val)
        except Exception as e:
            log.Logger().getLogger().info(
                '@@@@@@@@向Hash;redis中添加name:[%s];key:[%s];val:[%s];发生异常:[%s]' % (name, key, val, e.message))
        return 0

    def getHash(self, name, key):
        try:
            return self.redis.hget(name, key)
        except Exception as e:
            log.Logger().getLogger().info('@@@@@@@@获取HasH;redis中name:[%s];@@@发生异常:[%s]' % (name, e.message))
        return None

    # return result 1
    def delKey(self, name):
        return self.redis.delete(name)

    # return result true
    def expire(self, name, time):
        return self.redis.expire(name, time)


#if __name__ == "__main__":
            # web_access_token = dict()
            # web_access_token["appid"] = "111111111"
            # web_access_token["authorizer_access_token"] = "authorizer_access_token"
            # web_access_token["authorizer_refresh_token"] = "authorizer_refresh_token"
            # print type(web_access_token)
            # Redis().setEx(cache.cache.get('web_access_token')+"111111111", web_access_token, 7000)
            # res = Redis().get(cache.cache.get('web_access_token') + "111111111")
            # res = eval(res)
            # print res["authorizer_access_token"]
