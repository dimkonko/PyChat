class User(object):
	def __init__(self, conn, thread):
		self.conn = conn
		self.thread = thread

	def get_conn(self):
		return self.conn

	def disconnect(self):
		self.conn.close()
		print "Disconected"
		print "Stopping thread " + str(self.thread.threadId)