#!/usr/bin/env python

'''
Module that update the software and its databases
'''

from os
import os.path
import shutil
import tarfile
import requests
from bs4 import BeautifulSoup

from ...base import *
from ...sentry import sentry
from ...clint import progress

class Updater(object):
    def __init__(self, path, ver):
        self.inst_path = path
        self.version = ver

    def upgrade_all(self):
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
                "{ver}".format(ver=version)) + "found"))
            # install
            self.install(self.inst_path, download_url)

    def install(path, url):
        try:
            archive_path = self.download(url, path)
            inst = self.extract(archive_path)
            inst_module = os.path.split(inst)[1]          # IMPROVE PROCESS
            if inst_module.find('-') != -1:
                inst_module = inst_module[:inst_module.find('-')]
                shutil.move(inst, os.path.join(os.path.split(inst)[0], inst_module))
            print(color.info.success("Installation completed"))
        except Exception as e:
            print(color.info.fail("Installation failed"))
            print(color.info.error(e))

    def download(url, path):
        '''
        Download module from [url] to [path]
        '''
        # get name of file to downaload
        local_filename = url.split('/')[-1]
        try:
            stream = requests.get(url, stream=True)
        except requests.exceptions.RequestException as e:
            print(color.info.error(e))
            return
        abspath = os.path.join(path, local_filename)
        total_length = int(stream.headers.get('Content-Length'))
        # write on file
        with open(abspath, 'wb') as f:
            for chunk in progress.bar(stream.iter_content(chunk_size=1024), 
                label=local_filename, expected_size=(total_length/1024)): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        return abspath

    def extract(path):
        try:
            tar = tarfile.open(path)
            repo = tar.getnames()[0]
            inst_path = os.path.split(path)[0]
            repo_path = os.path.join(inst_path, repo)
            tar.extractall()
            return repo_path
        except Exception as e:
            print(color.info.error(e))
        finally:
            tar.close()
            os.remove(path)
        
