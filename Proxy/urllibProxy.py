#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request

proxies = {
    'https': 'https://127.0.0.1:56948',
    'http': 'http://127.0.0.1:56948'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

google_url = 'https://www.youtube.com'
opener = request.build_opener(request.ProxyHandler(proxies))
request.install_opener(opener)

req = request.Request(google_url, headers=headers)
response = request.urlopen(req)

print(response.read().decode())
