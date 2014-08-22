import socket
import sys

class Client(object):

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.socket.connect((host, port))
		except socket.error, error_msg:
			print error_msg
			print "Unable to connect"
			sys.exit()

		print "Connected"

	def login(self):
		nickname = raw_input("Enter your name: ")

		self.socket.send(nickname)
		self.nickname = self.socket.recv(1024)

		if not self.nickname:
			print "Server error"
			self.close()
			sys.exit()

		print "Your name is: " + self.nickname

	def chat(self):
		while True:
			msg = raw_input(self.nickname + ": ")
			try:
				self.socket.send(msg)
			except socket.error:
				print "Server is offline"
				break

	def close(self):
		print "Disconecting..."
		self.socket.close()


client = Client("localhost", 2714)

try:
	client.login()
	client.chat()
except KeyboardInterrupt:
	client.close()
	sys.exit()