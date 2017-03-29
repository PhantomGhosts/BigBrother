#!/usr/bin/env python

'''
Module that update the software and its databases
'''

import os
import shutil
from sys import exit
import os.path
import tarfile
import requests
from bs4 import BeautifulSoup

from ...base import *
from ...sentry import sentry
from ...clint import progress

class Updater(object):
    def __init__(self, path, ver, url):
        self.inst_path = path
        self.repo_url = url
        self.version = ver

    def update_all(self):
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
            download_url = "https://github.com" + \
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
                "{ver}".format(ver=version)) + " found"))
            # install
            if self.install(self.inst_path, download_url):
                print(color.info.info("Need to be restarted for changes to be effective"))
                exit()

    def install(self, path, url):
        try:
            # downloaded file name
            dl_file = self.download(url, path)
            # change directory
            os.chdir(path)
            # extract in path directory
            inst_module = self.extract(dl_file)
            # normalize name
            inst_module_norm = inst_module[:inst_module.find('-')]
            if inst_module_norm in os.listdir():
                shutil.rmtree(inst_module_norm)
            shutil.move(inst_module, inst_module_norm)
            print(color.info.info(color.info.success("Installation completed")))
            return 1
        except Exception as e:
            print(color.info.info(color.info.fail("Installation failed")))
            print(color.info.error(e))
            return 0

    def download(self, url, path):
        '''
        Download module from [url] to [path]
        '''
        # get name of file to downaload
        local_filename = url.split('/')[-1]
        try:
            stream = requests.get(url, stream=True)
            total_length = int(stream.headers['Content-Length'])
        except requests.exceptions.RequestException as e:
            print(color.info.error(e))
            return
        # change to downlaod dir
        try:
            os.chdir(path)
        except Exception as e:
            print(color.info.error(e))
            return
        # write on file
        with open(local_filename, 'wb') as f:
            for chunk in progress.bar(stream.iter_content(chunk_size=1024), 
                label=local_filename, expected_size=(total_length/1024)): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        return local_filename

    def extract(self, filename):
        try:
            tar = tarfile.open(filename)
            repo = tar.getnames()[0]
            # remove old repo
            if repo in os.listdir():
                shutil.rmtree(repo)
            # extract in current directory
            tar.extractall()
            return repo
        except Exception as e:
            print(color.info.error(e))
            return
        finally:
            tar.close()
            os.remove(filename)
        
