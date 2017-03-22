#!/usr/bin/env python

'''
Module that update the software and its databases
'''

import sys
import requests
from bs4 import BeautifulSoup


from base import *

# Compatibility
if sys.version_info.majoir == 3:
    pass
elif sys.version_info.major == 2:
    pass

class Updater(object):
    def __init__(self, main_url, db_ver):
        self.repo_url = repo_url
        self.db_ver = db_ver

    def update_git(self):
        try:
            response = requests.get(self.repo_url)
        except equests.exceptions.RequestException as e:
            print(color.red(e))
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            version = soup.find(class_="tag-references").a.span.text
            download_url = "https://github.com" + 
                soup.find(class_="release-downloads").a['href']
        except Exception as e:
            sentry.client.captureException()
            print(color.red(e))
            return