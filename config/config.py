#!/usr/bin/env python

import os.path
#!/usr/bin/env python

'''
Config file
'''

import yaml

info_file = open(os.path.join(os.path.abspath('.'), 'info.yml'), 'r')
config_info = yaml.load(info_file)
info_file.close()
database_file = open(os.path.join(os.path.abspath('.'), 'database.yml'), 'r')
config_database = yaml.load(database_file)
database_file.close()
urls_file = open(os.path.join(os.path.abspath('.'), 'urls.yml'), 'r')
config_urls = yaml.load(urls_file)
urls_file.close()

class info(object):
    author = config_info['author']
    appname = config_info['appname']
    version = config_info['version']
    codename = config_info['codename']
    status = config_info['status']
    license = config_info['license']

class database(object):
    version = config_database['version']

class url(object):
    main_server = config_urls['main_server']
    repo_url = config_urls['repo_url']