#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/24 下午4:48
# @Author  : Anchor
# @File    : githelp.py
# @Des     : git瞎J8提交工具

from datetime import date, timedelta
from random import randint
from time import sleep
import sys
import subprocess

#天数
def get_date_string(n, startdate):
	d = startdate - timedelta(days=n)
	rtn = d.strftime("%a %b %d %X %Y %z -0400")
	return rtn

def main(argv):
	if len(argv) < 1 or len(argv) > 2:
		print("参数个数有误！")
		sys.exit(1)
	n = int(argv[0])
	if len(argv) == 1:
		startdate = date.today()
	if len(argv) == 2:
		startdate = date(int(argv[1][0:4]), int(argv[1][5:7]), int(argv[1][8:10]))
	i = 0
	while i <= n:
		curdate = get_date_string(i, startdate)
		num_commits = randint(1, 10)
		for commit in range(0, num_commits):
			subprocess.call("echo '" + "重复写入的body："+"\r"+curdate + str(randint(0, 1000000)) +"' > realwork.txt; git add realwork.txt; GIT_AUTHOR_DATE='" + curdate + "' GIT_COMMITTER_DATE='" + curdate + "' git commit -m 'update'; git push;", shell=True)
			sleep(.5)
		i += 1
	subprocess.call("git rm realwork.txt; git commit -m 'delete'; git push;", shell=True)

if __name__ == "__main__":
	main(sys.argv[1:])
