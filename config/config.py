#!/usr/bin/env python

import os.path
import yaml

yaml_file = open(os.path.join(os.path.abspath('.'), 'vars.yml'), 'r')
config = yaml.load(yaml_file)
yaml_file.close()

class info(object):
    author = config['author']
    appname = config['appname']
    version = config['version']
    codename = config['codename']
    status = config['status']
    license = config['license']
    
class url(object):
    main_server = config['main_server']