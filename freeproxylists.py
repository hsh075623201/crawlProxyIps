#!/usr/bin/env python
# -*- coding:  utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import random
import sys
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re
sys.path.append('../')
from utils.CommonUtil import *
from config import *

#todo list  deprecated
class FreeProxyServer():
    def __init__(self):
        self.urls = [
            "http://www.freeproxylists.com/anonymous.html"
        ]
        self.req = requests.Session()
        retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.req.mount('http://', HTTPAdapter(max_retries=retries))

    def getproxy(self):

        for url in self.urls:

            request_url = url
            time.sleep(10)
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                }
                res = self.req.get(request_url, headers=headers, timeout=8)
                content = res.text
                print content
                patt1 = re.compile("(anon/\d+.html)")
                for ele in patt1.findall(content):
                    print ele
                    subres = self.req.get("http://www.freeproxylists.com/" + ele, headers=headers, timeout=8)
                    subcontent = subres.text
                    patt2 = re.compile("(/load_anon_\d+.html)")
                    url = "http://www.freeproxylists.com/" + str(patt2.findall(subcontent)[0])
                    print url
                    lastres = self.req.get(url, headers=headers, timeout=8)
                    data = lastres.text
                    patt3 = re.compile("(\d+\.\d+\.\d+\.\d+)&lt;/td&gt;&lt;td&gt;(\d+)")
                    for ip in patt3.findall(data):
                        print ip

            except Exception, e:
                print "request Exceptin .............:" + str(e)

if __name__ == "__main__":
    print "start........."
    proxy = FreeProxyServer()
    proxy.getproxy()
    proxy.req.close()