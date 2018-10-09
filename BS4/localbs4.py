#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

try:
    html = open('','r')
    bsObj = BeautifulSoup(html.read(),"html.parser")
    allinfo = bsObj.findAll('input',{'cet':re.compile(r'(Text|DateTime)')})
    for info in allinfo:
        #print(info)
        try:
            print(info["title"]+':'+info["value"])
        except KeyError:
            print(info["title"]+':')
except BaseException as e:
    print(e)
finally:
    html.close()
