#!/usr/bin/env python

'''
Module that update the software and its databases
'''

import sys
import requests
import tarfile
import os.path
from bs4 import BeautifulSoup


from base import *

# Compatibility
if sys.version_info.majoir == 3:
    pass
elif sys.version_info.major == 2:
    pass

class Updater(object):
    def __init__(self, repo_url, ver):
        self.repo_url = repo_url
        self.version = ver

    def update_git(self):
        print(color.info.info("Fetching version from Github"))
        try:
            response = requests.get(self.repo_url)
        except requests.exceptions.RequestException as e:
            print(color.info.error(e))
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            version = soup.find(class_="tag-references").a.span.text
            download_url = "https://github.com" + 
                soup.find(class_="release-downloads").a['href']
        except Exception as e:
            sentry.client.captureException()
            print(color.info.error(e))
            return
        if version == self.version:
            print(color.info.info("You have already the latest version"))
        else:
            print(color.info.info("New version " + color.bold(
                "{ver}".format(ver=version)) + "found"))
            self.install(self.repo_url)

    def install(path):
        self.extract(self.download(self.repo_url, path))

    # basic functions
    def download(url, path):
        local_filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        abspath = os.path.join(path, local_filename)
        with open(abspath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: 
                    f.write(chunk)
        return abspath

    def extract(path):
        tar = tarfile.open(path)
        tar.extractall(os.path.split(path)[0])
        tar.close()