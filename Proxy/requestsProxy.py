#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

proxies = {
    'https': 'https://127.0.0.1:49621',
    'http': 'http://127.0.0.1:49620'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

google_url = 'https://www.youtube.com'
response = requests.get(google_url, proxies=proxies,headers=headers)
print(response.text)