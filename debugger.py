from core.globals import vars
from core.colors import *

# COMPATIBILITY
import sys
if sys.version_info.major == 3:
    raw_input = input
elif sys.version_info.major == 2:
    pass
# TEST FUNCTIONS
padding = "                                                                        "
def test_var(var, name):
    try:
        foo = var
        print("%s%s" % (bold(name.upper()), padding[len(name):]) + bold(green("SUCCESS")))
    except:
        print("%s%s" % (bold(name.upper()), padding[len(name):]) + bold(red("FAIL")))
def test_import(name):
    try:
        exec('import %s' % name)
        print("%s%s" % (bold(name.upper()), padding[len(name):]) + bold(green("SUCCESS")))
    except IOError as e:
        print("%s%s" % (bold(name.upper()), padding[len(name):]) + bold(red("FAIL")))
        print(e)

vars.DEBUG_LEVEL = 3
# START TEST
imports = ['core.colors', 'core.cli', 'core.crypt', 'core.database', 'core.search', 'core.update']
test_var(vars.banner, "banner")
for imp in imports:
    test_import(imp)
import core.database as database
db_handler = database.DBHandler()