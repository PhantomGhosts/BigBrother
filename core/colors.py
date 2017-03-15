#!/usr/bin/env python

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[0m'
MAGENTA = '\033[35m'
BOLD = '\033[01m'
UNDERLINE = '\033[04m'

def bold(str):
    return BOLD + str + WHITE
def underline(str):
    return UNDERLINE + str + WHITE
def purple(str):
    return PURPLE + str + WHITE
def blue(str):
    return BLUE + str + WHITE
def green(str):
    return GREEN + str + WHITE
def red(str):
    return RED + str + WHITE
def yellow(str):
    return YELLOW + str + WHITE
def white(str):
    return WHITE + str + WHITE

class info(object):
    @staticmethod
    def header(string):
        return ''.join([clrs.BOLD, clrs.BLUE, '---', str(string.upper()), clrs.ENDC])
    @staticmethod
    def info(string):
        return ''.join([clrs.BLUE, '[#] ', clrs.ENDC, str(string)])
    @staticmethod
    def process(string):
        return ''.join([clrs.YELLOW, '[+] ', clrs.ENDC, str(string)])
    @staticmethod
    def config(string):
        return ''.join([clrs.MAGENTA, '[@] ', clrs.ENDC, str(string)])
    @staticmethod
    def user_input(string):
        return ''.join([clrs.GREEN, '[$] ', clrs.ENDC, str(string)])
    @staticmethod
    def error(string, num):
        return ''.join([clrs.RED, clrs.BOLD, '[*] ERROR.%03d: ' % num, str(string).upper(), clrs.ENDC])
    @staticmethod
    def success(string):
        return ''.join([clrs.GREEN, str(string), clrs.ENDC])
    @staticmethod
    def fail(string):
        return ''.join([clrs.RED, str(string), clrs.ENDC])
    @staticmethod
    def bold(string):
        return ''.join([clrs.BOLD, str(string), clrs.ENDC])
    @staticmethod
    def underline(string):
        return ''.join([clrs.UNDERLINE, str(string), clrs.ENDC])