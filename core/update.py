#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

import sys
from os import remove, rename

# Compatilibility to Python3
if sys.version_info.major == 3:
    from urllib.request import urlopen
elif sys.version_info.major == 2:
    from urllib2 import urlopen
    import urllib2
else:
    sys.stderr.write("What kind of sorcery is this?!\n")

from core.globals import vars
# from core import database
from core.colors import *

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

#     def get_malware(self, id):

#         # get mal location

#         loc = self.db.query("SELECT LOCATION FROM MALWARES WHERE ID=?", id)[0][0]

#         # get from git

#         self.download_from_repo(loc, '.zip')
#         self.download_from_repo(loc, '.pass')
#         self.download_from_repo(loc, '.md5')
#         self.download_from_repo(loc, '.sha256')
#         print(bold(green("[+]")) + " Successfully downloaded a new friend.\n")

#     def download_from_repo(self, filepath, suffix=''):
#         if vars.DEBUG_LEVEL is 1:
#             print(locals())
#         file_name = filepath.rsplit('/')[-1] + suffix

#         # Dirty way to check if we're downloading a malware

#         if suffix is not '':
#             url = vars.giturl_dl + filepath + '/' + file_name
#         else:
#             url = vars.giturl_dl + filepath
#         u = urlopen(url)
#         f = open(file_name, 'wb')
#         meta = u.info()
#         file_size = int(meta.getheaders("Content-Length")[0])
#         print("Downloading: %s Bytes: %s" % (file_name, file_size))
#         file_size_dl = 0
#         block_sz = 8192
#         while True:
#             buffer = u.read(block_sz)
#             if not buffer:
#                 break
#             file_size_dl += len(buffer)
#             f.write(buffer)
#             status = r"%10d  [%3.2f%%]" % (
#                 file_size_dl, file_size_dl * 100. / file_size)
#             status = status + chr(8) * (len(status) + 1)
#             sys.stdout.write('\r' + status)
#         f.close()
#         print("\n")
