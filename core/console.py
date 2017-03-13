import ConfigParser
import os, os.path, shlex
from commands.base import *

# FIRST LEVEL
def useful_folders(path, separator):
    folders = extract_path(path, separator)
    refined_folders = []
    if len(folders) == 0:
        return []
    refined_folders.append(folders[0])
    if len(folders) >= 4:
        refined_folders.append(folders[3])
    if len(folders) == 5:
        refined_folders.append(folders[4])
    return refined_folders
# SECOND LEVEL
def command_IN(path, path_separator):
    folders = useful_folders(path, path_separator)
    console_name = info.underline("BBro")
    if len(folders) >= 0:
        string = console_name
    if len(folders) >= 1:
        console_kingdom = info.bold(clrs.format_clr(folders[0], "CYAN"))
        string = string + ' {0}'.format(console_kingdom)
    if len(folders) >= 2:
        console_family = info.bold(clrs.format_clr(folders[1], "YELLOW"))
        string = string + '[{0}]'.format(console_family)
    if len(folders) >= 3:
        console_specie = info.bold(clrs.format_clr(folders[2], "RED"))
        string = string + '({0})'.format(console_specie)
    string = string + ' > '
    inputs = shlex.split(raw_input(string))
    cmd = inputs[0]
    if len(inputs) > 1:
        args = inputs[1:]
    else:
        args = []
    return {'cmd': cmd, 'args': args}


# MAIN
def main():
    print info.process("Starting {0}...".format(info.bold("console")))
    from commands.select import select

    path_separator = "modules"                                                                      # module folder
    path = os.path.realpath(__file__).split('core')[0].strip('/\\')                                 # path to main project
    modules_path = os.path.join(path, path_separator)

    while (1):
        INPUT = command_IN(modules_path, path_separator)
        if INPUT['cmd'] == 'select':
            currcmd = select(modules_path)
            if len(INPUT['args']) == 1:
                currcmd.run(INPUT['args'][0])
            else:
                currcmd.help()
        else:
            continue


if __name__ == "__main__":
    main()