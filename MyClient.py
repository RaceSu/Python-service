# ^_^ coding: utf-8 ^_^
"""
Created on 2016/12/16 18:39

@author: surui
"""

import os, time, logging, sys
import requests
import json
import ConfigParser


class HttpClient:

	def __init__(self):
		self.cf = ConfigParser.ConfigParser()
		# 注意这里面路径的问题可能会导致server not found问题，base_dir 并不好使
		self.conf_dir = "./conf/server.conf"
		# 解析server的配置文件
		self.cf.read(self.conf_dir)

	def deal_via_http(self, url, request_data):
		# build headers
		headers = {'content-type': 'application/json'}
		# post data to url
		response = requests.post(url, data=request_data, headers=headers)
		response.encoding = "utf-8"
		result = response.text
		result = json.loads(result)
		return result

	def postdata(self, client_data):
		url = self.cf.get("server", "my_url")

		# post表单数据
		request_data = {"pin": client_data}

		if isinstance(client_data, str):
			request_data["type"] = "str_type"
		if isinstance(client_data, int):
			request_data["type"] = "int_type"
		if isinstance(client_data, list):
			request_data["type"] = "list_type"
		if isinstance(client_data, tuple):
			request_data["type"] = "tuple_type"
		if isinstance(client_data, dict):
			request_data["type"] = "dict_type"

		# 提交表单数据，使用服务
		result = self.deal_via_http(url, request_data)
		# 使用服务返回结果
		pin = result["pin"]
		# pin = pin.encode('utf-8')
		return pin


if __name__ == "__main__":
	room = HttpClient()
	start = time.time()
	# 测试
	print room.postdata(1)
	print room.postdata("test")
	print room.postdata([5, "hello", 4, 6, "world", 2, 4, 7])
	print room.postdata((1, 2, 3, 4))
	print room.postdata({'x':60, 'y':70})
	end = time.time()
	print "Used time %ss"%(end-start)