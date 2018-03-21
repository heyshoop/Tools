#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 下午2:51
# @Author  : Anchor
# @File    : tellme.py
import getopt
import sys
from pymongo import MongoClient
import re


def tellme():
    try:
        # 这里的 h 就表示该选项无参数，u:表示 u 选项后需要有参数
        opts,args=getopt.getopt(sys.argv[1:],"hu:p:",["help","user=","dept="])
    except getopt.GetoptError as error:
        print(str(error))
        sys.exit(2)

    user = None
    dept = None
    cursor = None
    for key,value in opts:
        if key in ("-h","--help"):
            print("tellme.py -u <用户名> -p <部门名>")
        elif key in ("-u","--user"):
            user = value
        elif key in ("-p","--dept"):
            dept= value

    # 数据库设置
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.hussar
    hussaruser = db.hussar_user
    if(user != None):
        cursor = hussaruser.find({'姓名':re.compile(r'('+user+')')})
        if (dept != None):
            cursor = hussaruser.find({'姓名': re.compile(r'(' + user + ')'),'所在部门': re.compile(r'(' + dept + ')')})

    for emp in cursor:
        print(emp)

if __name__=="__main__":
    tellme()
