#!/usr/bin/env python

CYAN = '\033[96m'
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
def cyan(str):
    return CYAN + str + WHITE
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
        return ''.join([BOLD, BLUE, '---', str(string.upper()), WHITE])
    @staticmethod
    def info(string):
        return ''.join([BLUE, '[#] ', WHITE, str(string)])
    @staticmethod
    def process(string):
        return ''.join([YELLOW, '[+] ', WHITE, str(string)])
    @staticmethod
    def config(string):
        return ''.join([MAGENTA, '[@] ', WHITE, str(string)])
    @staticmethod
    def user_input(string):
        return ''.join([GREEN, '[$] ', WHITE, str(string)])
    @staticmethod
    def error(string, num):
        return ''.join([RED, BOLD, '[*] ERROR: ', str(string).upper(), WHITE])
    @staticmethod
    def success(string):
        return ''.join([GREEN, str(string), WHITE])
    @staticmethod
    def fail(string):
        return ''.join([RED, str(string), WHITE])
    @staticmethod
    def bold(string):
        return ''.join([BOLD, str(string), WHITE])
    @staticmethod
    def underline(string):
        return ''.join([UNDERLINE, str(string), WHITE])