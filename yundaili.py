#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../')
from utils.CommonUtil import *
from config import *

class proxyServer(object):
    def __init__(self):
        self.urls = [
            "http://www.yun-daili.com/?stype=1&page=",
			"http://www.yun-daili.com/?stype=3&page="
        ]
    def getproxy(self):
        for url in self.urls:
            for i in range(1, 2):
                ipList=[]
                request_url = url + str(i)
                print request_url #time.sleep(5)
                time.sleep(5)
                try:
                    headers = {
                        "Host": "www.yun-daili.com",
                        "User-Agent": UA[random.randint(0, len(UA) - 1)]
                    }
                    res = requests.get(request_url, headers=headers, timeout=8)
                    content = res.text
                    soup = BeautifulSoup(content, "html.parser", from_encoding="utf8")
                    try:
                        trs = soup.find_all('table')[0].find_all("tr")
                        #print trs
                    except Exception, e:
                        print "error:" + str(e)
                        continue
                    for tr in trs[1:]:
                        tds = tr.find_all('td')
                        ip = tds[0].text.strip()  # ip
                        port = tds[1].text.strip()  # 端口
                        #type = tds[3].text.strip()
                        proxyIp=ip+":"+port
                        if validateIp(proxyIp):
                            ipList.append(proxyIp)
                            print proxyIp #ipList.append(proxyIp)
                        if len(ipList)>5:
                            addIpsToRedis(ipList)
                            ipList = []
                except Exception, e:
                    print str(e)
                else:
                    addIpsToRedis(ipList)
if __name__ == "__main__":
    proxy = proxyServer()
    proxy.getproxy()
