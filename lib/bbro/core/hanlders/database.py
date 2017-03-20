#!/usr/bin/env python

import sqlite3 as lite

from ..base import pather

pathHD = pather.PATHandler(__file__)

class DBHandler(object):
	def __init__(self):
		try:
			self.con = lite.connect(os.path.join(pathHD.relative_dir()), 'databases', 'modules.db'))
			self.cur = self.con.cursor()
		except lite.Error as e:	
			print("\033[91mAn error occurred: {0}\033[0m".format(e))

	def query(self, query):
		pass
