#!/usr/bin/env python

'''
Sentry integration module
'''

from raven import Client

client = Client(
    # dns url
    dns='https://3dc3f3d21a554b4795c06b5f8a21ac02:39441beb0bb842d8a89 \
    7413e126a7a10@sentry.io/147629',
    # version
    release='0.4.0')
