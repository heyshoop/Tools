#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = '账号'
password = '密码'
to_addr = '目标邮箱'

def mail():
    ret = True
    try:
        for i in range(10):
            msg = MIMEText('%d只青蛙%d张嘴,%d只眼睛%d条腿' % (i,i,2*i,4*i), 'plain', 'utf-8')
            msg['From'] = _format_addr('一个无聊的人 <%s>' % from_addr)
            msg['To'] = _format_addr('wbb<%s>' % to_addr)
            msg['Subject'] = Header('数青蛙喽', 'utf-8').encode()

            server = smtplib.SMTP('smtp.163.com', 25)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())

    except Exception:
        ret = False
    finally:
        server.quit()

    return ret


ret = mail()
if ret:
    print("发送成功")
else:
    print("发送失败")


