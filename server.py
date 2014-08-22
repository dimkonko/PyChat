import socket
import sys

from chat_thread import ChatThread
from user import User

class Server(object):
	def __init__(self, host, port, listen_sockets=5):
		self.user_list = list()
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Is it works?
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
			self.user_list.append(User(conn, conn_thread))
			conn_thread.start()
			print "Started thread " + str(self.counter)

			self.counter += 1
			print "Connection added!"

	def close(self):
		for user in self.user_list:
			user.disconnect()
		self.socket.close()

	def chat_thread(self, threadId):
		chat_user = None
		for user in self.user_list:
			if user.thread.threadId == threadId:
				chat_user = user
				break

		conn = chat_user.get_conn()

		nickname = conn.recv(1024)
		conn.send(nickname)

		def close():
			"""Remove thread from user_list
			This function removing connection object from
			main list of connections
			"""
			self.user_list.remove(chat_user)
			print "Disconnected: " + nickname

		while True:
			try:
				msg = conn.recv(4096)
				if msg:
					for user in self.user_list:
						user.conn.send(nickname + ": " + msg)
				else:
					close()
					return
			except:
				close()
				return
			

server = Server("localhost", 2713)

try:
	server.start()
except KeyboardInterrupt:
	print ""
	print "Force exiting...."
	server.close()
