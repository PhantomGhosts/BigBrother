import os.path
from .base import info

class select(object):
	def __init__(self, stdpath):
		super(select, self).__init__()
		self.stdpath = stdpath

	def run(self, path):
		future_path = os.path.join(self.stdpath, path)
		try:
			os.listdir(future_path)
		except IOError:
			print info.error("%s Doesn't exists")
	def help(self):
		print 