# ^_^ coding: utf-8 ^_^
"""
Created on 2016/12/16 18:39

@author: surui
"""
import time


class HTTPWorker:
	def __init__(self):
		self.count = 0

	def deal_request(self, data):
		print "0"
		if self.count == 0:
			# 模拟耗费时间的初始化
			print "Loading Model"
			time.sleep(2)
			self.count = 2

		# 对应用户传入的不同类型数据的 进行不同处理
		if isinstance(data, int):
			data += 1000
		if isinstance(data, str):
			data = "Hello" + data + "world"
		if isinstance(data, list):
			data = ''.join(data)
		if isinstance(data, dict):
			data["ok"] = 100
		if isinstance(data, tuple):
			data = data + (0, 0, 0, 0, 0, 0, 0, 0)

		print "work end {} was return".format(data)
		return data
