# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/19 14:37
# @Author  : ywg663@qq.com
# @File    : get_date.py
# @Software: TA
# @description: 实现参考了 https://www.huaweicloud.com/articles/8f0b1cbae8f64c402d733916e56e1715.html
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
# -*- coding: UTF-8 -*-

import datetime
from datetime import timedelta
import pandas as pd
from enum import Enum, unique
import jqdatasdk as jq
import mysql.connector
import pymysql
from jqdatasdk import *
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import config.setup as setup
import utils.flog as flog
from data.Modules.securies import KlineDay
from data.Modules.securies import Security as YSecurity
from data.Modules.setting import Setting
from cacheout import Cache

jq_scurity_types = ['stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof', 'fja', 'fjb', 'open_fund',
                    'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund']
'''标的类型列表，跟JQData统一'''


@unique
class SecurityType(Enum):
    """
    标的类型 + 自自定义其他类型
    """
    Stock = 0
    '''
    个股
    '''
    Fund = 1
    '''
    基金
    '''
    Index = 2
    '''
    指数
    '''
    Futures = 3
    Options = 4
    Etf = 5
    '''
    ETF基金
    '''
    Lof = 6
    Fja = 7
    Fjb = 8
    Open_fund = 9
    Bbond_fund = 10
    Stock_fund = 11
    QDII_fund = 12
    Money_market_fund = 13
    Mixture_fund = 14
    SW = 15
    '''
    申万行业
    '''


@unique
class SecurityStatus(Enum):
    """
    标的状态
    """
    Strong = 0
    '''由弱转强'''
    Weakness = 1
    '''由强转弱'''
    StrongKeep = 2
    '''持续强势'''
    WeaknessKeep = 3
    '''持续弱势'''


@unique
class DownMod(Enum):
    """
    数据下载方式
    """
    Increment = 0
    '''
    增量
    '''
    Full = 1
    '''
    全量
    '''


@unique
class ScreenState(Enum):
    """选股状态"""
    Nothing = 0
    '''无变化'''
    Add = 1
    '''新增选'''
    Reject = 2
    '''剔除'''


class BasicData:
    """
        获取存储用于计算的基础数据，如股票，ETF，行情，行业分类。。。
        可以引用其他数据源进行操作，底层进行替换
    """

    def __init__(self, data_config_file="dataBase.yaml"):
        """
        初始化
        """
        self.mysql_conf = setup.MySql(data_config_file)
        self.engine = create_engine(self.mysql_conf.PyMySql_STR)
        self.db_session_factory = sessionmaker(bind=self.engine)
        self.app = setup.App()
        self.cache = Cache()

    def get_session(self):
        return self.db_session_factory()

    @staticmethod
    def get_axr_date(security):
        """
        获取指字标的的除权日期列表
        :param security:
        :return:
        """
        df = jq.finance.run_query(query(finance.STK_XR_XD.code, finance.STK_XR_XD.a_xr_date)
                                  .filter(finance.STK_XR_XD.code == security, finance.STK_XR_XD.a_xr_date.isnot(None))
                                  .order_by(finance.STK_XR_XD.a_xr_date.desc()).limit(5))
        datas = df['a_xr_date'].tolist()
        return datas

    def get_trade_days(self):
        """
        获取最近10天交易日
        :return:
        """
        if self.cache.get('trade_days') is None:
            self.cache.set('trade_days', jq.get_trade_days(end_date=datetime.datetime.now(), count=10), 21600)
        return self.cache.get('trade_days')

    def get_all_securities(self, types=[]):
        """
        获取全部股票信息,更新标的信息，没有的添加，有的看其是否已经被st,退市，进行更新。
        """
        flog.FinanceLoger.logger.info('证券信息更新开始...!')
        now = datetime.datetime.now()
        db_session = self.db_session_factory()
        list_screening = db_session.query(Setting).filter(Setting.name == 'security.down.last').first()
        list_date = datetime.datetime.strptime(list_screening.value, '%Y-%m-%d')
        day_count = (now - list_date).days
        if day_count < self.app.conf.conf['Update']['SecuritiesInterval']:
            return

        for x in types:
            res = jq.get_all_securities(types=x, date=None)
            i = 0
            for index, security in res.iterrows():
                s = index
                security_temp = db_session.query(YSecurity).filter(YSecurity.security == s).first()
                if security_temp:
                    security_temp.security = s
                    security_temp.display_name = security["display_name"]
                    security_temp.name = security['name']
                    security_temp.start_date = security['start_date']
                    security_temp.end_date = security["end_date"]
                    security_temp.update_date = now.date()
                else:
                    security_temp = YSecurity(security=s, display_name=security["display_name"], name=security["name"],
                                              start_date=security["start_date"], end_date=security["end_date"],
                                              stype=security["type"], status=0, update_date=now.date())
                    db_session.add(security_temp)
                db_session.commit()
                i += 1
            flog.FinanceLoger.logger.info('本次标[{}]的更新完成，共更新{}条!'.format(x, i))
        list_screening.value = now.date().strftime('%Y-%m-%d')
        db_session.commit()
        db_session.close()
        flog.FinanceLoger.logger.info('证券信息更新结束...!')
        return

    def execute_sql(self, sql):
        """
        执行指定的sql语句
        :param sql:
        :return:
        """
        try:
            db_session = self.db_session_factory()
            db_session.execute(sql)
            db_session.commit()
        except Exception as e:
            flog.FinanceLoger.logger.error('excute sql:{0} error e-{1}'.format(sql, e))
            db_session.rollback()
        finally:
            db_session.close()
        flog.FinanceLoger.logger.debug('excute sql:{}'.format(sql))
        return

    def clean_data_by_table(self, table_name):
        """
        清理标的数据表
        """
        sql = 'truncate table {}'.format(table_name)
        self.execute_sql(sql)
        flog.FinanceLoger.logger.info('truncate table {} success'.format(table_name))
        return

    def get_security_prices(self, security):
        """
        获取数据库中指定标的的行情数量和最后行情日期
        :param security:
        :return: tuple 总的行情数量 k_count, 最后行情日 last_trade_k
        """
        db_session = self.db_session_factory()
        k_count = db_session.query(func.count(KlineDay.kday)).filter(KlineDay.security == security).scalar()
        last_trade_k = db_session.query(KlineDay).filter(KlineDay.security == security).order_by(
            KlineDay.kday.desc()).first()
        db_session.close()
        return k_count, last_trade_k

    def get_day_price(self, security):
        """
        获取单只股票的指定时间段的前复权日线数据,可以单独执行
        """
        # today
        now = datetime.datetime.now()
        last_year_day = now - datetime.timedelta(days=366)
        scount, last_k = self.get_security_prices(security)
        xr_datas = self.get_axr_date(security)
        start_date = last_year_day.date()  # 默认下载一年数据

        if 180 > scount > 0:
            sql = "delete from kline_day where security = '{0}' ".format(security)
            self.execute_sql(sql)
        elif scount >= 180 and last_k is not None:
            local_data_date = last_k.kday
            start_date = local_data_date + datetime.timedelta(days=1)

        trade_days = self.get_trade_days()
        end_date = trade_days[-1]
        if now.date() == end_date:
            if now.hour < 15:
                end_date = end_date + datetime.timedelta(days=-1)
        if start_date > end_date:
            return

        # 除权日，全量下载
        if end_date in xr_datas:
            if scount > 0:
                sql = "delete from kline_day where security = '{0}' ".format(security)
                self.execute_sql(sql)
            start_date = last_year_day.date()

        res = jq.get_price(security, start_date=start_date, end_date=end_date, frequency='daily',
                           fields=['open', 'close', 'high', 'low', 'volume', 'money', 'factor', 'high_limit',
                                   'low_limit', 'avg', 'pre_close', 'paused'],
                           skip_paused=True, fq='pre')
        # 跳过停牌日行情，可能会下载不到数据
        if res.empty:
            return

        '''增加股票代码列'''
        res['security'] = security
        res['update_date'] = now.date()
        try:
            pymysql.install_as_MySQLdb()
            mysqlconnect = create_engine(self.mysql_conf.MYSQL_CON_STR)
            res.to_sql(name="kline_day", con=mysqlconnect, if_exists='append', index=True, index_label='kday',
                       chunksize=1000)
            new_count, _ = self.get_security_prices(security)
            if new_count > 240:
                # 清理老数据
                sql = "delete from kline_day where security = '{0}' and kday <= '{1}'".format(security,
                                                                                              str(last_year_day))
                self.execute_sql(sql)
        except Exception as e:
            flog.FinanceLoger.logger.error("更新行情时出错，标的：{}，错误信息：{}".format(security, e))
        flog.FinanceLoger.logger.debug("更新了行情，标的：{}".format(security))
        return

    @staticmethod
    def verfiy_finance(security):
        """
        验证基本面
        :param security:
        :return: bool 验证是否通过
        """
        fund_df = jq.get_fundamentals(query(
            valuation, indicator
        ).filter(
            valuation.code == security
        ))

        fund_df = fund_df.fillna(value=100)
        if fund_df is None or fund_df.empty:
            flog.FinanceLoger.logger.info("标的{},获取不到财务数据".format(security))
            return False

        # and fund_df.iloc[0]["turnover_ratio"] > 0.01 and fund_df.iloc[0]["roe"] > 0.01 \
        #     and fund_df.iloc[0]["net_profit_margin"] > 5
        if fund_df.iloc[0]["market_cap"] > 80 and fund_df.iloc[0]["circulating_market_cap"] > 50:
            return True
        # fund_df.to_csv(security + '.csv')
        return False

    @staticmethod
    def get_finance(code=None):
        """
        获取指定财务条件的标的列表
        :return:
        """
        if not (code is None):
            q = query(
                valuation, indicator
            ).filter(
                valuation.code == code
            )
        else:
            q = query(
                valuation.code, valuation.market_cap, valuation.circulating_market_cap, indicator.roe,
                indicator.gross_profit_margin
            ).filter(
                valuation.market_cap > 80,
                valuation.circulating_market_cap > 50,
                valuation.turnover_ratio > 0.1,
                indicator.roe > 0.05
            ).order_by(
                # 按市值降序排列
                valuation.market_cap.desc()
            )
        # 取某行，某列的值 market_cap = df.iloc[0]['market_cap']
        return jq.get_fundamentals(q)

    def get_all_price(self, stype):
        """
        遍历全部股票,获取日线数据，当天更新，市场结束即更新
        :param stype: 标的类型 count 数量，获取120均线，必须最晚时间在240个行情数据
        :return:
        """
        if stype is None:
            return
        flog.FinanceLoger.logger.info("开始全部标的价格获取...")
        '''从本地数据库里获取全部股票信息,代码,上市日期,退市日期'''
        db_session = self.db_session_factory()
        for s in stype:
            securities = db_session.query(YSecurity).filter(YSecurity.type == s, YSecurity.status == 1).all()
            j = 0
            '''循环取出每个标的的行情数据'''
            for security in securities:
                self.get_day_price(security=security.security)
                j += 1
            flog.FinanceLoger.logger.info("获取了指定标的类型{}的数据,共计拉取了{}条符合条件的价格信息".format(s, j))
        db_session.close()
        return

    def get_industries_store(self, name='jq_l2', date=None):
        """
        获取行业信息并存入数据
        :param name:
        :param date:
        :return:
        """
        res = jq.get_industries(name=name, date=None)

        '''增加类别列,行业分类者，聚宽，申万，国证'''
        res['type'] = name

        '''DataFrame入库'''
        pymysql.install_as_MySQLdb()
        mysqlconnect = create_engine(self.mysql_conf.MYSQL_CON_STR)
        res.to_sql(name='industries', con=mysqlconnect, if_exists='append',
                   index=True, index_label='index', chunksize=1000)
        flog.FinanceLoger.logger.info('所有行业信息已经保存成功')
        return

    def clean_industries(self):
        """
        清理行业信息表，表信息由于上游更新定期进行重置
        :return:
        """
        self.clean_data_by_table('industries')

    def get_swl1_daliy_price(self, date=None):
        """
        获取申万一级行业日行情
        申万行业行情每天18：00更新，这个最好是第二天下载
        :return:
        """
        '''从本地数据库里获取全部股票信息,代码,上市日期,退市日期'''
        sql = "select * from industries i2 where i2.`type` = 'sw_l1' "
        industries = self.get_df_by_sql(sql)
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')

        j = 0
        for i in range(0, len(industries)):
            industry = industries.iloc[i]['index']
            s = industry.decode("utf-8")

            res = finance.run_query(
                query(finance.SW1_DAILY_PRICE).filter(finance.SW1_DAILY_PRICE.code == s and finance.SW1_DAILY_PRICE.date
                                                      <= date).order_by(
                    finance.SW1_DAILY_PRICE.date.desc()).limit(1))

            '''DataFrame入库'''
            pymysql.install_as_MySQLdb()
            mysqlconnect = create_engine(self.mysql_conf.MYSQL_CON_STR)
            try:
                res.to_sql(name='sw1_daily_price', con=mysqlconnect, if_exists='append', index=False, chunksize=1000)
                j += 1
            except Exception as e:
                flog.FinanceLoger.logger.error("获取申万一级行业的行情，存储数据库时出错，标的：{},出错信息：{}".format(s, e))
        flog.FinanceLoger.logger.info("获取申万一级行业的行情信息,总计拉取了{}条符合条件的标的".format(j))
        return

    def screening_security(self, types):
        """
        筛选stock入库，置标识字段status为 1,标记后，下载行情时，进行判断 ，如果不足240的补足
        :return:
        """
        # 每30天执行一次基本面选标策略
        flog.FinanceLoger.logger.info('证券筛选更新开始...!')
        if types is None:
            return
        now = datetime.datetime.now()
        half_year_day = now - datetime.timedelta(days=180)
        db_session = self.db_session_factory()
        list_screening = db_session.query(Setting).filter(Setting.name == 'security.status.update.date').first()
        list_date = datetime.datetime.strptime(list_screening.value, '%Y-%m-%d')
        day_count = (now - list_date).days
        if day_count < self.app.conf.conf['Update']['SecuritiesInterval']:
            return

        for x in types:
            i, j = 0, 0
            securities = db_session.query(YSecurity).filter(YSecurity.type == x).all()
            for security in securities:
                flag_comm = security.end_date > datetime.datetime.now().date() and 'ST' not in security.display_name \
                            and security.start_date < half_year_day.date()
                flag = False
                # 不同标的的入选标识
                if x == 'stock':
                    flag = self.verfiy_finance(security.security) and flag_comm
                else:
                    flag = flag_comm
                # 总的入选标识
                if security.status == 1:
                    if flag:
                        state = ScreenState.Nothing
                    else:
                        state = ScreenState.Reject
                elif security.status == 0:
                    if not flag:
                        state = ScreenState.Nothing
                    else:
                        state = ScreenState.Add

                # 依据不同的入选标识，没有改变，增选，剔除，做不同的动作
                if state == ScreenState.Nothing:
                    continue
                elif state == ScreenState.Add:
                    security.status = 1
                    db_session.commit()
                    j += 1
                    # 下载240天数据
                    self.get_day_price(security.security)
                    flog.FinanceLoger.logger.debug("标的 {} - 代码 {}被增选为优质标的".format(security.display_name,
                                                                                  security.security))
                elif state == ScreenState.Reject:
                    security.status = 0
                    db_session.commit()
                    # 清理行情数据
                    self.execute_sql("delete from kline_day where `security` = '{}' ".format(security.security))
                    self.execute_sql("delete from indicator_day where `security` = '{}' ".format(security.security))
                    flog.FinanceLoger.logger.debug("标的 {} - 代码 {}被删除优质标的".format(security.display_name,
                                                                                 security.security))
                    i += 1
                    db_session.commit()
            flog.FinanceLoger.logger.info("对于标的类型{}共有{}被剔除,总共有{}被选择........".format(x, i, j))
        list_screening.value = now.strftime('%Y-%m-%d')
        db_session.commit()
        db_session.close()
        flog.FinanceLoger.logger.info('证券筛选更新结束...!')
        return

    @staticmethod
    def get_industry_by_security(security):
        """
        stock所属版块行业信息
        :param security:
        :return:
        """
        d = jq.get_industry(security)
        return (d[security]['sw_l1']['industry_name'], d[security]['sw_l2']['industry_name'],
                d[security]['sw_l3']['industry_name'])

    def down_data(self, types):
        """
        自动执行下载数据
        :return:
        """
        self.get_all_price(types)
        # self.get_swl1_daliy_price(now)

    def clean_indicator(self):
        """
        清理指标数据表
        :return:
        """
        self.clean_data_by_table('indicator_day')

    def get_df_by_sql(self, sql):
        """
        通过指定的sql获取到dataframe
        :param sql:
        :return: dataframe
        """
        # 公用时这里可能有隐患，数据库及时打开和关闭的问题。
        # self.engine.open()
        # self.engine.close()
        df = pd.read_sql(sql, self.engine, index_col=None, coerce_float=True, params=None, parse_dates=None,
                         columns=None, chunksize=None)
        return df


if __name__ == "__main__":
    pass
