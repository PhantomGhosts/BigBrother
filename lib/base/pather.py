#!/usr/bin/env python

'''
This module contains main complex functions that operate over relative
pathes.
'''

import os.path

class PATHandler(object):
    def __init__(self, file):
        self.file = file

    def parent_dir(self):
        '''
        return parent directory
        '''
        return os.path.abspath(os.path.dirname(self.file))