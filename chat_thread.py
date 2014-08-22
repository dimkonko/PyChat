import threading

class ChatThread(threading.Thread):
	def __init__(self, threadId, func):
		threading.Thread.__init__(self)
		self.threadId = threadId
		self.func = func

	def run(self):
		print "Starting thread " + str(self.threadId)
		self.func(self.threadId)
		print "Finishing thread " + str(self.threadId)
