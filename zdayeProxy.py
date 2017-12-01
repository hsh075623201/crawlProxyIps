#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import random
import re
import sys
sys.path.append('../')
from config import *
from utils.CommonUtil import *

class ZDaYeServer():
    def __init__(self):
        #self.ipList=[]
        self.urls = [
            "http://ip.zdaye.com/dayProxy.html"
        ]

    def getproxy(self):

        for url in self.urls:
            ipList=[]
            request_url = url
            time.sleep(10)
            try:
                headers = {
                    "Host": "ip.zdaye.com",
                    "User-Agent": UA[random.randint(0, len(UA) - 1)]
                }
                res = requests.get(request_url, headers=headers, timeout=8)
                patt1 = re.compile("/dayProxy/ip/\d+.html")
                urldict = {}
                for ele in patt1.findall(res.text)[:3]:
                    if ele not in urldict:
                        urldict[ele] = 1
                        subres = requests.get("http://ip.zdaye.com" + ele, headers=headers, timeout=8)
                        content = subres.text
                        patt = re.compile("(\d+\.\d+\.\d+\.\d+:\d+)@")
                        print patt
                        arr = patt.findall(content)
                        for ip in arr:
                            if validateIp(ip):
                                ipList.append(ip)
                            if len(ipList)>5:
                                addIpsToRedis(ipList)
                                ipList=[]
            except Exception, e:
                print "request Exceptin .............:" + str(e)
            else:
                addIpsToRedis(ipList)

if __name__ == "__main__":
    print "start........."
    proxy = ZDaYeServer()
    proxy.getproxy()
    #addIpsToRedis(proxy.ipList)