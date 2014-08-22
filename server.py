import socket
import sys

from chat_thread import ChatThread

class User(object):
	def __init__(self, conn, thread):
		self.conn = conn
		self.thread = thread

	def get_conn(self):
		return self.conn

	def close(self):
		self.conn.close()
		print "Disconected"
		print "Stopping thread " + str(self.thread.threadId)


class Server(object):
	def __init__(self, host, port, listen_sockets=5):
		self.con_list = list()
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

			conn_thread = ChatThread(self.counter, self.chat_thread)
			conn_thread.daemon = True
			self.con_list.append(User(conn, conn_thread))
			conn_thread.start()

			self.counter += 1
			print "Connection added!"

	def close(self):
		for con in self.con_list:
			con.close()
		self.socket.close()

	def chat_thread(self, threadId):
		chat_con = None
		for con in self.con_list:
			if con.thread.threadId == threadId:
				chat_con = con
				break

		conn = chat_con.get_conn()

		nickname = conn.recv(1024)
		conn.send(nickname)

		def close():
			"""Remove thread from con_list
			This function removing connection object from
			main list of connections
			"""
			self.con_list.remove(chat_con)
			print "Disconnected: " + nickname

		while True:
			try:
				msg = conn.recv(4096)
				if msg:
					for con in self.con_list:
						con.conn.send(nickname + ": " + msg)
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
