#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
import sys
import re
sys.path.append('../')
from utils.CommonUtil import *
from config import *

class XicidailiServer():
    def __init__(self):
        #self.ipList=[]
        self.urls = [
            "http://www.xroxy.com/proxylist.php?port=&type=Anonymous&ssl=&country=&latency=&reliability=5000&sort=reliability&desc=true&pnum={0}#table"
        ]
    def getproxy(self):
        for url in self.urls:
            for i in range(0, 11):
                ipList=[]
                request_url = url.format(i)
                print request_url
                time.sleep(5)
                try:
                    headers = {
                        "Host": "www.xroxy.com",
                        "User-Agent": UA[random.randint(0, len(UA) - 1)]
                    }
                    res = requests.get(request_url, headers=headers, timeout=8)
                    content = res.text
                    soup = BeautifulSoup(content, "html.parser", from_encoding="utf8")
                    try:
                        trs = soup.find_all(class_=re.compile("^row"))#('table')[4].find_all('tr')
                        print trs
                    except Exception, e:
                        print "error:" + str(e)
                        continue
                    for tr in trs[3:]:
                        tds = tr.find_all('td')
                        ip = tds[1].text.strip()  # ip
                        port = tds[2].text.strip()  # 端口
                        proxyIp = ip+":"+port
                        #print proxyIp
                        if validateIp(proxyIp):
                            ipList.append(proxyIp)
                        #protocol = tds[5].text.strip()
                        #print protocol
                        #if (protocol.lower() == "http"):
                        #    proxyIp=ip+":"+port
                        #    if(validateIp(proxyIp)):
                        #        self.ipList.append(proxyIp)
                except Exception, e:
                    print "Exception:"+str(e)
                #else:
                print ipList
                addIpsToRedis(ipList)
if __name__ == "__main__":
    proxy = XicidailiServer()
    proxy.getproxy()
    #print proxy.ipList
    #addIpsToRedis(proxy.ipList)
