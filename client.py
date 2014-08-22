import socket
import sys

from chat_thread import ChatThread

class Client(object):

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.socket.connect((host, port))
		except socket.error, error_msg:
			print error_msg
			print "Unable to connect."
			sys.exit()

		print "Connected."

	def login(self):
		"""Send the name and starts the message thread
		This function sending an entered name and 
		receiving response from server. 
		If response is empty - there is some throuble on the server
		and exiting from program
		else - login
		"""
		nickname = raw_input("Enter your name: ")

		self.socket.send(nickname)
		self.nickname = self.socket.recv(1024)

		if not self.nickname:
			print "Server error."
			self.close()
			sys.exit()

		print "Your name is: " + self.nickname
		
		msg_thread = ChatThread(20, self.recv_other)
		msg_thread.daemon = True
		msg_thread.start()

	def chat(self):
		print "Welcome in the chat room!"
		print "You can start typing a message."
		while True:
			msg = raw_input()
			try:
				self.socket.send(msg)
			except socket.error:
				print "Server is offline"
				break

	def recv_other(self, threadId):
		"""Receive messages from other people
		This function represents a new thread, which
		receiving messages from other users and
		printing them
		If message from server is empty - server was
		turned off
		"""
		while True:
			msg = self.socket.recv(4096)
			if not msg:
				print "Server is offline now.",
				print "Press enter to exit."
				self.close()
				sys.exit()
			else:
				print msg

	def close(self):
		"""Send signal to server and close socket
		This function sending empty message, which means,
		that user exiting from the program
		"""
		try:
			self.socket.send("")
		except:
			pass
		print "Disconecting..."
		self.socket.close()


client = Client("localhost", 2713)

try:
	client.login()
	client.chat()
except KeyboardInterrupt:
	client.close()
	sys.exit()