# -*- coding: utf-8 -*-
# @Time    : Copyright 2020/10/28 16:24
# @Author  : ywg663@qq.com
# @File    : email.py
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

from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import utils.flog as fg
import config.setup as setting


class SendEmail(object):
    """
    发送email的工具类
    """
    def __init__(self):
        """
        初始化
        """
        self.conf = setting.Configuration("email.yaml").conf
        '''用户信息'''
        self.from_addr = self.conf["from"]["email"]
        '''腾讯QQ邮箱或腾讯企业邮箱必须使用授权码进行第三方登陆'''
        self.password = self.conf["from"]["password"]
        '''腾讯服务器地址smtp.exmail.qq.com'''
        self.smtp_server = self.conf["from"]["server"]
        self.server = smtplib.SMTP_SSL(self.smtp_server, self.conf["from"]["port"])
        self.msg = MIMEText('test', "html", 'utf-8')

    def login_email_ser(self):
        """
        登陆服务器,服务端配置，账密登陆
        :return:
        """
        self.server.login(self.from_addr, self.password)

    @staticmethod
    def format_addr(name, addr):
        """
        发件人收件人信息格式化 ，可防空,固定用法不必纠结，我使用lambda表达式进行简单封装方便调用
        :param name:
        :param addr:
        :return:
        """
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self, tomail, subject, content):
        """
        内容初始化，定义内容格式（普通文本，html）
        :param tomail:
        :param subject:
        :param content:
        :return:
        """
        fg.FinanceLoger.logger.debug('准备发送邮件...')
        '''传入昵称和邮件地址# 腾讯邮箱可略# 腾讯邮箱可略'''
        self.msg = MIMEText(content, "html", 'utf-8')
        self.msg['From'] = self.format_addr('蜂鸟行情计算系统', self.from_addr)
        self.msg['To'] = self.format_addr('订阅人', ','.join(tomail))
        '''邮件标题'''
        self.msg['Subject'] = Header(subject, 'utf-8').encode()
        self.login_email_ser()
        self.server.sendmail(self.from_addr, tomail, self.msg.as_string())
        '''发送邮件及退出发送地址需与登陆的邮箱一致'''
        self.server.quit()
        fg.FinanceLoger.logger.debug("发送邮件至至：{}".format(tomail))


def test_send_email():
    """
    测试发送email的功能
    :return:
    """
    conf = setting.Configuration("email.yaml").conf
    send_email = SendEmail()
    with open("../conf/email-template.html", "r", encoding="utf-8") as f:  # 打开文件
        data = f.read()  # 读取文件
    mail_content = """\
               <tr align="center">
                    <td>
                        <a href="https://cn.tradingview.com/chart/?symbol=SSE:000027">SZSE:000027</a>
                    </td>
                    <td>
                        深圳能源
                    </td>
                    <td>
                        29.000
                    </td>
                </tr>
               """
    mail_content = data.replace("$content", mail_content)
    send_email.send(tomail=[x["email"] for x in conf["toEmails"]], subject='行情计算日报', content=mail_content)


if __name__ == '__main__':
    test_send_email()

















