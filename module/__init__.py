# -*- coding: UTF-8 -*-
"""
    Author  :   曹鹏鹏
    E-mail  :   lettger@163.com
    Date    :   2017/8/14
    Desc    :   
"""

import json
import datetime
import types
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, datetime.datetime):
                        data = data.strftime('%Y-%m-%d %H:%M:%S')
                    if isinstance(data, types.LongType):
                        data = str(data)
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, types.MethodType):
                        pass
                    else:
                        fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
