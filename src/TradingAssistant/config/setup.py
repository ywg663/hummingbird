# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/19 15:58
# @Author  : ywg663@qq.com
# @File    : setup.py
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

import yaml
import conf.ppath as conf_path
import utils.tools as tools

class App:
    """
    app配置
    """
    def __init__(self):
        self.conf = Configuration("app.yaml")

class MySql:
    """
    mysql相关配置
    """
    def __init__(self, file_name):
        self.con = Configuration(file_name).conf
        self.HOST = self.con["Mysql"]["Host"]
        self.MYSQL_CON_STR = self.con["Mysql"]["Constr"]
        self.PyMySql_STR = self.con['Mysql']['PyMySqlConstr']
        self.USER_NAME = self.con["Mysql"]["UserName"]
        self.PWD = self.con["Mysql"]["Pwd"]
        self.DATABASENAME = self.con["Mysql"]["DataBaseName"]

class MA:
    """
    设置均线常量
    """
    MA20 = 20
    MA60 = 60
    MA120 = 120

class SRoc:
    """
    设置sroc常量
    """
    ROC_LEN = 21
    EMA_LEN = 13
    SROC_LEN = 21

class Configuration:
    """
    通用配置加载
    加载指定的yaml格式配置文件，输出一个配置内容，通常为self.conf
    """
    def __init__(self, file_name):
        """
        初始化
        """
        tools.get_separator()
        self.file = conf_path.CONF_DIR + "{}{}".format(tools.get_separator(), file_name)
        with open(self.file, encoding='utf-8') as f:
            conf = yaml.unsafe_load(f)
            self.conf = conf



