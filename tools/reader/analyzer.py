#!/bin/python

# import files
import sys, getopt, re
from optparse import OptionParser 

# colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# +++++ verbose symbol legend +++++
# | # - info                      |
# | + - process                   |
# +++++++++++++++++++++++++++++++++
class info:
	info = bcolors.OKBLUE + '[#] ' + bcolors.ENDC
	process = bcolors.WARNING + '[+] ' + bcolors.ENDC

# +++++++ MAIN +++++++
def main():
	# ++++++ parser ++++++
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-f", "--file", dest="filename", help="read log data from FILE", metavar="FILE")
	parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=False, help="don't print status messages to stdout")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose output to stdout")
	(options, args) = parser.parse_args()
	# +++++ options +++++
	if len(args) != 0 or options.filename == None:
		parser.error("incorrect number of arguments type -h to view help")
	if options.verbose:
		print info.info + "reading %s%s%s..." % (bcolors.BOLD, options.filename, bcolors.ENDC)

	# ++++++ main ++++++
	# read from file
	with open(options.filename, "r") as f:
		lines = f.readlines()
		# if verbose 
		if options.verbose:
			print info.info + "File length: %s%d lines%s" % (bcolors.BOLD, len(lines), bcolors.ENDC)

	# to analyze our data we have to:
	# I.	replace invalid values
	# II.	get usernames
	# 	1.		extend array
	# 	2.		split elements
	# 	3.		tidy up
	#		a.		replace BLOCK

	# I.
	lines_refined = []
	username_list = []
	for line in lines:
		line = line.replace("[CTRL][`~]", "@")
		line = line.replace("[CTRL]", "")
		line = line.replace("[ [{ ]", "'")
		line = line.replace("\\", "\\\\")
		line = line.replace("[BACKSPACE]", "\\b")
		line = line.replace("[ENTER]", "")
		line = line.replace("[SHIFT]", "\\s")
		line = line.replace("[CAPS LOCK]", "\\B")
		line = line.replace("[TAB]", "\\t")
		lines_refined.append(line)
	if options.verbose:
		print info.process + "Replaced " + bcolors.BOLD + "invalid characters" + bcolors.ENDC
	
	# II.
	# 1.  extend array
	res = "".join(lines_refined)
	# 2. split elements
	line_splitted = re.split(' ', res)
	if options.verbose:
		print info.process + "Lines Splitted"
		print info.info + "Elements splitted: " + bcolors.BOLD + "%s" % len(line_splitted) + bcolors.ENDC
	# 3. tidy up
	for element in line_splitted:
		if element.find("@") != -1 or element.find("miii0001.") != -1:
			# a. replace BLOCK
			while element.find("\\B") != -1:
				index = element.find("\\B")
				next_index = element.find("\\B", index + 2)
				element = element[:(index + 2)] + element[(index + 2):next_index].upper() + element[next_index:]
				element = element.replace("\\B", "", 2)
			# b. repalce SHIFT
			while element.find("\\s") != -1:
				index = element.find("\\s")
				element = element[:(index + 2)] + element[(index + 2)].upper() + element[(index + 3):]
				element = element.replace("\\s", "", 1)	
			if element.find("MIII0001.") != -1:
				index = element.find("MIII0001.")
				username = element[index:(index + 16)]
				username_list.append(username)
				if options.verbose:
					sys.stdout.write("\r%sUsername extracted: %s%d%s" % (info.info, bcolors.BOLD, len(username_list), bcolors.ENDC))
			else:
				pass
	print ""
if __name__ == "__main__":
	main()