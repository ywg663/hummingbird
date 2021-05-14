# -*- coding: utf-8 -*-
# @Time    : Copyright 2020/11/19 17:05
# @Author  : ywg663@qq.com
# @File    : securies.py
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

from sqlalchemy import Column, Integer, Float, String, DateTime, Date, BigInteger, SmallInteger
from .common import Base

''' 标的 '''
class Security(Base):
    """
    证券
    """
    __tablename__ = 'securities'

    security = Column(String(20), primary_key=True)
    '''证券代码'''
    display_name = Column(String(20))
    '''显示名称'''
    name = Column(String(20))
    '''简称'''
    start_date = Column(Date)
    '''上市日期'''
    end_date = Column(Date)
    '''退市日期'''
    type = Column(String(16))
    '''类型，股票，ETF，基金...'''
    status = Column(Integer)
    '''状态'''
    update_date = Column(Date)
    '''信息更新时间'''
    def __init__(self, security, display_name, name, start_date, end_date, stype, status, update_date):
        """
        初始化
        :param security:
        :param display_name:
        :param name:
        :param start_date:
        :param end_date:
        :param stype:
        :param status:
        :param update_date:
        """
        self.security = security
        self.display_name = display_name
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.type = stype
        self.status = status
        self.update_date = update_date


class KlineDay(Base):
    """
    日线行情
    """
    __tablename__ = "kline_day"
    '''表名'''
    security = Column(String(20), primary_key=True)
    '''证券代码'''
    kday = Column(Date, primary_key=True)
    '''交易日期'''
    open = Column(Float)
    '''开盘价'''
    close = Column(Float)
    '''收盘价'''
    low = Column(Float)
    '''最低价'''
    high = Column(Float)
    '''最高价'''
    volume = Column(BigInteger)
    '''交易数量'''
    money = Column(Float)
    '''交易额'''
    factor = Column(Float)
    '''复权因子'''
    high_limit = Column(Float)
    '''涨停最高价'''
    low_limit = Column(Float)
    '''跌停最低'''
    avg = Column(Float)
    '''均价'''
    pre_close = Column(Float)
    '''前一个结束价'''
    paused = Column(SmallInteger)
    '''是否暂停交易'''
    update_date = Column(Date)
    '''更新日期'''
    status = Column(Integer)
    '''状态'''
    def __init__(self, security, kday, close, status, avg, volume, money):
        """
        构造函数
        :param security:
        :param kday:
        :param close:
        :param status:
        :param avg:
        :param volume:
        :param money:
        """
        self.security = security
        self.kday = kday
        self.close = close
        self.status = status
        self.avg = avg
        self.volume = volume
        self.money = money


class Industries(Base):
    """
    行业分类信息
    """
    __tablename__ = "industries"
    '''表名'''
    type = Column(String(20), primary_key=True)
    '''分类类别，申万，聚宽，国证'''
    index = Column(String(20), primary_key=True)
    '''分类代码'''
    name = Column(String(20))
    '''行业名称'''
    start_date = Column(Date)
    '''行业开始日期'''
    update_date = Column(Date)
    '''行业结束日期'''
    status = Column(Integer)
    '''状态'''
    def __init__(self, stype, index, name, start_date, update_date, status):
        """
        初始化
        :param stype:
        :param index:
        :param name:
        :param start_date:
        :param update_date:
        :param status:
        """
        self.status = status
        self.type = stype
        self.index = index
        self.name = name
        self.start_date = start_date
        self.update_date = update_date
        self.status = status

class IndicatorDay(Base):
    """
    指标数据
    """
    __tablename__ = "indicator_day"
    security = Column(String(20), primary_key=True)
    '''证券代码'''
    kday = Column(Date)
    '''交易日期'''
    open = Column(Float)
    '''开盘价'''
    close = Column(Float)
    '''收盘价'''
    low = Column(Float)
    '''最低价'''
    high = Column(Float)
    '''最高价'''
    volume = Column(BigInteger)
    '''交易量'''
    money = Column(Float)
    '''交易金额'''
    high_limit = Column(Float)
    '''涨停价'''
    low_limit = Column(Float)
    avg = Column(Float)
    '''均价'''
    ma20 = Column(Float)
    '''均线20值'''
    ma60 = Column(Float)
    '''均线60值'''
    ma120 = Column(Float)
    '''均线120值'''
    roc = Column(Float)
    '''roc指标值'''
    sroc = Column(Float)
    '''sroc指标值'''
    kd20 = Column(Float)
    '''差值比率'''
    kd60 = Column(Float)
    '''60前天价差值比率'''
    kd120 = Column(Float)
    '''120前天与今天收盘价差值比率'''
    cs = Column(Float)
    '''收盘价与20日均线减值比率'''
    sm = Column(Float)
    '''20日均线与60日均线减值比率'''
    ml = Column(Float)
    '''60日均线与与120日均线减值比率'''
    change_pct = Column(Float)
    '''涨跌幅'''
    day_pct = Column(Float)
    '''日内振幅'''
    rel20 = Column(Float)
    '''与中证800涨跌之差'''
    update_date = Column(Date)
    '''更新日期'''
    status = Column(Integer)
    '''状态'''
    i_pct20 = Column(Float)
    '''中证800，20日涨跌幅'''
    money20 = Column(Float)
    '''20日成交额均值'''
    change_pct20 = Column(Float)
    '''20日涨跌均值'''
    kst = Column(Float)
    '''kst指标之kst值'''
    sig = Column(Float)
    '''kst指标之sig值'''
    security_type = Column(Integer)
    '''证券类型'''

class Sw1DailyPrice(Base):
    """
    申万行业行情
    """
    __tablename__ = "sw1_daily_price"
    code = Column(String(20), primary_key=True)
    '''行业代码'''
    date = Column(Date, primary_key=True)
    '''日期'''
    name = Column(String(20))
    '''行业名称'''
    open = Column(Float)
    '''开盘价'''
    close = Column(Float)
    '''收盘价'''
    low = Column(Float)
    '''最低价'''
    high = Column(Float)
    '''最高价'''
    volume = Column(Integer)
    '''交易量'''
    money = Column(Float)
    '''交易金额'''
    change_pct = Column(Float)
    '''涨跌幅'''
    id = Column(Integer)
    '''id'''
    update_date = Column(Date)
    '''更新日期'''
    status = Column(Integer)
    '''状态'''

    def __init__(self, code, date, name, sopen, close, low, high, volume, money, change_pct, update_date, status):
        """
        初始化
        :param code:
        :param date:
        :param name:
        :param sopen:
        :param close:
        :param low:
        :param high:
        :param volume:
        :param money:
        :param change_pct:
        :param update_date:
        :param status:
        """
        self.code = code
        self.date = date
        self.name = name
        self.open = sopen
        self.close = close
        self.low = low
        self.high = high
        self.volume = volume
        self.money = money
        self.change_pct = change_pct
        self.update_date = update_date
        self.status = status
