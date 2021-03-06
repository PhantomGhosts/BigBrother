#!/usr/bin/env python

    # BigBrother
    # Copyright 2017, Federico Lolli aka Mr.Robot

    # :todo:
    # add db manipulation database

import sqlite3 as lite
from core.globals import vars
import sys

class DBHandler(object):

    def __init__(self):
        try:
            self.con = lite.connect(vars.db_path)
            self.cur = self.con.cursor()
        except lite.Error as e:
            print("An error occurred:", e.args[0])
            sys.exit()


    def get_full_details(self):
        return self.cur.execute("SELECT * FROM modules").fetchall()

    def get_partial_details(self):
        return self.cur.execute("SELECT id, specie, family, kingdom, permission FROM modules").fetchall()

    def get_modules_list(self):
        return self.cur.execute("SELECT id, specie, family FROM modules").fetchall()

    # def get_mal_names(self):

        # Sqlite3 returns a tuple even if a single value is returned
        # We use x[0] for x to unpack the tuples
        # return [val[0] for val in self.cur.execute("SELECT specie, family FROM modules").fetchall()]

#     def get_mal_tags(self):
#         return [val[0] for val in self.cur.execute("SELECT DISTINCT TAGS FROM modules WHERE TAGS IS NOT NULL").fetchall()]

    def get_mod_info(self, mid):
        return self.cur.execute("SELECT specie, family, class, phylum, kingdom, permission, power FROM modules WHERE id = " \
            + str(mid)).fetchall()


    def get_mod_path(self, mid):
        return self.cur.execute("SELECT specie, family FROM modules WHERE id = " \
            + str(mid)).fetchall()

    def get_permission(self, specie):
        return self.cur.execute("SELECT permission FROM modules WHERE specie = '%s'" % specie).fetchall()[0][0]

    def get_level_permission(self, level):
        return self.cur.execute("SELECT permission FROM levels WHERE name = '%s'" % level).fetchall()[0][0]

    def query(self, query, param=''):
        if vars.DEBUG_LEVEL is 2:
            print(locals())
        try:
            if param is not '':
                return self.cur.execute(query, param if type(param) is list else [param]).fetchall()
            else:
                return self.cur.execute(query).fetchall()
        except lite.Error as e:
            print("An error occurred:", e.args[0])
            sys.exit()

    def close_connection(self):
        try:
            self.cur.close()
            self.con.close()
            return
        except lite.Error as e:
            print("An error occurred:", e.args[0])
            sys.exit()

    def renew_connection(self):
        try:
            self.con = lite.connect(vars.db_path)
            self.cur = self.con.cursor()
        except lite.Error as e:
            print("An error occurred:", e.args[0])
            sys.exit()
