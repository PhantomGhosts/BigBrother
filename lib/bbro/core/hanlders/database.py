#!/usr/bin/env python

'''
This module consist of functions that manage database.
'''

import sqlite3 as lite
import sys

from ....base import *
from ....sentry import sentry

pathHD = pather.PATHandler(__file__)

class DBHandler(object):
    def __init__(self):
        try:
            self.con = lite.connect(os.path.join(pathHD.parent_dir()), 
                'databases', 'modules.db')
            self.cur = self.con.cursor()
        except lite.Error as e: 
            # send error to sentry
            sentry.client.captureException()
            print(color.red("An error occurred: ", e.args[0]))

    def query(self, query, param=''):
        '''
        Allow to submit a sql query
        '''
        try:
            if type(param) is not list:     
                param = [param]
            if param != '':
                return self.cur.execute(query, param)
            else:
                return self.cur.execute(query)
        except lite.Error as e:
            print(color.red("An error occurred:", e.args[0]))
            sys.exit()

    def close_connection(self):
        '''
        Close connection to database
        '''
        try:
            self.cur.close()
            self.con.close()
            return
        except lite.Error as e:
            print(color.red("An error occurred:", e.args[0]))
            sys.exit()            