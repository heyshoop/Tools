#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *

c = socket(AF_INET,SOCK_STREAM)
c.connect(('127.0.0.1',6666))
text = c.recv(1024)
print(text)
c.send(b'Hello world')
