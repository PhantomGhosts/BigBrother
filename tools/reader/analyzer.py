#!/bin/python

# import
import sys, getopt, re, os
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
def bold(string):
	return bcolors.BOLD + str(string) + bcolors.ENDC

# +++++ verbose symbol legend +++++
# | # - info                      |
# | + - process                   |
# | @ - config
# +++++++++++++++++++++++++++++++++
class info:
	info = bcolors.OKBLUE + '[#] ' + bcolors.ENDC
	process = bcolors.WARNING + '[+] ' + bcolors.ENDC
	config = bcolors.HEADER + '[@] ' + bcolors.ENDC

class _Getch:
    # Gets a single character from standard input.  Does not echo to the screen.
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
def promt(string):
	x = _Getch()
	print "%s" % string
	return x()

# +++++++ MAIN +++++++
def main():
	# ++++++ parser ++++++
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-f", "--file", dest="filename", help="read log data from FILE", metavar="FILE")
	parser.add_option("-o", "--output", dest="output", default="credentials.csv", help="write result on FILE", metavar="FILE")
	parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose output to stdout")
	parser.add_option("-e", "--encrypt", action="store_true", dest="encrypt", default=False, help="encrypt results")
	(options, args) = parser.parse_args()

	# +++++ options +++++
	if len(args) != 0 or options.filename == None:
		parser.error("incorrect number of arguments type -h to view help")
	if options.verbose:	
		if options.encrypt == True:
			print "%sEncrypt       %s" % (info.config, (bcolors.BOLD + bcolors.OKGREEN + "ON" + bcolors.ENDC))
		else:
			print "%sEncrypt       %s" % (info.config, (bcolors.BOLD + bcolors.FAIL + "OFF" + bcolors.ENDC))
		resume = promt("Press C to continue...")
		if resume != 'c':
			print "%s%sSTOPPED%s" % (bcolors.FAIL, bcolors.BOLD, bcolors.ENDC)
			sys.exit()
		print info.info + "reading %s ..." % bold(options.filename)

	# ++++++ main ++++++
	# read from file
	with open(options.filename, "r") as f:
		lines = f.readlines()
		# if verbose 
		if options.verbose:
			print info.info + "File length: %s" % bold(str(len(lines)) + " lines")

	# to analyze our data we have to:
	# * replace invalid values
	# * get credentials
	# *  write results

	# +++++ INVALID CHARS ++++=
	lines_refined = []
	credentials_list = []
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
	# verbose
	if options.verbose:
		print info.process + "Replaced %s" % bold("invalid characters")

	# +++++ GET CREDENTIALS +++++
	# 1.  extend array
	res = "".join(lines_refined)
	# 2. split elements
	line_splitted = re.split(' ', res.replace('\\t', ' '))
	# verbose
	if options.verbose:
		print info.process + "Lines Splitted"
		print info.info + "Elements splitted: %s" % bold(len(line_splitted))
	# 3. tidy up
	lines_refined = []
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
			lines_refined.append(element)
	# 4. append usernames
	# functions
	def recognisedFailed(string, subject="this"):
		return raw_input("%s%sWARNING - Can't recognise %s%s\n%s -> " % (bcolors.WARNING, bcolors.BOLD, subject, bcolors.ENDC, string))
	def checkDuplicate(string, arr):
		for i in arr:
			if i[0] == string:
				return True
			else:
				pass
		return False
	for x, element in enumerate(lines_refined):
		# a. user_ids
		if element.find("MIII0001.") != -1:
			index = element.find("MIII0001.")
			username = element[index:(index + 16)]
			try:
				passwd = recognisedFailed(element[(element.find(username) + len(username)):], "password")
			except:
				passwd = recognisedFailed(lines_refined[x + 1], "password")
			if passwd == '':
				passwd = element[(element.find(username) + len(username)):]
			credential = (username, passwd)
			if checkDuplicate(username, credentials_list) == False:
				credentials_list.append(credential)

		# b. emails
		if element.find("@") != -1:
			username = recognisedFailed(element, "email address")
			try:
				passwd = recognisedFailed(element[(element.find(username) + len(username)):], "password")
			except:
				passwd = recognisedFailed(lines_refined[x + 1], "password")
			if passwd == '':
				passwd = element[(element.find(username) + len(username)):]
			credential = (username, passwd)
			if checkDuplicate(username, credentials_list) == False:
				credentials_list.append(credential)
	# verbose
	if options.verbose:
		count_usernames = 0
		count_passwds = 0
		for i in credentials_list:
			if i[0] != '':
				count_usernames += 1
			if i[1] != '':
				count_passwds += 1
		print "%sUsernames extracted: %s" % (info.info, bold(count_usernames))
		print "%sPasswords extracted: %s" % (info.info, bold(count_passwds))

	# +++++ WRITE RESULTS +++++
	f = open(options.output, "a")
	for cred in credentials_list:
		f.write("%s,%s\n" % (cred[0], cred[1]))
	f.close()
	if options.verbose:
		print "%sWrited result on file %s" % (info.process, options.output)
	if options.encrypt:
		if options.verbose:
			print "%sEncrypting in AES-256 algorithm..." % info.process
		os.system("gpg -co %s --cipher-algo AES256 %s" % (options.output, options.output))

if __name__ == "__main__":
	main()