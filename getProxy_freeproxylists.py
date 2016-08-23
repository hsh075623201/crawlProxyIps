#coding:utf-8
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import random
import re
from config import *



UA = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
]


class FreeProxyServer():

	def __init__(self):
		self.urls = [
			"http://www.freeproxylists.com/anonymous.html"
		]
		self.req = requests.Session()
		retries = Retry(total=3,backoff_factor=0.1,status_forcelist=[ 500, 502, 503, 504 ])
		self.req.mount('http://', HTTPAdapter(max_retries=retries))

	def getproxy(self):


		for url in self.urls:
	
			request_url=url
			time.sleep(10)
			try:
				headers = {
					"Host":"www.freeproxylists.com",
					'Connection': 'keep-alive',
					"User-Agent":UA[random.randint(0, len(UA) - 1)]
				}
				res = self.req.get(request_url,headers=headers,timeout=8)
				content = res.text
				patt1=re.compile("(anon/\d+.html)")
				for ele in patt1.findall(content):
					print ele
					subres = self.req.get("http://www.freeproxylists.com/"+ele,headers=headers,timeout=8)
					subcontent= subres.text
					patt2=re.compile("(/load_anon_\d+.html)")
					url="http://www.freeproxylists.com/"+str(patt2.findall(subcontent)[0])
					print url
					lastres = self.req.get(url,headers=headers,timeout=8)
					data=lastres.text
					patt3=re.compile("(\d+\.\d+\.\d+\.\d+)&lt;/td&gt;&lt;td&gt;(\d+)")
					for ip in patt3.findall(data):
						print ip
						self.validate("http",str(ip[0])+":"+str(ip[1]))

				#print content
				#soup = BeautifulSoup(content,"html.parser",from_encoding="utf8")

				# try:
				# 	lists = soup.find('ol').find_all('li')
				# except Exception,e:
				# 	print "error:"+str(e)
				# 	continue
				# for ele in lists[1:]:
				# 	print ele
				# 	elearrs = ele.find('a').text.strip().split(":")
				# 	ip = elearrs[0]
				# 	port= elearrs[1]
				# 	# port = tds[2].text.strip() #端口
				# 	protocol = "http"
				# 	self.validate(protocol.lower(),ip,port)
			except Exception,e:
				print "request Exceptin .............:"+str(e)
	def validate(self,protocol,ip):

		try:

			headers = {
				"User-Agent":UA[random.randint(0, len(UA) - 1)]
			}
			proxy_ip = {protocol:protocol+'://'+ip}
			print proxy_ip
			#requests.get("http://bang.360.cn/liangpin/aj_get_goods?pn=0",proxies=proxy_ip,headers=headers,timeout=5)
			requests.get("http://youpin.58.com",proxies=proxy_ip,headers=headers,timeout=8)
		except Exception,e:
			print "validate Exception:"+str(e)
		else:
			print "***********************************************"
			self.log(ip)

	def log(self,ip):
		with open("logs/proxyIps.log","a") as f:
			f.write(ip+",\n")
			f.flush()



	


if __name__=="__main__":

	print "start........."
	proxy = FreeProxyServer()
	proxy.getproxy()
	proxy.req.close()