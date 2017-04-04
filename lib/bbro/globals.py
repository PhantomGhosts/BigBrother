#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

import sys
import os
import yaml

from core.colors import *

class Completer(object):
    def __init__(self, commands):
        self.commands = commands
        self.prefix = None

    def complete(self, prefix, index):
        if prefix != self.prefix:
            self.matchingCommand = [w for w in self.commands if w.startswith(prefix)]
            self.prefix = prefix
        try:
            return self.matchingCommand[index]
        except IndexError:
            return None

# DEBUG_LEVEL 0 = NO DEBUGGING
# DEBUG_LEVEL 1 = DEBUG DOWNLOADS
# DEBUG_LEVEL 2 = DEBUG SQL QUERIES
# DEBUG_LEVEL 3 = ALL
DEBUG_LEVEL = 0

#     usage = '\nUsage: ' + sys.argv[0] + ' -s search_query -t trojan -p vb\n\n'
#     usage += 'The search engine can search by regular search or using specified arguments:\n\nOPTIONS:\n   -h  --help\t\tShow this message\n   -t  --type\t\tMalware type, can be virus/trojan/botnet/spyware/ransomeware.\n   -p  --language\tProgramming language, can be c/cpp/vb/asm/bin/java.\n   -u  --update\t\tUpdate malware index. Rebuilds main CSV file. \n   -s  --search\t\tSearch query for name or anything. \n   -v  --version\tPrint the version information.\n   -w\t\t\tPrint GNU license.\n'

#     opts = [
#         ("type", ("virus"`, "worm", "ransomware", "botnet", "apt", "rootkit", "trojan", "exploitkit", "dropper")),
#         ("architecture", ("x86", "x64", "arm", "web")),
#         ("platform", ("win32", "win64", "android", "ios", "mac", "*nix32", "*nix64", "symbian")),
#         ("language", ("c", "cpp", "asm", "bin", "java", "apk", "vb", "php"))]

