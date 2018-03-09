#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *

s = socket(AF_INET,SOCK_STREAM)
s.bind(('',6666))
s.listen(1)
sock,addr = s.accept()
print('Connected by'+str(addr))
sock.send(b'Welcome to server')
text = sock.recv(1024)
print(text)
sock.close()
s.close()