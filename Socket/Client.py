#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *

c = socket(AF_INET,SOCK_STREAM)
port = socket.getservbyname("http", "tcp")
c.connect(('dce9e46e.ngrok.io',port))
text = c.recv(1024)
print(text)
c.send(b'Hello world')
