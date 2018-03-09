#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen,HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen("http://www.baidu.com")
    bsObj = BeautifulSoup(html.read(),"html.parser")
    print(bsObj.p)
except HTTPError as e:
    print(e)
else:
    pass


