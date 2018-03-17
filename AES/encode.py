#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/17 下午4:53
# @Author  : Anchor
# @File    : encode.py
# @Des     : 加密

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from binascii import a2b_hex,b2a_hex
import getpass
import os
import time

#补全字符
def align(str,isKey=False):
    #如果接受的字符串是密码，需要确保其长度为16
    if isKey:
        if len(str) > 16:
            return str[1:16]
        else:
            return align(str)
    #如果接受的字符串是明文或长度不足的密码，确保其长度为16的整数倍
    else:
        zerocount = 16 - len(str) % 16
        for i in range(0,zerocount):
            str = str + '\0'
        return str