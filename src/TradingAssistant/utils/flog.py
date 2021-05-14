# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/17 16:22
# @Author  : ywg663@qq.com
# @File    : flog.py
# @Software: TA
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging.config
import logging.handlers
import os
from log import ppath as lstordir
import config.setup as st
from logging.handlers import RotatingFileHandler, SMTPHandler
from utils.femail import SendEmail

class SSLSMTPHandler(SMTPHandler):
    """
    使用ssl-smtp发送日志，主要针对error类错误
    """
    def emit(self, record):
        """
        Emit a record.
        """
        try:
            email = SendEmail()
            email.send(','.join(self.toaddrs), self.getSubject(record), self.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            self.handleError(record)

class FinanceLoger:
    """
    日志工具
    """
    logger = None

    def __init__(self, file_name):
        """
        初始化
        """
        self.config = st.Configuration(file_name)

    def get_loger(self):
        """
        获得一个loger
        :return:
        """
        logging.config.dictConfig(self.config.conf)
        return logging.getLogger()

    @staticmethod
    def create_loger():
        """
        创建一个Logger
        :return:
        """
        if FinanceLoger.logger is None:
            '''判断存储目录是否存在'''
            if os.path.exists(lstordir.LOG_STORE_DIR):
                pass
            else:
                os.mkdir(lstordir.LOG_STORE_DIR)
            FinanceLoger.logger = FinanceLoger("logging.yaml").get_loger()
            # FinanceLoger.logger.addHandler(mail_handler)


logging.handlers.SSLSMTPHandler = SSLSMTPHandler
FinanceLoger.create_loger()