# -*- coding: utf-8 -*-
# @Time    : Copyright 2020/10/29 15:17
# @Author  : ywg663@qq.com
# @File    : provide_akShare.py
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
import akshare as ak

stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='1', adjust="qfq")
# stock_zh_a_daily_hfq_df.to_csv('../log/ss.csv', index=False)
print(stock_zh_a_minute_df)

"""
stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol="sh600582", adjust="hfq")
print(stock_zh_a_daily_hfq_df)
"""
