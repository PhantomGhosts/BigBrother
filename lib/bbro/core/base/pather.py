#!/usr/bin/env python

import os.path

class PATHanlder(object):
	def __init__(self, file):
		self.file = file

	def relative_dir(self):
		return os.path.abspath(os.path.dirname(self.file))