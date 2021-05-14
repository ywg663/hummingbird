# -*- coding: utf-8 -*-
# @Time    : Copyright 2020/11/19 17:10
# @Author  : ywg663@qq.com
# @File    : account.py
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

from sqlalchemy import Column, Integer, Float, String, DateTime
from .common import Base

'''' 帐户 '''
class Account(Base):
    """
    帐号表
    """
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    '''
    编号
    '''
    serial = Column(String(32))
    '''
    业务编号
    '''
    create_datetime = Column(DateTime)
    '''
    创建时间
    '''
    update_time = Column(DateTime)
    '''
    更新时间
    '''
    status = Column(Integer)
    '''
    状态
    '''
    type = Column(Integer)
    '''
    类型
    '''
    name = Column(String(20))
    '''
    名称
    '''
    pwd = Column(String)
    '''
    密码
    '''
    amount = Column(Float)
    '''
    金额
    '''
