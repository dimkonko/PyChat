import socket
import sys
import threading
import time

class Con(object):
	def __init__(self, conn, thread):
		self.conn = conn
		self.thread = thread
		self.isExit = False

	def close(self):
		self.conn.close()
		print "Disconected"
		print "Stopping thread " + str(self.thread.threadId)


class MyThread(threading.Thread):
	def __init__(self, threadId, conn, func):
		threading.Thread.__init__(self)
		self.threadId = threadId
		self.conn = conn
		self.func = func

	def run(self):
		print "Starting thread " + str(self.threadId)
		self.func(self.conn, self.threadId)
		print "Finishing thread " + str(self.threadId)


class Server(object):
	def __init__(self, host, port, listen_sockets=5):
		self.con_list = list()
		self.threads_lsit = list()
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.socket.bind((host, port))
		self.socket.listen(listen_sockets)

		print "Server started at port: " + str(port)

	def start(self):
		self.counter = 1
		while True:
			print "Waiting for connection..."
			conn, addr = self.socket.accept()

			conn_thread = MyThread(self.counter, conn, self.chat_thread)
			conn_thread.daemon = True
			conn_thread.start()
			self.con_list.append(Con(conn, conn_thread))

			self.counter += 1
			print "Connection added!"

	def close(self):
		for con in self.con_list:
			con.close()
		self.socket.close()

	def chat_thread(self, conn, threadId):
		nickname = conn.recv(1024)
		conn.send(nickname)

		def close():
			del self.con_list[threadId - 1]
			print "Disconected: " + nickname
			self.counter -= 1

		while True:
			try:
				msg = conn.recv(4096)
				if msg:
					print nickname + ": " + msg
					conn.send(msg)
				else:
					close()
					return
			except:
				close()
				return
			

server = Server("localhost", 2714)

try:
	server.start()
except KeyboardInterrupt:
	print ""
	print "Force exiting...."
	server.close()
