# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/9
    Desc    :   http请求工具
"""
import tornado.httpclient
import json
from config import logger as log


class HttpClient:
    def __init__(self):
        self.http_client = tornado.httpclient.HTTPClient()
        self.http_header = {}

    def close(self):
        self.http_client.close()

    def get(self, url):
        request = tornado.httpclient.HTTPRequest(url=url, method='GET', connect_timeout=200, request_timeout=600,
                                                 headers=self.http_header)
        return self.execute(request)

    def post(self, url, pams):
        self.http_header = {'Content-Type': 'application/json;charset=UTF-8'}
        body = json.dumps(pams)
        request = tornado.httpclient.HTTPRequest(url=url, method='POST', body=body, connect_timeout=200,
                                                 request_timeout=600, headers=self.http_header)
        return self.execute(request)

    def execute(self, request):
        try:
            response = self.http_client.fetch(request)
            return response.body
        except tornado.httpclient.HTTPError as e:
            log.Logger().getLogger().info('Execute Error:%s' % e)
        finally:
            self.close()


class AsyncHttpClient:
    def __init__(self):
        self.http_client = tornado.httpclient.AsyncHTTPClient()
        self.http_header = {}

    def close(self):
        self.http_client.close()

    def get(self, url):
        request = tornado.httpclient.HTTPRequest(url=url, method='GET', connect_timeout=200, request_timeout=600,
                                                 headers=self.http_header)
        return self.execute(request)

    def post(self, url, pams):
        self.http_header = {'Content-Type': 'application/json;charset=UTF-8'}
        body = json.dumps(pams)
        request = tornado.httpclient.HTTPRequest(url=url, method='POST', body=body, connect_timeout=200,
                                                 request_timeout=600, headers=self.http_header)
        return self.execute(request)

    def execute(self, request):
        try:
            response = self.http_client.fetch(request)
            return response.body
        except tornado.httpclient.HTTPError as e:
            log.Logger().getLogger().info('Execute Error:%s' % e)
        finally:
            self.close()
