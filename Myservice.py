# ^_^ coding: utf-8 ^_^
"""
Created on 2016/12/16 18:39

@author: surui
"""

import re, cgi, json, logging, ConfigParser, threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from Myworker import HTTPWorker


class LocalData(object):
	records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
	deal_requester = HTTPWorker()

	def do_POST(self):
		logger.debug("### self.path:%s"%self.path)
		# self.path是server.conf里面的路径
		if None != re.search('/test/*', self.path):
			# 设置header，在访问的时候header要与此保持一致
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			logger.debug("ctype:%s pdict:%s" % (ctype, pdict))
			# ctype 是获取服务的钥匙
			if ctype == 'application/json':
				length = int(self.headers.getheader('content-length'))
				# 获取用户提交的数据
				client_data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
				logger.debug("33 data : %s" % client_data)
				# 建立新的字典用于返回给用户结果
				total_result = {}
				# 得到pin键对应的值
				logger.debug(" data.get(\"pin\") :{}".format(client_data.get("pin")))
				# “pin” 是用户提交的字典带的键指定提交数据的类型
				data_type = client_data.get("type")[0]

				# 字符型传入会被列表包着
				if data_type == "str_type":
					data = client_data.get("pin")[0]
					# print type(data)
					result = self.deal_requester.deal_request(data)
					total_result["pin"] = result

				# 整型传入会被列表包着
				if data_type == "int_type":
					data = client_data.get("pin")[0]
					# print type(data)
					result = self.deal_requester.deal_request(int(data))
					total_result["pin"] = result

				# 列表传入还是列表，并不是想象中的嵌套列表
				if data_type == "list_type":
					data = client_data.get("pin")
					# print type(data)
					# exec("data = %s"%data)
					result = self.deal_requester.deal_request(data)
					total_result["pin"] = result

				# 元组传入后会变成列表
				if data_type == "tuple_type":
					data = client_data.get("pin")
					# print data
					# print type(data)
					result = self.deal_requester.deal_request(data)
					total_result["pin"] = result

				# 字典传入后, 只有字典的键作为字符放在列表里面传入
				if data_type == "dict_type":
					data = client_data.get("pin")
					# print data
					# print type(data)
					result = self.deal_requester.deal_request(data)
					total_result["pin"] = result

				# 最终结果转化为字符串，网络传输数据都是走的字符串流
				result_str = json.dumps(total_result)
				logger.info("deal_request result is: %s " % result_str)
			else:
				result_str = {}

			self.send_response(200)
			self.send_header('Content-Type', 'application/json;charset=utf-8')
			self.end_headers()
			self.wfile.write(result_str)
		else:
			self.send_response(403)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
		return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	allow_reuse_address = True

	def shutdown(self):
		self.socket.close()
		HTTPServer.shutdown(self)


# start simple server
class SimpleHttpServer():
	def __init__(self, ip, port):
		self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

	def start(self):
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

	def waitForThread(self):
		self.server_thread.join()

	def addRecord(self, recordID, jsonEncodedRecord):
		LocalData.records[recordID] = jsonEncodedRecord

	def stop(self):
		self.server.shutdown()
		self.waitForThread()


if __name__ == '__main__':
	logger = logging.getLogger("service")
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler("./web.log")
	fh.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s - [%(name)s] - [%(levelname)s] - |%(message)s|")
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)
	logger.addHandler(ch)
	logger.addHandler(fh)
	# 开启服务
	logger.debug("Initializing service ...")
	# # initialize a parser to parse the server.conf
	parser = ConfigParser.ConfigParser()
	parser.read("./conf/server.conf")
	host = parser.get("server", "my_host")
	port = parser.getint("server", "my_port")
	server = SimpleHttpServer(host, port)
	logger.info('HTTP Server Running @ %s:%s '%(host, port))
	server.start()
	server.waitForThread()
