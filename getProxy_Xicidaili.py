#coding:utf-8
import requests
#from requests.packages.urllib3.util.retry import Retry
#from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import random
#from config import *
import sys
sys.path.append('../')
from util import *


headers = {
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, sdch",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"Host":"www.xicidaili.com",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
}
UA = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
]


class XicidailiServer():

	def __init__(self):

		self.redisConn=getRedisConn()
		self.urls = [
			"http://www.xicidaili.com/nn/"
		]
		#self.req=requests.Session()
                #retries = Retry(total=5,backoff_factor=0.1,status_forcelist=[ 500, 502, 503, 504 ])
                #req.mount('http://', HTTPAdapter(max_retries=retries))

	def getproxy(self):


		for url in self.urls:
			for i in range(1,5):
				request_url=url+str(i)
				time.sleep(5)
				try:
					headers = {
						"Host":"www.xicidaili.com",
						"User-Agent":UA[random.randint(0, len(UA) - 1)]
					}
					#s=requests.Session()
					#retries = Retry(total=5,backoff_factor=0.1,status_forcelist=[ 500, 502, 503, 504 ])
					#s.mount('http://', HTTPAdapter(max_retries=retries))
					res = requests.get(request_url,headers=headers,timeout=8)
					content = res.text
					#s.close()
					soup = BeautifulSoup(content,"html.parser",from_encoding="utf8")
			
					try:
						trs = soup.find('table').find_all('tr')
					except Exception,e:
						print "error:"+str(e)
						continue
					for tr in trs[1:]:
						tds = tr.find_all('td')
						ip = tds[1].text.strip() #ip
						port = tds[2].text.strip() #端口
						protocol = tds[5].text.strip()
						if(protocol.lower()=="http"):

							self.validate(protocol.lower(),ip,port)
				except Exception,e:
					print "request Exceptin .............:"+str(e)
	def validate(self,protocol,ip,port):

		try:

			headers = {
				"User-Agent":UA[random.randint(0, len(UA) - 1)]
			}
			proxy_ip = {protocol:protocol+'://'+ip+':'+port}
			#requests.get("http://bang.360.cn/liangpin/aj_get_goods?pn=0",proxies=proxy_ip,headers=headers,timeout=5)
			requests.get("http://youpin.58.com",proxies=proxy_ip,headers=headers,timeout=5)
		except Exception,e:
			print "validate Exception:"+str(e)
		else:
			obj = {
				"protocol":protocol,
				"ip":ip,
				"port":port,
				"accept":"youpin.58"
			}
			print (ip+":"+port).replace(' ', '')
			self.redisConn.sadd("proxyIps",(ip+":"+port).replace(' ', ''))
			#self.insert(obj)





if __name__=="__main__":
	proxy = XicidailiServer()
	proxy.getproxy()
	#proxy.req.close()
