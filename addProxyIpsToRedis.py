#coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import pymysql.cursors
import random
from proxyIpsConfig import *
import sys
sys.path.append('../')
from util import *


class AddIpsToRedisServer():

	def __init__(self):

		self.redisConn=getRedisConn()

	def add(self):
	
		for ip in ips:
			print ip
			self.redisConn.sadd("proxyIps",ip.replace(' ', ''))





if __name__=="__main__":
	objServer = AddIpsToRedisServer()
	objServer.add()
