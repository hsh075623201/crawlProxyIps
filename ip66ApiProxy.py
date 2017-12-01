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
			#"http://www.89ip.cn/apijk/?&tqsl=100&sxa=&sxb=&tta=&ports=&ktip=&cf=1"
			"http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D100%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1"
        ]

    def getproxy(self):

        for url in self.urls:
            ipList = []
            request_url = url
            time.sleep(3)
            try:
                headers = {
                    "Host": "www.66ip.cn",
                    "User-Agent": UA[random.randint(0, len(UA) - 1)]
                }
                res = requests.get(request_url, headers=headers, timeout=8)
                patt = re.compile("(\d+\.\d+\.\d+\.\d+:\d+)<br />")
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
