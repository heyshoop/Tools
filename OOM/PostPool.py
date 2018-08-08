#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process,Pool
import os,time
import requests

def run_proc(name):
    for i in range(30000):
        postdata = {'code': i}
        r = requests.post("http://localhost:8080/choiceWebService/OOM.do", data=postdata)

if __name__ =='__main__':
    print('Run the main process (%s).' % (os.getpid()))
    mainStart = time.time()
    p = Pool(8)
    for i in range(16):
        p.apply_async(run_proc,args=('Process'+str(i),))

    print('Waiting for all subprocesses done ...')
    p.close()
    p.join()
    print('All subprocesses done')
    mainEnd = time.time()
    print ('All process ran %0.2f seconds.' % (mainEnd-mainStart))