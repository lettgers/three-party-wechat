# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/11
    Desc    :   接收微信消息并处理
"""
import time
import lxml.etree as etree
from utilities import WechatServer
from config import wx, logger as log

# 处理接收的事件
def reply(decrypt_xml, nonce, appid, session):
    xml = etree.fromstring(decrypt_xml)
    toUserName = xml.find('ToUserName').text
    fromUserName = xml.find('FromUserName').text
    msgType = xml.find('MsgType').text
    log.Logger().getLogger().info(" received MsgType: %s " % msgType)
    if msgType == wx.WxConsts.get("MsgType").get("MSG_TEXT"):
        content = xml.find('Content').text
        log.Logger().getLogger().info(" received message: %s " % content)
        if content == "安可":
            return send_img_cont(fromUserName, toUserName, "", nonce)
        # 默认不做处理
        return send_text_cont(fromUserName, toUserName, content, nonce)

    elif msgType == wx.WxConsts.get("MsgType").get("MSG_EVENT"):
        event = xml.find("Event").text
        if event == wx.WxConsts.get("EventType").get("EVT_SUBSCRIBE"):
            log.Logger().getLogger().info("@@@@@@@@@@ 用户关注公众号: %s " % event)

            # TODO 需要处理
        elif event == wx.WxConsts.get("EventType").get("EVT_UNSUBSCRIBE"):
            log.Logger().getLogger().info("@@@@@@@@@@ 用户取消关注公众号: %s " % event)
            # TODO 需要处理
        elif event == wx.WxConsts.get("EventType").get("EVT_SCAN"):
            log.Logger().getLogger().info("@@@@@@@@@@ 用户扫描二维码 : %s " % event)

# 回复文本消息
def send_text_cont(fromu, tou, cont, nonce):
    reply_xml = """
    <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%d</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
    </xml>""" % (fromu, tou, int(time.time()), cont)
    encrypt_xml = WechatServer.XmlUtils().get_encrypt_xml(reply_xml, nonce)
    return encrypt_xml

# 回复图文消息
def send_img_cont(fromu, tou, cont, nonce):
    url = "http://club.agoent.com/wechat/1001"
    pic = "http://agoent-res.oss-cn-beijing.aliyuncs.com/wechat/wall.jpg"
    cont = "祝大家玩得开心愉快!"
    reply_xml = """
    <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%d</CreateTime>
        <MsgType> <![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
            <item>
                <Title><![CDATA[欢迎光临"%s",点击开始参与互动]]></Title>
                <Description><![CDATA[%s]]></Description>
                <PicUrl><![CDATA[%s]]></PicUrl>
                <Url><![CDATA[%s]]></Url>
            </item>
        </Articles>
    </xml>
    """%(fromu, tou, int(time.time()), "xxx", cont, pic, url)
    encrypt_xml = WechatServer.XmlUtils().get_encrypt_xml(reply_xml, nonce)
    return encrypt_xml
