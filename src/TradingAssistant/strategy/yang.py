# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/24 11:15
# @Author  : ywg663@qq.com
# @File    : yang.py
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
import json
import datetime
from jqdatasdk import *
import config.setup as setting
import data.data_base as bdata
import data.db as db
import utils.femail as mil
import utils.flog as flog
import utils.tools as ts
from data.Modules.securies import Security as YSecurity
from data.Modules.setting import Setting


class Potential:
    """
    wolf 策略
    """

    def __init__(self):
        """
        初始化
        """
        self.db_help = db.DbHelp()
        self.base_data = bdata.BasicData()

    def execute(self, security_types):
        """
        筛选
        :return:
        """
        flog.FinanceLoger.logger.info("策略开始执行...")
        d = self.calculate(security_types)
        if d is not None:
            self.handle_report(d)
        flog.FinanceLoger.logger.info("策略执行结束...")

    def calculate(self, security_types=None):
        """
        策略执行，
        1 中证800
        2 个股
        3 指数
        4 行业
        5 ETF
        :return:
        """
        if security_types is None:
            return
        db_session = self.base_data.get_session()
        resuts = {}
        for c in security_types:
            securities = db_session.query(YSecurity).filter(YSecurity.type == bdata.jq_scurity_types[
                c.value], YSecurity.status == 1).all()
            '''准备空目标结果集'''
            resuts[c] = {}
            resuts[c][bdata.SecurityStatus.Strong] = pd.DataFrame()
            resuts[c][bdata.SecurityStatus.Weakness] = pd.DataFrame()
            '''循环取出每个标的的指标数据'''
            j = 0
            k = 0
            for security in securities:
                flog.FinanceLoger.logger.debug("标的{}策略开始执行...".format(security.security))
                in_sql = "select id.*, s2.display_name from indicator_day id left join securities s2 on " \
                         "id.`security` = s2.`security` where id.`security` = '{}' and s2.status = 1 order by " \
                         "id.kday".format(security.security)
                indicators = self.base_data.get_df_by_sql(in_sql)
                # todo 加个停牌的判断
                if indicators.empty or indicators.shape[0] < 20 or indicators.iloc[-1]['ma120'] is None:
                    continue
                # indicators.dropna(axis=0, how='any', inplace=True)
                indicators["sroc10"] = indicators['sroc'].rolling(10).mean()
                indicators["kst10"] = indicators['kst'].rolling(10).mean()
                if c == bdata.SecurityType.Stock:
                    indicators["sroc5"] = indicators['sroc'].rolling(5).mean()

                '''判断筛选'''
                try:
                    if indicators.iloc[-1]['ma20'] < indicators.iloc[-1]['ma60'] < indicators.iloc[-1]['ma120']:
                        continue
                    if (indicators.iloc[-1]['sroc'] > 0 > indicators.iloc[-1]['sroc10']
                        and indicators.iloc[-2]['sroc'] < 0) \
                            or (
                            indicators.iloc[-1]["kst10"] < 0 and indicators.iloc[-2]['kst'] < indicators.iloc[-2]['sig']
                            and indicators.iloc[-1]['kst'] > indicators.iloc[-1]['sig']):
                        j += 1
                        resuts[c][bdata.SecurityStatus.Strong] = resuts[c][bdata.SecurityStatus.Strong] \
                            .append(indicators.iloc[-1])
                        flog.FinanceLoger.logger.debug("标的{}被选中为强势组...".format(security.security))
                    # 可能走弱的个股
                    if ((indicators.iloc[-1]['sroc'] < 0 < indicators.iloc[-2]['sroc'] and
                         indicators.iloc[-2]['sroc10'] > 0) or
                            (indicators.iloc[-2]['kst'] > 0 > indicators.iloc[-1]['kst'] and
                             indicators.iloc[-2]['kst10'] > 0)):
                        k += 1
                        resuts[c][bdata.SecurityStatus.Weakness] = resuts[c][bdata.SecurityStatus.Weakness].append(
                            indicators.iloc[-1])
                        flog.FinanceLoger.logger.debug("标的{}被选中为弱势组...".format(security.security))
                    # 当前强势股，暂不处理
                    '''
                    if c == bdata.SecurityType.Stock and indicators.iloc[-2]['sroc'] > 0 \
                            and indicators.iloc[-1]['sroc5'] > 0:
                        k += 1
                        resuts[bdata.SecurityType.Strong] = resuts[bdata.SecurityType.Strong].append(
                            indicators.iloc[-1])
                    '''
                    # 当前弱势股，暂不处理
                    '''
                    if c == bdata.SecurityType.Stock and indicators.iloc[-1]['sroc'] < 0 \
                            and indicators.iloc[-1]['sroc5'] < 0:
                        m += 1
                        resuts[bdata.SecurityType.Weakness] = resuts[bdata.SecurityType.Weakness].append(
                            indicators.iloc[-1])
                    '''
                except Exception as e:
                    indicators.to_csv("{}.csv".format(security.security))
                    flog.FinanceLoger.logger.error("根据指标筛选标的时出错，错误信息{}".format(e))
                    # return
            if not resuts[c][bdata.SecurityStatus.Strong].empty:
                resuts[c][bdata.SecurityStatus.Strong].sort_values(by=['rel20', 'change_pct20'],
                                                                   ascending=[False, False], inplace=True)
            if not resuts[c][bdata.SecurityStatus.Weakness].empty:
                resuts[c][bdata.SecurityStatus.Weakness].sort_values(by=['change_pct20', 'rel20'], axis=0, ascending=[
                    False, False], inplace=True)
            flog.FinanceLoger.logger.info("当前标的类型：{},根据指标计算，由弱转强:{},由强转弱:{}".format(c, j, k))
        db_session.close()
        return resuts

    def handle_report(self, results, is_send=True):
        """
        发送报告
        :param is_send 是否发送
        :param results: 计算结果集dataframe
        :return:
        """
        flog.FinanceLoger.logger.info("处理策略执行结果，发送报告...")
        conf = setting.Configuration("email.yaml").conf
        hodl_list = []
        db_session = self.base_data.get_session()
        holds = db_session.query(Setting).filter(Setting.name == 'holds').first()
        if holds is not None:
            hodl_list = json.loads(holds.value)
        send_email = mil.SendEmail()
        now = datetime.datetime.now()
        prompts = {bdata.SecurityStatus.Strong: "可能由弱变强", bdata.SecurityStatus.Weakness: "可能由强变弱"}

        if not is_send:
            for k in results:
                for m in k:
                    results[m].to_csv("{0:%Y%m%d%H%M%S-}-{1}.csv".format(now, m.name))
            return
        with open(conf["template"], "r", encoding="utf-8") as f:  # 打开文件
            data = f.read()  # 读取文件
        content = ""
        # securities.to_csv("sss4.csv")
        title = '''
         <div style="line-height: 200%;">
                <span
                    style="font-size: 14px; font-family: Helvetica, Arial, sans-serif; color: black;
                    line-height: 200%;">
                    <strong>订阅者您好: 本次报告基于{0:%Y-%m-%d}最近的交易日标的收盘价，交易额，市直，流通市值等计算生成</strong></span>
                </div>
        '''.format(now)
        m_content = ""
        for k in results:
            for m in results[k]:
                i = 0
                for index, row in results[k][m].iterrows():
                    code = row["security"]
                    style = ''
                    if code in hodl_list:
                        style = 'style="background-color: #ff00003b;"'
                    else:
                        style = 'style="background-color: none;"'
                    tradingview_code = ts.jqcode_to_trading(code)
                    easymoney_code = ts.jqcode_to_eastmoney(code, k == bdata.SecurityType.Index)
                    industry = ""
                    if k is bdata.SecurityType.Stock:
                        industry = ",".join(self.base_data.get_industry_by_security(code))
                        if '非银金融I' in industry or '房地产I' in industry:
                            continue
                    i += 1
                    content += """\
                                   <tr align="center" {7}>
                                        <td>{5}</td>
                                        <td>
                                            <a href="https://cn.tradingview.com/chart/?symbol={0}">{0}</a>
                                        </td>
                                        <td>
                                            <a href="http://quote.eastmoney.com/{6}.html">{1}</a>
                                        </td>
                                        <td>
                                            {2}
                                        </td>
                                        <td>{3}</td>
                                        <td>{4}</td>
                                    </tr>
                                           """.format(tradingview_code, row["display_name"], industry, row["close"],
                                                      row["rel20"], i, easymoney_code, style)

                str_table = """
                    <div style="line-height: 200%;">
                    <span
                        style="font-size: 14px; font-family: Helvetica, Arial, sans-serif; color: black; line-height: 200%;">
                        <strong>{0}-{1}列表</strong></span>
                    </div>
                    <table
                        border="1"
                        cellpadding="0"
                        cellspacing="0"
                        width="100%"
                        class="bmeContainerRow"
                        style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: black; 
                        line-height: 200%; border-collapse:collapse">
                        <tr align="center">
                            <th>序号</th>
                            <th>代码</th>
                            <th>名称</th>
                            <th>行业</th>
                            <th>收盘价</th>
                            <th>相对强度</th>
                        </tr>
                       {2}
                    </table>
                """.format(k.name, prompts[m], content)
                content = ""
                m_content += str_table

        mail_content = data.replace("$content", title + m_content)
        send_email.send(tomail=[x["email"] for x in conf["toEmails"]], subject='行情计算日报', content=mail_content)
        db_session.close()


if __name__ == "__main__":
    pass
