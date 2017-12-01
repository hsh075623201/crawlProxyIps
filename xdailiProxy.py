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
import json


class proxyServer():
    def __init__(self):
        #self.ipList=[]
        self.urls = [
            "http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10"
        ]

    def getproxy(self):

        for url in self.urls:
            ipList = []
            request_url = url
            time.sleep(10)
            try:
                headers = {
                    "Host": "www.xdaili.cn",
                    "User-Agent": UA[random.randint(0, len(UA) - 1)]
                }
                res = requests.get(request_url, headers=headers, timeout=8)
                data = json.loads(res.text).get("rows")
                for obj in data:
                    ip=obj.get("ip")+":"+obj.get("port")
                    if validateIp(ip):
                        ipList.append(obj.get("ip")+":"+obj.get("port"))
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