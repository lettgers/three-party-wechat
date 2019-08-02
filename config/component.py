# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/7
    Desc    :   第三方平台的配置信息
"""

component = {
    'appid': 'wx55d37bfa16afxxxx',
    'appsecret': '88fe1910d2f37e8500fc7b27a0xxxx',
    'token': 'www_agokara_com',
    'key': '2225f2476f4f80eea4cb6ea7805bb1602cd9xxx',
    'event_url': 'http://wx.agokara.com/$APPID$/client',
    'redirect_uri': 'http://wx.agokara.com/auth/event',
    'url': {
        'com_token': 'https://api.weixin.qq.com/cgi-bin/component/api_component_token',
        'pre_auth_code': 'https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token=',
        'login_page': 'https://mp.weixin.qq.com/cgi-bin/componentloginpage?',
        'authorizer_access_token': 'https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=',
        'refresh_authorizer_access_token': 'https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?component_access_token=',
        'authorizer_info': 'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?component_access_token=',
        'authorizer_token': 'https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?component_access_token=',
        'customer_msg': 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='
    },
    'web': {
        'create_qrcode': 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=',
        'user_info': 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN '
    }
}
