#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process,Pool
import os,time
import requests
from requests.cookies import RequestsCookieJar

def run_proc(name):
    url = 'http://localhost:8080/publish/checkPublishDataError.do'
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("JSESSIONID", "047AD0603EE77BF83AB6688B4A006BA6")
    for i in range(30000):
        postdata = {'store': '5d555246fe1144c19950,24e06b90997c4f2ea622,sJEhkohTnkJBuEaLWkWm,NbdBSsQJItaQXBxgCoSH,fRHuTZRpacEcFIWwRaQP,zPqheSuSXdunIrElXsqA,18e9396e655b45d39a27,MuNauLsFIqlDzqRRpMfG,CZBhnIBTfkogipkMhDqL,OxmEkwnPFgVtlkgDkNJp,PDtsWMpzcGgcuwtMPHFR,FodVMsfFeAqIUzcJOMrC,wAvGilGOddFheCzusjLo,8d2491f5722c4ff4955c,CtvSscZjSkXCLjAiEnQy,sDfdUetrucTSGmelSzyo,FLffkYbGDzTsANKdQUgu,hlEGuxUmwzxQQHphbhET,VfQXYlrAYLbxkjJtGhpi,wKbUwNyZHHlHVNGzbnkx,JhefdCbErGWgAjvSBYpS,FuEoFUfYBwQifjiSazoH,0f29eff5dcc64856aaf4,02315cb7f07d4ccfbecc,vurZPHvtOBIzURfheLhN,ZcXmURjwyGeadLWUIach,MWVOhpTyppNIkiBIpwge,uwCOdIPYUJQgskvfcdVy,tJDushcllzwsNPvjHbLX,EhUTPofLEftdfRJeGgdc,XHCrBYCqdVWVSIXhUzFr,OYIxvGWVVaJtSpYoWiHY,YadwkpbcglGZizccCOTY,AzmrzWFCLGJASWBnsnYE,qPhjmoLcBNUVLPVoHVdn,444a94cfb6904c049ac9,tqIIARrHDZmSEORlWdKd,yLKhjFVTGqoyjPhyuDom,oGgEiyZVwEAgrXJFqJAg,imatybkqVbqdTLmpMHVK,WqcGWwlVjxVHeprmBcaK,waJHGLGpgfFDfzJUdxEx,QMliFMKSLoawYeFcPZDo,MQEdxjPQGFIHlLYekQNp,opwRSaLHuKEQxIjaIvJV,xeyyfjfLKwJaxswPGHAx,xjBVhQtlWpEzHPgCCCqs,IOwUePXodUFeHZmbXsDB,FlYhKUNjeTZnhhgtrfgq,qTvvOdHZRLYvmrWMegfK,nHOwWFxwqbdkPMdMqiEr,RQPGCJEWJFCHOPKllIEZ,VQUpKdwyxkzRXybxbATz,GvKhdadwNmQUpzkJoBWy,ydSXOIovfgBwXcrSlCen,DcjzzzChulMClTLDTNMp,nWoCvPzGrGJqrTovOHuT,YaOVkFewRmwjXEaLMuVh,NUngTqVBSXdFdFHzfVpG,sZNDhKlxWFkfwimSZSYv,qnvxcgJYvScqjYvXZqmO'}
        r = requests.post(url,data=postdata,cookies=cookie_jar)
        print(r)

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