#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

import re
import sys
import rlcompleter
import readline

from core.globals import *
# from core import search
# from core.update_handler import Updater
from core import database
from core.colors import *

# Compatilibility to Python3
if sys.version_info.major == 3:
    raw_input = input
elif sys.version_info.major == 2:
    pass
else:
    sys.stderr.write("What kind of sorcery is this?!\n")
    sys.quit()


class Controller(object):

    def __init__(self):
        self.modules = None
        self.currentmodule = None
        self.db = database.DBHandler()
        self.commands = [("search", "Search for spywares according to a \
                           filter,\n\t\t\texample: 'search cpp worm'."),
                         ("list all", "Lists all available modules"),
                         ("use", "Selects a module by ID"),
                         ("info", "Retreives information about module"),
                         ("get", "Downloads selected module"),
                         ("update-db", "Updates the database"),
                         ("help", "Displays this help..."),
                         ("exit", "Exits...")]

        self.commandsWithoutDescription = {'search': '', 'list all': '', 'use': '', 'info': '',
                                           'get': '', 'update-db': '', 'help': '', 'exit': ''}

        # self.searchmeth = [("arch", "architecture: x86, x64, arm7 etc..)"),
        #                    ("plat", "platform: win32, win64, mac, android etc.."),
        #                    ("lang", "language: c, cpp, vbs, bin etc..")]
        #                    ("vip", "1 or 0")]                                WHAT IS VIP?

        self.modules = self.GetModules()
        completer = Completer(self.commandsWithoutDescription)

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)

    def GetModules(self):
        return self.db.get_full_details()

    def MainMenu(self):
        # This will give you the nice prompt you like so much
        while (True):
            try:
                print_stack = underline('BBro ')
                if self.currentmodule is not None:
                    module = self.db.query("SELECT id, specie, family, kingdom FROM %s WHERE ID=?" \
                             % vars.db_name, self.currentmodule)[0]
                    print_stack += "{0}({1})[{2}]".format(bold(cyan(module[1])), \
                                                          bold(yellow(module[2])), \
                                                          bold(red(module[3])))
                    cmd = raw_input(print_stack + print_stack + ' > ').strip()
                else:
                    cmd = raw_input(underline('BBro ') + '> ').strip()
            except KeyboardInterrupt:
                print(info.process + bold(red("BigBrother")) + "is always watching you!")
                exit()

            self.actOnCommand(cmd)

    def actOnCommand(self, cmd):
        try:
            while cmd == "":
                return

            if cmd == 'help':
                print(" Available commands:\n")
                for (cmd, desc) in self.commands:
                    print("\t%s\t%s" % ('{0: <12}'.format(cmd), desc))
                print('')
                return

            if cmd == 'exit' or cmd == 'quit':
                print("\n%sExiting..." % info.process)
                sys.exit(1)

#             # Checks if normal or freestyle search
#             if re.match('^search', cmd):
#                 manySearch = manysearches.MuchSearch()
#                 try:
#                     args = cmd.rsplit(' ')[1:]
#                     manySearch.sort(args)
#                 except:
#                     print(red('[!]') + 'Uh oh, Invalid query.')
#                 return

#             if cmd == 'update-db':
#                 update_handler = Updater()
#                 db_ver = update_handler.get_maldb_ver()
#                 update_handler.update_db(db_ver)
#                 return

#             if cmd == 'report-mal':
#                 rprt_name = raw_input("Name of malware: ")
#                 rprt_type = raw_input("Type of malware: ")
#                 rprt_version = raw_input("Version: ")
#                 rprt_lang = raw_input("Language: ")
#                 rprt_src = raw_input("Source / Binary (s/b): ")
#                 rprt_arch = raw_input("Win32, ARM etc. ? ")
#                 rprt_reporter = raw_input(
#                     "Your name for a thank you note on theZoo.\n"
#                     "Please notice that this will be public!\n\nName: ")
#                 rprt_comments = raw_input("Comments? ")

#                 report = ("//%s//\n" % rprt_name)
#                 report += ("///type/%s///\n" % rprt_type)
#                 report += ("///ver/%s///\n" % rprt_version)
#                 report += ("///lang/%s///\n" % rprt_lang)
#                 report += ("///src/%s///\n" % rprt_src)
#                 report += ("///arch/%s///\n" % rprt_arch)
#                 report += ("//reporter/%s//\n" % rprt_reporter)
#                 report += ("//comments/%s//\n" % rprt_comments)

#                 # Just to avoid bots spamming us...
#                 email = "info"
#                 email += "\x40"
#                 email += "morirt\x2ecom"
#                 print("-------------- Begin of theZoo Report --------------")
#                 print(report)
#                 print("-------------- Ending of theZoo Report --------------")
#                 print("To avoid compromising your privacy we have chose this method of reporting.")
#                 print("If you have not stated your name we will not write a thanks in our README.")
#                 print("Your email will remain private in scenario and will not be published.")
#                 print("")
#                 print("Please create an archive file with the structure described in the README file")
#                 print("And attach it to the email. ")
#                 print("Please send this report to %s" % email)

#                 return

#             if cmd == 'get':
#                 update_handler = Updater()
#                 try:
#                     update_handler.get_module(self.currentmodule)
#                 except:
#                     print(red('[-] ') + 'Error getting malware.')
#                 return
#             # If used the 'use' command
#             if re.match('^use', cmd):
#                 try:
#                     cmd = re.split('\s+', cmd)
#                     self.currentmodule = int(cmd[1])
#                     cmd = ''
#                 except TypeError:
#                     print('Please enter malware ID')
#                 except:
#                     print('The use method needs an argument.')
#                 return

#             if cmd == 'list':
#                 print("\nAvailable Modules:")
#                 manySearch = manysearches.MuchSearch()
#                 manySearch.print_payloads(self.db.get_modules_list(), ["%", "Name", "Type"])
#                 return

#             if cmd == 'info':
#                 if self.currentmodule is None:
#                     print(red("[!] ") + "First select a malware using the \'use\' command")
#                     return
#                 m = self.db.get_mod_info(self.currentmodule)
#                 manySearch = manysearches.MuchSearch()
#                 manySearch.print_payloads(m, ["%", "Name", "Ver.", "Author", "Lang", "Date", "Arch.", "Plat.", "Tags"])
#                 return

            else:
                print(vars.info + "Unknown command: %s" % cmd)

        except KeyboardInterrupt:
            print("\n%sExiting..." % info.process)
            sys.exit()
