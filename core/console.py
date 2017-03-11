import os, os.path
import shlex

# BASIC LEVEL
# class
class clrs(object):
	CYAN = '\033[96m'
	MAGENTA = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	REVERSE = '\033[7m'
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
# function
# FIRST LEVEL
def extract_path(path, separator):
	if path.find(separator + '/') == -1:
		raise Exception
	path = path.split(separator + '/')[-1]
	folders = []
	while 1:
		path, folder = os.path.split(path)
		if folder != "":
			folders.append(folder)
		else:
			if path != "":
				folders.append(path)
			break
	folders.reverse()
	return folders
# SECOND LEVEL
def command_IN(path):

	inputs = shlex.split(raw_input(' '.join([info.underline('BBro'), '>']) + ' '))
# BACK-END LEVEL
# class
# function
# FRONT-END LEVEL
# class
# function

# MAIN
def main():
	pass

if __name__ == "__main__":
	main()