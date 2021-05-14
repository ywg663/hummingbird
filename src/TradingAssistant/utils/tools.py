# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/18 16:26
# @Author  : ywg663@qq.com
# @File    : tools.py
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

import platform

def get_separator():
    """
    获取系统平台类型，确定目录分隔符
    :return:
    """
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator

def jqcode_to_trading(jqcode):
    """
    处理标的代码为
    :param jqcode:
    :return:
    """
    ''''标的代码处理'''
    suffix = jqcode[-5:]
    if suffix == '.XSHE':
        return "SZSE:" + jqcode[0:6]
    if suffix == '.XSHG':
        return "SSE:" + jqcode[0:6]
    return None

def jqcode_to_eastmoney(jqcode, is_zs):
    """
    处理标的代码为东方财富代码
    :param jqcode: jq代码
    :param is_zs: 是否指数
    :return:
    """
    ''''标的代码处理'''
    if is_zs:
        return 'zs'+jqcode[0:6]
    suffix = jqcode[-5:]
    if suffix == '.XSHE':
        return "sz" + jqcode[0:6]
    if suffix == '.XSHG':
        return "sh" + jqcode[0:6]
    return None


if __name__ == "__main__":
    s = jqcode_to_trading("603997.XSHG")
    print(s)
