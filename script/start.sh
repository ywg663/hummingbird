#!/bin/sh
#author: yang
cur_dateTime=$(date "+%Y-%m-%d %H:%M:%S")
echo $cur_dateTime "蜂鸟行情计算系统启动..." >> /root/hummingbird/src/TradingAssistant/log/start.log
cd /root/hummingbird/src/TradingAssistant/
 . /usr/bin/FINANCE/bin/activate
nohup python3 main.py >/dev/null 2>&1 &
