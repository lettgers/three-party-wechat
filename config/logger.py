# -*- coding: UTF-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler

"""
 日志模块
"""
class Logger:
    def __init__(self, filename="wehcat.log", toConsole=True, toFile=True):
        self.logger = logging.getLogger("log")
        if not self.logger.handlers:
            formatter = logging.Formatter("%(levelname)s %(asctime)s %(pathname)s [%(funcName)s] %(lineno)s :%(message)s", "%Y-%m-%d %H:%M:%S")
            self.logger.setLevel(logging.INFO)
            try:
                if toFile:
                    fh = TimedRotatingFileHandler(filename, when='D', backupCount=5)
                    fh.setLevel(logging.INFO)
                    fh.setFormatter(formatter)
                    self.logger.addHandler(fh)
            except Exception as e:
                print e
            if toConsole:
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)

    def getLogger(self):
        return self.logger
