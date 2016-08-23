#coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import random
import re
import sys
sys.path.append('../')
from util import *



UA = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
]


class ZDaYeServer():

	def __init__(self):
		self.conn=getRedisConn()
		self.urls = [
			"http://ip.zdaye.com/dayProxy.html"
		]

	def getproxy(self):

		for url in self.urls:
			
			request_url=url
			time.sleep(10)
			try:
				headers = {
					"Host":"ip.zdaye.com",
					"User-Agent":UA[random.randint(0, len(UA) - 1)]
				}
				res = requests.get(request_url,headers=headers,timeout=8)
				patt1=re.compile("/dayProxy/ip/\d+.html")
				urldict={}
				for ele in patt1.findall(res.text)[:3]:
					if ele not in urldict:
						urldict[ele]=1
						subres=requests.get("http://ip.zdaye.com"+ele,headers=headers,timeout=8)
						content=subres.text
						patt=re.compile("(\d+\.\d+\.\d+\.\d+:\d+)#")
						arr=patt.findall(content)
						for ip in arr:
							self.validate("http",ip)

				# content = res.text
				# patt=re.compile("(\d+\.\d+\.\d+\.\d+:\d+)#")
				# arr=patt.findall(content)
				# for ip in arr:
				# 	self.validate("http",ip)
				#print content
				# soup = BeautifulSoup(content,"html.parser",from_encoding="utf8")

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
				#"Referer":"http://bang.360.cn/liangpin?from=index",
				"User-Agent":UA[random.randint(0, len(UA) - 1)]
			}
			proxy_ip = {protocol:protocol+'://'+ip}
			#requests.get("http://bang.360.cn/liangpin/aj_get_goods?pn=0",proxies=proxy_ip,headers=headers,timeout=5)
			requests.get("http://youpin.58.com",proxies=proxy_ip,headers=headers,timeout=5)
		except Exception,e:
			print "validate Exception:"+str(e)
		else:
			
			#self.log(ip)
			print ip
			self.loadRedis(ip)

	def loadRedis(self,ip):
		self.conn.sadd("proxyIps",ip.replace(' ', ''))

	def log(self,ip):
		with open("logs/proxyIps.log","a") as f:
			f.write(ip+",\n")
			f.flush()


	

if __name__=="__main__":

	print "start........."
	proxy = ZDaYeServer()
	proxy.getproxy()