# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/19 14:37
# @Author  : ywg663@qq.com
# @File    : main.py
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
# schedule.every(10).minutes.do(program.run)
# schedule.every().hour.do(program.run)
# schedule.every().day.at("10:30").do(program.run)
# schedule.every(5).to(10).days.do(program.run)
# schedule.every().monday.do(program.run)
# schedule.every().wednesday.at("13:15").do(program.run)
# -*- coding: UTF-8 -*-

import datetime
import time
import schedule
import data.data_base as bdata
import data.provide_jq as pjq
import indicator.yangi as dev
import utils.flog as floger
from data.Modules.setting import Setting
from strategy.yang import Potential


class Program:
    """
    主程序
    """

    def __init__(self):
        self.jqdata = pjq.JqFinanceData()
        '''
        聚宽数据源
        '''
        self.base_data_get = bdata.BasicData()
        self.composite = dev.Composite()
        self.wl = Potential()

    @staticmethod
    def run():
        """
        程序执行主函数
        :return:
        """
        floger.FinanceLoger.logger.info("蜂鸟行情系统启动...")
        program = Program()
        schedule.every().day.at("10:00").do(program.prepare_security)
        schedule.every().day.at("15:30").do(program.down_calculate)
        while True:
            schedule.run_pending()
            time.sleep(1)
        return

    def prepare_security(self):
        """
        准备标的
        :return:
        """
        try:
            self.jqdata.log()
            self.base_data_get.get_all_securities(['stock', 'index', 'etf'])
            self.base_data_get.screening_security(['stock', 'index', 'etf'])
        except Exception as ee:
            floger.FinanceLoger.logger.error('出错了 - {}', ee)
        finally:
            self.jqdata.log_out()

    def down_calculate(self):
        """
        下载行情计算
        :return:
        """
        # 3 下载行情
        try:
            self.jqdata.log()
            now = datetime.datetime.now()
            floger.FinanceLoger.logger.debug("开始获取本地最后计算行情的日期...")
            db_session = self.base_data_get.get_session()
            last_quotes_set = db_session.query(Setting).filter(
                Setting.name == 'strategy.report.last').first()
            floger.FinanceLoger.logger.debug("获取行情计算最后日期：{}".format(last_quotes_set.value))
            last_quotes_day = datetime.datetime.strptime(last_quotes_set.value, '%Y-%m-%d')
            trade_days = self.base_data_get.get_trade_days()
            floger.FinanceLoger.logger.debug("获取行情交易日信息：{}".format(trade_days))
            count = (trade_days[-1] - last_quotes_day.date()).days
            if count <= 0:
                floger.FinanceLoger.logger.info("未执行行情扫描过程...")
                return
            floger.FinanceLoger.logger.debug("准备下载行情数据...")
            self.base_data_get.down_data(types=['stock', 'index', 'etf'])
            # 4 指标计算
            self.composite.calculate_securities([bdata.SecurityType.Stock, bdata.SecurityType.Index,
                                                 bdata.SecurityType.Etf])
            # 5 策略执行
            self.wl.execute([bdata.SecurityType.Stock, bdata.SecurityType.Index, bdata.SecurityType.Etf])
            last_quotes_set.update_time = now
            if now.date() in trade_days and now.hour < 15:
                last_quotes_set.value = trade_days[-2].strftime("%Y-%m-%d")
            else:
                last_quotes_set.value = now.strftime("%Y-%m-%d")
            db_session.commit()
            floger.FinanceLoger.logger.info("程序运行结束...")
        except Exception as error:
            floger.FinanceLoger.logger.error('出错了 - {}', error)
        finally:
            self.jqdata.log_out()
            db_session.close()

    @staticmethod
    def test_schedule():
        floger.FinanceLoger.logger.info("蜂鸟行情系统启动...")
        program = Program()
        schedule.every(2).minutes.do(program.test)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def test():
        # self.jqdata.log()
        # self.base_data_get.down_data()
        # flag = self.base_data_get.verfiy_finance('000001.XSHE')
        # self.base_data_get.down_data()
        # self.base_data_get.clean_indicator()
        # self.composite.calculate_securities([bdata.SecurityType.Stock, bdata.SecurityType.Index])
        # self.wl.execute([bdata.SecurityType.Stock, bdata.SecurityType.Index])
        # klineday = program.base_data_get.db_session.query(KlineDay).filter(KlineDay.security == "000906.XSHG")\
        #     .order_by(KlineDay.kday.desc()).first()
        # print(klineday.kday)
        # self.jqdata.log_out()
        try:
            a = 1 / 0
            floger.FinanceLoger.logger.info('当前值为：{}'.format(a))
        except Exception as e:
            floger.FinanceLoger.logger.error('出错了：{}'.format(e))


if __name__ == '__main__':
    Program.run()
    # Program().test()
    # Program().down_calculate()
    # Program().prepare_security()
