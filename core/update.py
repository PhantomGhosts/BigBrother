#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

import sys
from os import remove, rename, mkdir
from shutil import rmtree
import os.path
import subprocess

# Compatilibility to Python3
if sys.version_info.major == 3:
    from urllib.request import urlopen
elif sys.version_info.major == 2:
    from urllib2 import urlopen
    import urllib2
else:
    sys.stderr.write("What kind of sorcery is this?!\n")

from core.globals import vars
from core import database
from core.colors import *
from core import crypt

class Updater:

    def __init__(self):
        self.db = database.DBHandler()

#     def get_maldb_ver(self):
#         '''
#         Get current malwareDB version and see if we need an update
#         '''
#         try:
#             with file(vars.maldb_ver_file) as f:
#                 return f.read()
#         except IOError:
#             print(
#                 "No malware DB version file found.\nPlease try to git clone the repository again.\n")
#             return 0

#     def update_db(self, curr_db_version):
#         '''
#         Just update the database from GitHub
#         :return:
#         '''
#         if vars.DEBUG_LEVEL is 1:
#             print(locals())
#         response = urlopen(
#             vars.giturl_dl + vars.maldb_ver_file)
#         new_maldb_ver = response.read()
#         if new_maldb_ver == curr_db_version:
#             print(green('[+]') + " theZoo is up to date.\n" + green('[+]') + " You are at " + new_maldb_ver + " which is the latest version.")
#             return

#         print(red('[+]') + " A newer version is available: " + new_maldb_ver + "!")
#         print(red('[+]') + " Updating...")

#         # Get the new DB and update it

#         self.download_from_repo(vars.db_path)
#         self.db.close_connection()
#         remove(vars.db_path)
#         rename("maldb.db", vars.db_path)
#         self.db.renew_connection()

#         # Write the new DB version into the file

#         f = open(vars.maldb_ver_file, 'w')
#         f.write(new_maldb_ver)
#         f.close()
#         return

    def get_module(self, id, password):
        loc = self.db.get_mod_path(id)[0]  # get mdoule location
        local = self.db.get_mod_info(id)[0]
        source_path = '/'.join(vars.download_server, loc[1], loc[0]).lower()
        destpath = os.path.join('modules', local[4], local[3], 
                                local[2], local[1], local[0]).lower()
        self.download(source_path, destpath, '.dat')    # get from server
        self.download(source_path, destpath, '.sha256')
        print(info.process("Successfully downloaded a new module."))
        if self.check_sha256(destpath) == 1:
            self.installer(destpath, password)
        else:
            rmtree(destpath)
            print(info.process("removed %s" % loc[0]))

    def download(self, filepath, destpath, suffix=''):
        if vars.DEBUG_LEVEL is 1:
            print(locals())
        file_name = filepath.rsplit('/')[-1] + suffix

        if suffix is not '':
            url = filepath + '/' + file_name
        else:
            url = filepath
        u = urlopen(url)
        folders = destpath.split(os.sep)
        a = None            # init a for store directories to create
        for x in folders:
            if a is not None:
                a = os.path.join(a, x)
            else:
                a = x
            if os.path.isdir(a) == 0:
                os.mkdir(a)
        f = open(destpath + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print(info.info("Downloading: %s Bytes: %s" % (file_name, file_size)))
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = info.process(r"%10d  [%3.2f%%]" % (
                file_size_dl, file_size_dl * 100. / file_size))
            status = status + chr(8) * (len(status) + 1)
            sys.stdout.write('\r' + status)
        f.close()
        print("\n")

    def check_sha256(destpath):
        files = os.listdir(destpath)
        sha256sum = None
        sha256dat = None
        for f in files:
            if f.split('.')[-1] == 'sha256':
                with open(os.path.join(destpath, f), 'r') as sha256:
                    sha256sum = sha256.readline().split(' ')[0]
            elif f.split('.')[-1] == 'dat':
                digester = crypt.HashDigester()
                sha256dat = digester.sha256_hash(f)
        
        if sha256sum == None or sha256dat == None:
            print(info.error("IOError: .sha256 or .dat not found"))
            return 0
        elif sha256sum == sha256dat:
            print(info.info("Module %s...Starting installation" % green("intact")))
            return 1
        else:
            print(info.info("Module %s...Starting removal" % red("corrupted")))
            return 0

    def installer(destpath, password):
        for f in os.listdir(destpath):
            if f.split('.')[-1] == '.dat':
                aes256 = crypt.AESCipher(password)
                with open(os.path.join(destpath, f), 'rb') as in_file, \
                    open(os.path.join(destpath, f.replace('.dat', '.tar.gz'), 'wb')) as out_file:
                    aes256.decrypt(in_file, out_file)
                remove(os.path.join(destpath, f))
            else:
                remove(os.path.join(destpath, f))
