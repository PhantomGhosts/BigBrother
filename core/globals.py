#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

import sys
import os
import yaml

from core import colors

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

########
# Vars #
########
class vars:
    # Global Variables
    with open('vars.yml', 'r') as yaml_config_file:
        config = yaml.load(yaml_config_file)
    version = config['version']
    codename = config['codename']
    status = config['status']
    appname = config['appname']
    author = config['author']
    maintainers = ["Mr.Robot"]
    licensev = config['license']
    db_path = config['database_path']
    db_name = config['database_name']

    # DEBUG_LEVEL 0 = NO DEBUGGING
    # DEBUG_LEVEL 1 = DEBUG DOWNLOADS
    # DEBUG_LEVEL 2 = DEBUG SQL QUERIES
    DEBUG_LEVEL = 0

#     usage = '\nUsage: ' + sys.argv[0] + ' -s search_query -t trojan -p vb\n\n'
#     usage += 'The search engine can search by regular search or using specified arguments:\n\nOPTIONS:\n   -h  --help\t\tShow this message\n   -t  --type\t\tMalware type, can be virus/trojan/botnet/spyware/ransomeware.\n   -p  --language\tProgramming language, can be c/cpp/vb/asm/bin/java.\n   -u  --update\t\tUpdate malware index. Rebuilds main CSV file. \n   -s  --search\t\tSearch query for name or anything. \n   -v  --version\tPrint the version information.\n   -w\t\t\tPrint GNU license.\n'

#     opts = [
#         ("type", ("virus", "worm", "ransomware", "botnet", "apt", "rootkit", "trojan", "exploitkit", "dropper")),
#         ("architecture", ("x86", "x64", "arm", "web")),
#         ("platform", ("win32", "win64", "android", "ios", "mac", "*nix32", "*nix64", "symbian")),
#         ("language", ("c", "cpp", "asm", "bin", "java", "apk", "vb", "php"))]

    # ASCII Art is a must...
    banner = '\n'
    banner += bold('''        w*"""^q_  0 ''' + red('''p" F  F _F  p^^"_''')) + bold('''__jM   j  F                                                \n''')
    banner += bold('''       _,,__   q ''' + red('''x" [  F J_ J  P  w""""''')) + bold('''_  _,"  9"                                               \n''')
    banner += bold('''      w"   "M_ ''' + red('''@ `, ",_!u_9__L F #  r^""^^''')) + bold('''"    f j"                                             \n''')
    banner += bold('''      _,,__  ''' + red('''B 9_ "v,''')) + bold(blue('''_Zp*"""""^@u# P''')) + bold(red(''' _m^"^u''')) + bold(''',a*"   j    ''') + '\t\tBigBrother: %s %s\n' % (version, codename)
    banner += bold('''    _F    `''' + red('''4 A_ "*-''')) + bold(blue('''ap"            ^Lj"''')) + bold(red(''' _smu,''')) + bold('''    _* ,   \n''') + '\t\tAuthor: %s' % author
    banner += bold('''    "__,,_ ''' + red('''jL  -- ''')) + bold(blue('''m<                5j!''')) + bold(red(''' ____*''')) + bold('''-*^   &   \n''')
    banner += bold('''    p"    ''' + red('''9p`^u,''')) + bold(blue('''av'                  `,*''')) + bold(red('''""""q''')) + bold('''_    _x"  \n''')
    banner += bold('''    q _____''' + red('''!L___''')) + bold(blue(''',M                    Lsr''')) + bold(red('''--x_''')) + bold('''"^^`""qP  \n''')
    banner += bold('''    y^    ''' + red('''"_    ''')) + bold(blue('''_J                    L_,''')) + bold(red(''',_ ?_''')) + bold('''    _#   \n''')
    banner += bold('''    F  __,_''' + red('''`^---''')) + bold(blue('''"jr                  j__''')) + bold(red('''_ ""y"''')) + bold('''"^^""_,  \n''')
    banner += bold('''     j!    ''' + red('''?s_, ''')) + bold(blue('''*"jp                g""''')) + bold(red('''""^q_b''')) + bold('''_    _F   \n''')
    banner += bold('''     L  _,w''' + red('''ma_  _x''')) + bold(blue('''"jN__          __d""''')) + bold(red('''"^c  F''')) + bold('''  "-^""    \n''')
    banner += bold('''     " J"    ''' + red('''"""  _F ''')) + bold(blue('''99Nu______g**L_"''')) + bold(red('''"s  4''')) + bold(''' A,    _P    \n''')
    banner += bold('''      j_  _-^"''' + red('''"mw^" _' ''')) + bold(blue('''# 9"N""L ^,''')) + bold(red(''' "s  b #''')) + bold('''   "--^"     \n''')
    banner += bold('''       @ j"   _''' + red('''v-wa+" ," j  #  p  r j qF''')) + bold(''' "q_   _*           \n''')
    banner += bold('''         0_  f   _''' + red('''m-**" _F _F  L _FjP ?,''')) + bold('''    "^""            \n''')
    banner += bold('''          # J   j"   ''' + red('''p"""p-^ x^ p" d''')) + bold('''_   -q__a-              \n''')
    banner += bold('''            `q  #   f   j   4   b   ^,                      \n''')
    banner += bold('''              F 9L_ b   1   4   `u_   "-^"                  \n''')
    banner += bold('''                  0 `+a_ W__ 9,___"^^"+                     \n''')
    banner += bold('''                          ""     "                          \n''')
