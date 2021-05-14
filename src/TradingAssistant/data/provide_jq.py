# -*- coding: utf-8 -*-
# @Time    : Copyright 2021/3/19 09:41
# @Author  : ywg663@qq.com
# @File    : provide_jq.py
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

import jqdatasdk as jq
import utils.flog as flog
import config.setup as setting

class JqFinanceData:
    """
    聚宽本地数据服务
    """
    def __init__(self):
        """
        初始化
        """
        self.log_status = False
        self.conf = setting.Configuration("data_provide.yaml").conf

    def log(self):
        """
        登录
        :return:
        """
        flog.FinanceLoger.logger.info("准备登录聚宽数据")
        jq.auth(self.conf["JQData"]["UserName"], self.conf["JQData"]["Pwd"])
        self.log_status = jq.is_auth()
        flog.FinanceLoger.logger.info("登录结果：{0}".format(self.log_status))

    def log_out(self):
        """
        退出
        :return:
        """
        if self.log_status:
            jq.logout()


def get_provide_jqdata():
    """
    获取聚宽数据服务
    :return:
    """
    return JqFinanceData()

def test_get_data():
    """
    测试方法
    :return:
    """
    q = jq.query(
        jq.finance.STK_HOLDER_NUM).filter(
        jq.finance.STK_HOLDER_NUM.code == '000002.XSHE',
        jq.finance.STK_HOLDER_NUM.pub_date > '2015-01-01'
    ).limit(10)
    df = jq.finance.run_query(q)
    print(df)


if __name__ == "__main__":
    jq_finance_data = get_provide_jqdata()
    if not jq_finance_data.log_status:
        jq_finance_data.log()
    # test_get_data()
    jq_finance_data.log_out()