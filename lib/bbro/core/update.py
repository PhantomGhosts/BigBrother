#!/usr/bin/env python

'''
Module that update the software and its databases
'''

import sys
import os.path
from shutil import rmtree
import tarfile
import requests
from bs4 import BeautifulSoup

from base import *

class Updater(object):
    def __init__(self, path, repo_url, ver):
        self.inst_path = path
        self.repo_url = repo_url
        self.version = ver

    def upgradeAll(self):
        '''
        Upgrade BigBrother completely
        '''
        print(color.info.info("Fetching version from Github..."))
        # Retrieving github releases
        try:
            response = requests.get(self.repo_url)
        except requests.exceptions.RequestException as e:
            print(color.info.error(e))
            return
        # Getting latest release
        soup = BeautifulSoup(response.content, 'html.parser')
        try:    # Parsing info from page
            version = soup.select("ul.tag-references > li > a > span")[0].text
            download_url = "https://github.com" + 
                soup.select(".release-downloads > li > a")[1]['href']
        except Exception as e:
            sentry.client.captureException()
            print(color.info.error(e))
            return
        # check version
        if version == self.version:
            print(color.info.info("You have already the latest version"))
        else:
            print(color.info.info("New version " + color.bold(
                "{ver}".format(ver=version)) + "found"))

            # CONTINUE

    #         self.install(self.path)

    # def install(path):
    #     self.extract(self.download(self.repo_url, path))
        

    # # basic functions
    # def download(url, path):
    #     local_filename = url.split('/')[-1]
    #     r = requests.get(url, stream=True)
    #     abspath = os.path.join(path, local_filename)
    #     with open(abspath, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=1024): 
    #             if chunk: 
    #                 f.write(chunk)
    #     return abspath

    # def extract(path):
    #     tar = tarfile.open(path)
    #     tar.extractall(os.path.split(path)[0])
    #     tar.close()
    #     rmtree(path)