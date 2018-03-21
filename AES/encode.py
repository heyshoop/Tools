#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/17 下午4:53
# @Author  : Anchor
# @File    : encode.py
# @Des     : 加密

from Crypto.Cipher import AES
from binascii import b2a_hex
from Crypto.Hash import MD5

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
        zerocount = 16 - len(str.encode()) % 16
        for i in range(0,zerocount):
            str = str + '\0'
        return str

#CBC模式加密
def encrypt_CBC(str,key):
    #补全字符串
    str = align(str)
    key = align(key,True)
    #初始化AES，引入初始向量
    AESCipher = AES.new(key,AES.MODE_CBC,'1234567890123456')
    #加密
    cipher = AESCipher.encrypt(str)
    return b2a_hex(cipher)

#读取文件并加密
def entext(name,key):
    try:
        fpaint = open(name,'r')
        #读取明文文件
        painText = fpaint.read()
        #如果明文为空，则不执行加密
        if len(painText) > 0:
            fcipher = open('en'+name,'w')
            #加密
            cipherText = encrypt_CBC(painText,key)
            #计算明文哈希值
            MD5hash = MD5.new()
            MD5hash.update(painText.encode())
            #将密文和校验写入密文文件
            cipherText = bytes.decode(cipherText) + ',' +MD5hash.hexdigest()
            fcipher.write(cipherText)
            fcipher.close()
        fpaint.close()
        print('加密成功！')
    except:
        print('加密出错！')

if __name__ == '__main__':
    entext('pw.txt','key')