#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

import sys
import os
from optparse import OptionParser
# from imports.update_handler import Updater            # TODO
# from imports import manysearches                      # TODO
# from imports import muchmuchstrings                   # TODO
# from imports.eula_handler import EULA                 # TODO
# from imports.globals import vars                      # TODO
# from imports.terminal_handler import Controller       # TODO
# from imports import db_handler                        # TODO

__version__ = "0.2.0 Camera"
__codename__ = "Camera"
__appname__ = "BigBrother"
__authors__ = ["Mr.Robot"]
__licensev__ = "MIT"
__maintainer = "Mr.Robot"
__status__ = "Alpha"


def main():
    """                                                 # TODO
    updateHandler = Updater
    eulaHandler = EULA()
    bannerHandler = muchmuchstrings.banners()
    db = db_handler.DBHandler()
    terminalHandler = Controller()

    def filter_array(array, colum, value):
        ret_array = [row for row in array if value in row[colum]]
        return ret_array

    def getArgvs():
        parser = OptionParser()
        parser = OptionParser()
        parser.add_option("-f", "--filter", dest="mal_filter", default=[],
                          help="Filter the malwares.", action="append")
        parser.add_option("-u", "--update", dest="update_bol", default=0,
                          help="Updates the DB of theZoo.", action="store_true")
        parser.add_option("-v", "--version", dest="ver_bol", default=0,
                          help="Shows version and licensing information.", action="store_true")
        parser.add_option("-w", "--license", dest="license_bol", default=0,
                          help="Prints the GPLv3 license information.", action="store_true")
        (options, args) = parser.parse_args()
        return options

    # Here actually starts Main()
    arguments = getArgvs()

    # Checking for EULA Agreement
    a = eulaHandler.check_eula_file()
    if a == 0:
        eulaHandler.prompt_eula()

    # Get arguments

    # Check if update flag is on
    if arguments.update_bol == 1:
        a = Updater()
        a.update_db()
        sys.exit(1)

    # Check if version flag is on
    if arguments.ver_bol == 1:
        print(vars.maldb_banner)
        sys.exit(1)

    # Check if license flag is on
    if arguments.license_bol == 1:
        bannerHandler.print_license()
        sys.exit(1)

    if len(arguments.mal_filter) > 0:
        manySearch = manysearches.MuchSearch()
        print(vars.maldb_banner)
        manySearch.sort(arguments.mal_filter)
        sys.exit(1)

    # Initiate normal run. No arguments given.
    os.system('cls' if os.name == 'nt' else 'clear')
    print(vars.maldb_banner)
    while 1:
        terminalHandler.MainMenu()
    sys.exit(1)"""


if __name__ == "__main__":
    main()
