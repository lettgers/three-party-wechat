# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/14
    Desc    :   
"""
import json
import time, datetime
import sys
from utilities import snowflake
from config import logger as log
from sqlalchemy import Column, String, BIGINT, INT, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from module import AlchemyEncoder

Base = declarative_base()


class Authorization(Base):
    # 表的名字:
    __tablename__ = 'wx_authorization_info'
    # 表的结构:
    id = Column(BIGINT, primary_key=True)
    authorizer_appid = Column(String(50), nullable=False)
    authorizer_access_token = Column(String(200), nullable=False)
    authorizer_refresh_token = Column(String(200), nullable=False)
    expires_in = Column(INT, nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    update_time = Column(TIMESTAMP, nullable=False)


class AuthorizerInfo(Base):
    __tablename__ = 'wx_authorizer_info'

    id = Column(BIGINT, primary_key=True)
    sid = Column(BIGINT, nullable=False, default=1001)
    authorizer_appid = Column(String(50), nullable=False)
    authorizer_nick_name = Column(String(50), nullable=False)
    authorizer_head_img = Column(String(200), nullable=False)
    authorizer_service_type = Column(INT, nullable=False)
    authorizer_verify_type = Column(INT, nullable=False)
    authorizer_user_name = Column(String(50), nullable=False)
    authorizer_principal_name = Column(String(200), nullable=False)
    authorizer_alias = Column(String(200), nullable=False)
    authorizer_qrcode_url = Column(String(200), nullable=False)
    authorizer_status = Column(Boolean, nullable=False)
    authorizer_type = Column(Boolean, nullable=False)
    authorizer_signature = Column(String(200), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    update_time = Column(TIMESTAMP, nullable=False)

class UserInfo(Base):
    __tablename__ = 'wx_user_info'

    id = Column(BIGINT, primary_key=True)
    openid = Column(String(50), nullable=False)
    nick_name = Column(String(50), nullable=False)
    subscribe = Column(Boolean, nullable=False)
    sex = Column(Boolean, nullable=False)
    province = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    headimgurl = Column(String(200), nullable=False)
    unionid = Column(String(50), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    update_time = Column(TIMESTAMP, nullable=False)
    aid = Column(BIGINT, ForeignKey('wx_authorizer_info.id'), index=True, nullable=False)
    authorizerInfo = relationship("AuthorizerInfo", backref=backref("wx_user_info", order_by=id))

class Service:
    def __init__(self, session):
        self.session = session

    def getAuthorizationByAppId(self, appid):
        return self.session.query(Authorization).filter_by(authorizer_appid=appid).first()

    def getWebAccessToken(self, appid):
        result = self.session.query(Authorization).filter_by(authorizer_appid=appid).first()
        return json.dumps(result, cls=AlchemyEncoder, check_circular=False)

    def upWebAccessToken(self, appid, authorizer_access_token, authorizer_refresh_token, now):
        res = self.session.query(Authorization).filter_by(authorizer_appid=appid).first()
        date = datetime.datetime.now()
        res.authorizer_access_token = authorizer_access_token
        res.authorizer_refresh_token = authorizer_refresh_token
        res.expires_in = now
        res.update_time = date
        self.session.commit()

    def saveAuthorization(self, authorizer_appid, authorizer_access_token, authorizer_refresh_token):
        now = int(time.time()) + 7000
        date = datetime.datetime.now()
        self.session.add(Authorization(
            id=snowflake.Snowflake().make_snowflake(time.time() * 1000, 1, 0),
            authorizer_appid=authorizer_appid,
            authorizer_access_token=authorizer_access_token,
            authorizer_refresh_token=authorizer_refresh_token,
            expires_in=now,
            create_time=date,
            update_time=date
        ))
        self.session.commit()

    def getAuthorizerInfoByAppId(self, appid):
        return self.session.query(AuthorizerInfo).filter_by(authorizer_appid=appid).first()

    def saveAuthorizerInfo(self, authorizer_appid, authorizer_nick_name, authorizer_head_img, authorizer_service_type,
                           authorizer_verify_type, authorizer_user_name, authorizer_principal_name, authorizer_alias,
                           authorizer_qrcode_url, authorizer_status, authorizer_type, authorizer_signature):
        date = datetime.datetime.now()
        self.session.add(AuthorizerInfo(
            id=snowflake.Snowflake().make_snowflake(time.time() * 1000, 1, 0),
            sid=1001,
            authorizer_appid=authorizer_appid,
            authorizer_nick_name=authorizer_nick_name,
            authorizer_head_img=authorizer_head_img,
            authorizer_service_type=authorizer_service_type,
            authorizer_verify_type=authorizer_verify_type,
            authorizer_user_name=authorizer_user_name,
            authorizer_principal_name=authorizer_principal_name,
            authorizer_alias=authorizer_alias,
            authorizer_qrcode_url=authorizer_qrcode_url,
            authorizer_status=authorizer_status,
            authorizer_type=authorizer_type,
            authorizer_signature=authorizer_signature,
            create_time=date,
            update_time=date
        ))
        self.session.commit()

    def getUserInfoByAid(self, aid):
        result = self.session.query(UserInfo).filter_by(aid=aid).all()
        return json.dumps(result, cls=AlchemyEncoder, check_circular=False)

    def saveUserInfo(self, aid, openid, nick_name, subscribe, sex, province, city, country, headimgurl):
        date = datetime.datetime.now()
        self.session.add(UserInfo(
            id=snowflake.Snowflake().make_snowflake(time.time() * 1000, 1, 0),
            aid=aid,
            openid=openid,
            nick_name=nick_name,
            subscribe=subscribe,
            sex=sex,
            province=province,
            city=city,
            country=country,
            headimgurl=headimgurl,
            unionid='',
            create_time=date,
            update_time=date
        ))
        self.session.commit()

    def getUserInfoByOpenIdAndAid(self, openid, aid):
        result = self.session.query(UserInfo).filter_by(aid=aid, openid=openid).first()
        return json.dumps(result, cls=AlchemyEncoder, check_circular=False)
