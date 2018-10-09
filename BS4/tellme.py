#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import sys

try:
    username = str(sys.argv()[1]) #输入参数
    html = open('','r')
    bsObj = BeautifulSoup(html.read(),"html.parser")
    allinfo = bsObj.findAll('input',{'cet':re.compile(r'(Text|DateTime)')})
    for info in allinfo:
        try:
            print(info["title"]+':'+info["value"])
        except KeyError:
            print(info["title"]+':')
except BaseException as e:
    print(e)
finally:
    html.close()