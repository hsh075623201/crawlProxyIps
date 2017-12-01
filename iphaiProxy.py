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
        #self.ipList = []
        self.urls = [
            "http://www.iphai.com/free/ng",
            "http://www.iphai.com/free/wg"
        ]

    def getproxy(self):

        for url in self.urls:
            ipList=[]
            request_url = url
            time.sleep(10)
            try:
                headers = {
                    "Host": "www.iphai.com",
                    "User-Agent": UA[random.randint(0, len(UA) - 1)]
                }
                res = requests.get(request_url, headers=headers, timeout=8)
                soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf8")
                try:
                    trs = soup.find("table").find_all('tr')
                    print trs
                except Exception, e:
                    print "error:" + str(e)
                    continue
                for tr in trs[1:]:
                    tds = tr.find_all('td')
                    print tds
                    ip = tds[0].text.strip()  # ip
                    port = tds[1].text.strip()  # 端口
                    type = tds[2].text.strip()
                    print type
                    if type.find(u"匿") > -1:
                        proxyIp = ip + ":" + port
                        if validateIp(proxyIp):
                            ipList.append(proxyIp)
                    if len(ipList)>5:
                        addIpsToRedis(ipList)
                        ipList=[]
            except Exception, e:
                print "request Exceptin .............:" + str(e)
            else:
                addIpsToRedis(ipList)

if __name__ == "__main__":
    print "start........."
    proxy = proxyServer()
    proxy.getproxy()
    #addIpsToRedis(proxy.ipList)