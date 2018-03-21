#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 上午10:26
# @Author  : Anchor
# @File    : decode.py
# @Des     : 解密


from Crypto.Cipher import AES
from Crypto.Hash import MD5
from binascii import a2b_hex

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

#CBC模式解密
def decrypt_CBC(str,key):
    #补全字符串
    key = align(key,True)
    #初始化AES
    AESCipher = AES.new(key,AES.MODE_CBC,'1234567890123456')
    #解密
    paint = AESCipher.decrypt(a2b_hex(str))
    return paint

#读取文件并解密
def detext(name,key):
    try:
        fcipher = open(name,'r')
        fpaint = open('readme.txt','w+')
        #读取密文文件
        fcipherText = fcipher.read()
        #读取密文和校验哈希值
        cipherText = fcipherText.split(',')[0]
        painhash = fcipherText.split(',')[1]
        #用密码解密
        painText = decrypt_CBC(cipherText,key)
        #去除\0
        painText = painText.decode().rstrip('\0')
        #校验密码
        #计算本次解密后明文的哈希值
        MD5hash = MD5.new()
        MD5hash.update(painText.encode())
        #比对哈希值判断密码是否正确
        if painhash != MD5hash.hexdigest():
            print('密码错误!')
        else:
            fpaint.write(painText)
            fpaint.close()
            fcipher.close()
            print('解密成功！')
    except:
        print('解密失败，密码错误!')

if __name__ == '__main__':
    detext('enpw.txt','key')