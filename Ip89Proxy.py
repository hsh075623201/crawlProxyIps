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

class proxyServer():
    def __init__(self):
        #self.ipList=[]
        self.urls = [
            #"http://www.89ip.cn/api/?&tqsl=100&sxa=&sxb=&tta=&ports=&ktip=&cf=1"
			"http://www.89ip.cn/apijk/?&tqsl=100&sxa=&sxb=&tta=&ports=&ktip=&cf=1"
        ]

    def getproxy(self):

        for url in self.urls:
            ipList = []
            request_url = url
            time.sleep(3)
            try:
                headers = {
                    "Host": "www.89ip.cn",
                    "User-Agent": UA[random.randint(0, len(UA) - 1)]
                }
                res = requests.get(request_url, headers=headers, timeout=8)
                patt = re.compile("(\d+\.\d+\.\d+\.\d+:\d+)<BR>")
                for ip in patt.findall(res.text):
                    if validateIp(ip):
                        ipList.append(ip)
                    if len(ipList)>5:
                        addIpsToRedis(ipList)
                        ipList = []
            except Exception, e:
                print "request Exceptin .............:" + str(e)
            else:
                addIpsToRedis(ipList)

if __name__ == "__main__":
    print "start........."
    proxy = proxyServer()
    proxy.getproxy()
    #addIpsToRedis(proxy.ipList)
