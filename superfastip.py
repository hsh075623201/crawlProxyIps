#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
import sys

sys.path.append('../')
from utils.CommonUtil import *
from config import *

class SuperFastServer():
    def __init__(self):
        #self.ipList=[]
        self.urls = [
            "http://superfastip.com/welcome/getips/"
        ]
    def getproxy(self):
        for url in self.urls:
            for i in range(1, 10):
                ipList=[]
                request_url = url + str(i)
                time.sleep(5)
                try:
                    headers = {
                        "Host": "superfastip.com",
                        "User-Agent": UA[random.randint(0, len(UA) - 1)]
                    }
                    res = requests.get(request_url, headers=headers, timeout=8)
                    content = res.text
                    soup = BeautifulSoup(content, "html.parser", from_encoding="utf8")
                    try:
                        trs = soup.find('table').find_all('tr')
                    except Exception, e:
                        print "error:" + str(e)
                        continue
                    for tr in trs[1:]:
                        tds = tr.find_all('td')
                        ip = tds[1].text.strip()  # ip
                        port = tds[2].text.strip()  # 端口
                        #type = tds[4].text.strip()
                        print type #= tds[4].text.strip()
                        if (1==1):
                            proxyIp=ip+":"+port
                            print proxyIp #=ip+":"+port
                            if(validateIp(proxyIp)):
                                ipList.append(proxyIp)
                        if len(ipList)>5:
                            addIpsToRedis(ipList)
                            ipList=[]
                except Exception, e:
                    print str(e)
                else:
                    addIpsToRedis(ipList)
if __name__ == "__main__":
    proxy = SuperFastServer()
    proxy.getproxy()
    #addIpsToRedis(proxy.ipList)
