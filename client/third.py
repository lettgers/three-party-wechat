# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/7
    Desc    :   微信第三方平台业务; 授权页面; 取消,授权,更新; 全网发布
"""
import time
import datetime
import lxml.etree as etree
from utilities import WechatServer, HttpUtils as http, RedisUtils as redis
from urllib import urlencode
from config import logger as log, component as com, cache as cache
from module.models import Service


# 拉取授权页面
def auth_page():
    com_ticket = WechatServer.WxCommon().get_com_ticket()
    log.Logger().getLogger().info("@@@@@@com_ticket:%s" % com_ticket)
    wxOpenSDK = WechatServer.WxOpenSDK(com_ticket)
    pre_auth_code = wxOpenSDK.pre_auth_code()
    redirect_uri = com.component.get('redirect_uri')
    log.Logger().getLogger().info("@@@@@@redirect_uri:%s" % redirect_uri)
    url = com.component.get('url').get('login_page')
    params = {
        "component_appid": com.component.get('appid'),
        "pre_auth_code": pre_auth_code,
        "redirect_uri": redirect_uri
    }
    url = url + urlencode(params)
    return url

# TODO 需要删除
def test(session):
    authorization = Service(session).getByAppId("cccccccc")
    if authorization is not None:
        authorization.authorizer_access_token = "xxxxxxxxxxxxxx"
        authorization.update_time = datetime.datetime.now()
        session.commit()

# 处理ticket和公众号授权事件(取消,授权,更新)
def ticket(session, decrypt_xml):
    ticket_xml = etree.fromstring(decrypt_xml)
    info_type = ticket_xml.find('InfoType').text
    log.Logger().getLogger().info('get InfoType: %s' % info_type)
    if info_type == 'component_verify_ticket':  # 推送的消息是ComponentVerifyTicket
        data = {'ComponentVerifyTicket': ticket_xml.find('ComponentVerifyTicket').text}
        log.Logger().getLogger().info('get the ComponentVerifyTicket: %s' % data)
        WechatServer.WxCommon().set_com_ticket(data)
    elif info_type == 'unauthorized':
        authorizer_appid = ticket_xml.find('AuthorizerAppid').text
        if authorizer_appid == 'wx570bc396a51b8ff8':
            log.Logger().getLogger().info('全网发布取消授权通知!')
        else:
            log.Logger().getLogger().info('@@@@@@@@@@@@需要操作数据库取消授权')
            authorizerInfo_ = Service(session).getAuthorizerInfoByAppId(authorizer_appid)
            if authorizerInfo_ is not None:
                authorizerInfo_.authorizer_status = False
                authorizerInfo_.update_time = datetime.datetime.now()
                session.commit()
    elif info_type == 'authorized':
        authorizer_appid = ticket_xml.find('AuthorizerAppid').text
        log.Logger().getLogger().info('@@@@@@@@@@@@公众号授权 appid is:[%s] ' % authorizer_appid)
        authorizer(session, ticket_xml=ticket_xml)
    elif info_type == 'updateauthorized':
        authorizer_appid = ticket_xml.find('AuthorizerAppid').text
        log.Logger().getLogger().info('@@@@@@@@@@@@更新授权 appid is:[%s] ' % authorizer_appid)
        authorizer(session, ticket_xml=ticket_xml)

# 保存授权信息
def authorizer(session, ticket_xml):
    authorizer_appid = ticket_xml.find('AuthorizerAppid').text
    if authorizer_appid == 'wx570bc396a51b8ff8':
        log.Logger().getLogger().info('全网发布账号不记录数据信息!')
    else:
        authorization_code = ticket_xml.find('AuthorizationCode').text
        log.Logger().getLogger().info('authorizer_info is AuthorizerAppid:[%s] and AuthorizationCode:[%s] ' %(authorizer_appid, authorization_code))
        verify_ticket = WechatServer.WxCommon().get_com_ticket()
        if verify_ticket != '':
            wxOpenSDK = WechatServer.WxOpenSDK(verify_ticket)
            authorization = wxOpenSDK.get_authorizer_access_token(authorization_code)
            now = time.time()
            now = int(now) + 7000
            date = datetime.datetime.now()
            if authorization is not None:
                web_access_token = dict()
                web_access_token["appid"] = authorizer_appid
                web_access_token["authorizer_access_token"] = authorization['authorizer_access_token']
                web_access_token["authorizer_refresh_token"] = authorization['authorizer_refresh_token']
                web_access_token["create_time"] = date.strftime('%Y-%m-%d %H:%M:%S')
                web_access_token["expires_in"] = now
                redis.Redis().setEx(cache.cache.get('web_access_token')+authorizer_appid, web_access_token, 7000)
                authorization_ = Service(session).getAuthorizationByAppId(authorizer_appid)
                if authorization_ is not None:
                    authorization_.authorizer_access_token = authorization['authorizer_access_token']
                    authorization_.authorizer_refresh_token = authorization['authorizer_refresh_token']
                    authorization_.expires_in = now
                    authorization_.update_time = date
                    session.commit()
                else:
                    Service(session).saveAuthorization(
                        authorizer_appid=authorizer_appid,
                        authorizer_access_token=authorization['authorizer_access_token'],
                        authorizer_refresh_token=authorization['authorizer_refresh_token']
                    )
                authorizerinfo = wxOpenSDK.get_authorizer_info(authorizer_appid)
                if authorizerinfo is not None:
                    nick_name = authorizerinfo['nick_name']
                    head_img = ''
                    if authorizerinfo.has_key('head_img'):
                        head_img = authorizerinfo['head_img']
                    service_type_info = authorizerinfo['service_type_info']['id']
                    verify_type_info = authorizerinfo['verify_type_info']['id']
                    user_name = authorizerinfo['user_name']
                    principal_name = authorizerinfo['principal_name']
                    alias = authorizerinfo['alias'] if authorizerinfo['alias'] is not None else ""
                    qrcode_url = authorizerinfo['qrcode_url']
                    authorizer_type = False
                    signature = ''
                    if authorizerinfo.has_key('MiniProgramInfo'):
                        authorizer_type = True
                        signature = authorizerinfo['signature']
                    authorizerInfo_ = Service(session).getAuthorizerInfoByAppId(authorizer_appid)
                    if authorizerInfo_ is not None:
                        authorizerInfo_.authorizer_nick_name = nick_name
                        authorizerInfo_.authorizer_head_img = head_img
                        authorizerInfo_.authorizer_service_type = service_type_info
                        authorizerInfo_.authorizer_verify_type = verify_type_info
                        authorizerInfo_.authorizer_user_name = user_name
                        authorizerInfo_.authorizer_principal_name = principal_name
                        authorizerInfo_.authorizer_alias = alias
                        authorizerInfo_.authorizer_qrcode_url = qrcode_url
                        authorizerInfo_.authorizer_status = True
                        authorizerInfo_.authorizer_type = authorizer_type
                        authorizerInfo_.authorizer_signature = signature
                        authorizerInfo_.update_time = datetime.datetime.now()
                        session.commit()
                    else:
                        Service(session).saveAuthorizerInfo(
                            authorizer_appid=authorizer_appid,
                            authorizer_nick_name=nick_name,
                            authorizer_head_img=head_img,
                            authorizer_service_type=service_type_info,
                            authorizer_verify_type=verify_type_info,
                            authorizer_user_name=user_name,
                            authorizer_principal_name=principal_name,
                            authorizer_alias=alias,
                            authorizer_qrcode_url=qrcode_url,
                            authorizer_status=True,
                            authorizer_type=authorizer_type,
                            authorizer_signature=signature
                        )

# 全网发布
def whole(decrypt_xml, nonce, response):
    xml = etree.fromstring(decrypt_xml)
    toUserName = xml.find('ToUserName').text
    fromUserName = xml.find('FromUserName').text
    msgType = xml.find('MsgType').text
    if msgType == 'event':
        event = xml.find("Event").text
        eval_cont = event+'from_callback'
        return send_text_cont(fromUserName, toUserName, eval_cont, nonce, response)
    elif msgType == 'text':
        content = xml.find('Content').text
        log.Logger().getLogger().info('get the content %s' % content)
        if content == 'TESTCOMPONENT_MSG_TYPE_TEXT':
            reply_cont = content+'_callback'
            return send_text_cont(fromUserName, toUserName, reply_cont, nonce, response)
        elif content.startswith('QUERY_AUTH_CODE'):
            response.write("")
            query_auth_code = content.split(':')[1]
            com_ticket = WechatServer.WxCommon().get_com_ticket()
            wxOpenSDK = WechatServer.WxOpenSDK(com_ticket)
            info = wxOpenSDK.get_authorizer_access_token(query_auth_code)
            authorizer_access_token = info['authorizer_access_token']
            post_cont = query_auth_code + '_from_api'
            post_custom_text_msg(fromUserName, post_cont, authorizer_access_token)

# send all text msg
def send_text_cont(fromu, tou, cont, nonce, response):
    reply_xml = """
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>""" % (fromu, tou, int(time.time()), cont)
    encrypt_xml = WechatServer.XmlUtils().get_encrypt_xml(reply_xml, nonce)
    response.write(encrypt_xml)

# send custom text msg
def post_custom_text_msg(touser, content, stoken):
    url = com.component.get('url').get('customer_msg') + stoken
    payload = {
        "touser": touser,
        "msgtype": "text",
        "text":
            {
                "content": content
            }
    }
    result = http.HttpClient().post(url, payload)
    log.Logger().getLogger().info('send custom message result %s' % result)
