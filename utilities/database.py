# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/14
    Desc    :   
"""
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

engine = create_engine('mysql+pymysql://write_user:3nQUCamLHa6+T^PdJGIpA.*A^paRPz3Y@10.10.0.18:3306/boonto_wechat_v1?charset=utf8', echo=True, encoding='utf-8')
session_factory = sessionmaker(autocommit=False, bind=engine)
session = session_factory()
