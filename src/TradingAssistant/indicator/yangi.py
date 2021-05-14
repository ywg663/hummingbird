# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/20 20:16
# @Author  : ywg663@qq.com
# @File    : yangi.py
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

import mysql.connector
import pandas as pd
import pymysql
import talib
from jqdatasdk import *
from sqlalchemy import and_
from sqlalchemy import create_engine
import config.setup as setting
import data.data_base as bdata
import utils.flog as flog
from data.Modules.securies import Security as YSecurity


class Composite:
    """
    指标计算
    """

    def __init__(self):
        """
        指标计算，初始化
        """
        self.mysql = setting.MySql("dataBase.yaml")
        self.base_data = bdata.BasicData("dataBase.yaml")

    def calculate_securities(self, security_types=None):
        """
        标的指标计算
        :param security_types: 标的类型
        :return: 执行动作不返回结果
        """
        flog.FinanceLoger.logger.info("开始指标计算...")
        # 清理原来指标计算结果
        self.base_data.clean_indicator()
        if security_types is None:
            return
        db_session = self.base_data.get_session()
        for c in security_types:
            securities = db_session.query(YSecurity). \
                filter(and_(YSecurity.status == 1, YSecurity.type == bdata.jq_scurity_types[c.value])).all()
            '''循环取出每个标的的行情数据'''
            j = 0
            for security in securities:
                k_count, last_trade_k = self.base_data.get_security_prices(security.security)
                # 对于交易数据少于230个（可能是下载数据有误，或中间停牌，退市等未及时清理导致走到计算这一步，理论上前面过滤后不到到这一步）
                # 或行情最后日期不是要计算的最后一个交易日，则退出计算。
                if k_count < 150:
                    flog.FinanceLoger.logger.info('计算标的{}时，行情数少150或最后一个交易日不是市场交易日'.format(security.security))
                    continue
                self.calculate(security=security.security, security_type=c)
                j += 1
            flog.FinanceLoger.logger.info("当前计算的{}类型指标，共计完成{}".format(c.name, j))
        db_session.close()

    def calculate_k906(self):
        if self.base_data.cache.get('df_k960') is None:
            mdbconn = mysql.connector.connect(user=self.mysql.USER_NAME, password=self.mysql.PWD,
                                              database=self.mysql.DATABASENAME, use_unicode=True,
                                              host=self.mysql.HOST,
                                              auth_plugin='mysql_native_password')

            sql1 = "SELECT `close`,`kday` FROM ta.kline_day where security = '000906.XSHG'"
            kdays906 = pd.read_sql(sql1, mdbconn, index_col='kday', coerce_float=True, params=None, parse_dates=None,
                                   columns=None, chunksize=None)

            kdays906["change_pct"] = (kdays906['close'].shift(1) - kdays906['close']) / kdays906['close'] * 100
            kdays906["i_pct20"] = kdays906['change_pct'].rolling(20).mean()  # 需要添加
            kdays906 = kdays906.drop(['change_pct'], axis=1)
            kdays906 = kdays906.drop(['close'], axis=1)
            # kdays906.to_csv("k906.csv")
            self.base_data.cache.set('df_k960', kdays906, 3600)  # 缓存一小时
        return self.base_data.cache.get('df_k960')

    def calculate(self, security, security_type=bdata.SecurityType.Stock):
        """
        均线计算
        :return:
        """
        flog.FinanceLoger.logger.debug("开始{}指标计算".format(security))
        mdbconn = mysql.connector.connect(user=self.mysql.USER_NAME, password=self.mysql.PWD,
                                          database=self.mysql.DATABASENAME, use_unicode=True,
                                          host=self.mysql.HOST,
                                          auth_plugin='mysql_native_password')

        kdays906 = self.calculate_k906()
        if kdays906 is None:
            return

        sql = "SELECT `security`, `kday`, `open`, `close`, low, high, volume, money, high_limit, low_limit," \
              " avg FROM ta.kline_day where security = '{}' and close <> 0".format(security)
        kdays = pd.read_sql(sql, mdbconn, index_col='kday', coerce_float=True, params=None, parse_dates=None,
                            columns=None, chunksize=None)

        kdays.dropna(axis=0, how='any')
        kdays['security_type'] = security_type.value

        # 分别计算5日、20日、60日的移动平均线
        ma_list = [setting.MA.MA20, setting.MA.MA60, setting.MA.MA120]
        # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
        for ma1 in ma_list:
            kdays['ma' + str(ma1)] = kdays['close'].rolling(ma1).mean()
        # 计算指数平滑移动平均线EMA
        for ma2 in ma_list:
            kdays['EMA_' + str(ma2)] = pd.DataFrame.ewm(kdays['close'], span=ma2).mean()

        '''SROC计算'''
        kdays.dropna(axis=0, how='any')
        kdays['roc'] = talib.ROC(kdays['close'], timeperiod=setting.SRoc.ROC_LEN)
        kdays['EMA_13'] = pd.DataFrame.ewm(kdays['close'], span=setting.SRoc.EMA_LEN).mean()
        kdays['sroc'] = talib.ROC(kdays['EMA_13'], setting.SRoc.SROC_LEN)
        kdays = kdays.drop(['EMA_13'], axis=1)

        kdays['kst'] = self.kst(kdays['close'])
        kdays['sig'] = self.sig(kdays['kst'])

        kdays["kd20"] = (kdays["close"] - kdays["close"].shift(20)) / kdays["close"].shift(20) * 100
        kdays["kd60"] = (kdays["close"] - kdays["close"].shift(60)) / kdays["close"].shift(60) * 100
        kdays["kd120"] = (kdays["close"] - kdays["close"].shift(120)) / kdays["close"].shift(120) * 100

        '''乖离计算'''
        kdays['cs'] = (kdays['close'] - kdays['EMA_20']) / kdays['EMA_20'] * 100
        kdays['sm'] = (kdays['EMA_20'] - kdays['EMA_60']) / kdays['EMA_60'] * 100
        kdays['ml'] = (kdays['EMA_60'] - kdays['EMA_120']) / kdays['EMA_120'] * 100
        kdays = kdays.drop(['EMA_20'], axis=1)
        kdays = kdays.drop(['EMA_60'], axis=1)
        kdays = kdays.drop(['EMA_120'], axis=1)

        '''涨幅计算'''
        kdays["change_pct"] = (kdays["close"].shift(1) - kdays["close"]) / kdays["close"] * 100
        kdays["change_pct20"] = kdays["change_pct"].rolling(20).mean()
        kdays["day_pct"] = (kdays["high"] - kdays["low"]) / kdays["low"] * 100

        '''20日均成交额'''
        kdays["money20"] = kdays["money"].rolling(20).mean()

        # kdays['security'] = kdays['security'].apply(lambda x: x.decode("utf-8"))
        # kdays906['security'] = kdays906['security'].apply(lambda x: x.decode("utf-8"))

        df = pd.merge(kdays, kdays906, how='left', on='kday')
        df["rel20"] = df["change_pct20"] - df["i_pct20"]
        kdays.dropna(axis=0, how='any', inplace=True)

        # 将数据按照交易日期从近到远排序
        # kdays.sort_values(by='kdate')
        '''DataFrame入库'''
        df = df.tail(20)
        pymysql.install_as_MySQLdb()
        mysqlconnect = create_engine(self.mysql.MYSQL_CON_STR)
        try:
            df.to_sql(name='indicator_day', con=mysqlconnect, if_exists='append', index=True, chunksize=1000)
        except Exception as e:
            df.to_csv(security + ".csv")
            flog.FinanceLoger.logger.error("保存至指标数据库时出错，标的：{},出错信息：{}".format(security, e))
        flog.FinanceLoger.logger.debug("完成{}指标计算".format(security))
        # df.to_csv('{}

    @staticmethod
    def smaroc(price, roclen, smalen):
        """
        KST自定义用于计算KST的函数
        :param price:
        :param roclen:
        :param smalen:
        :return:
        """
        return talib.MA(talib.ROC(price, timeperiod=roclen), timeperiod=smalen)

    def kst(self, price):
        """
        KST计算
        :param price:
        :return:
        """
        return self.smaroc(price, 10, 10) + 2 * self.smaroc(price, 15, 10) + 3 * self.smaroc(price, 20, 10) + \
               4 * self.smaroc(price, 30, 15)

    @staticmethod
    def sig(kst):
        """
        KST的sig计算
        """
        return talib.MA(kst, timeperiod=9)


if __name__ == "__main__":
    # jq_data = bdata.JqFinanceData()
    # jq_data.log()
    ma = Composite()
    ma.calculate_securities([bdata.SecurityType.Index])
    # jq_data.log_out()
