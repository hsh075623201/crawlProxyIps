#coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import random
import sys
sys.path.append('../')
from util import *



UA = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
]


class ProxyServer():

	def __init__(self):
		self.urls = [
			"http://www.cybersyndrome.net/pla.html"
		]

	def getproxy(self):


		for url in self.urls:
			
			request_url=url
			time.sleep(10)
			try:
				headers = {
					"Host":"www.cybersyndrome.net",
					"Referer":"http://www.cybersyndrome.net/",
					"User-Agent":UA[random.randint(0, len(UA) - 1)]
				}
				res = requests.get(request_url,headers=headers,timeout=8)
				content = res.text
				#print content
				soup = BeautifulSoup(content,"html.parser",from_encoding="utf8")

				try:
					lists = soup.find('ol').find_all('li')
				except Exception,e:
					print "error:"+str(e)
					continue
				for ele in lists[1:]:
					print ele
					ip = ele.find('a').text.strip()
					#ip = elearrs[0]
					#port= elearrs[1]
					# port = tds[2].text.strip() #端口
					#protocol = "http"
					self.validate(ip)
			except Exception,e:
				print "request Exceptin .............:"+str(e)
	def validate(self,ip):

		try:

			headers = {
				#"Referer":"http://bang.360.cn/liangpin?from=index",
				"User-Agent":UA[random.randint(0, len(UA) - 1)]
			}
			proxy_ip = {"http":'http://'+ip}
			#requests.get("http://bang.360.cn/liangpin/aj_get_goods?pn=0",proxies=proxy_ip,headers=headers,timeout=5)
			requests.get("http://youpin.58.com",proxies=proxy_ip,headers=headers,timeout=5)
		except Exception,e:
			print "validate Exception:"+str(e)
		else:
			print ip
			getRedisConn().sadd("proxyIps",ip.replace(' ', ''))
			#self.insert(obj)



if __name__=="__main__":

	print "start........."
	proxy = ProxyServer()
	proxy.getproxy()
