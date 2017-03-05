import ConfigParser
import tarfile
import yaml
import sys, os, os.path

# +++ CLASSES +++
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
class clrs:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
class info:
	info = clrs.OKBLUE + '[#] ' + clrs.ENDC
	process = clrs.WARNING + '[+] ' + clrs.ENDC
	config = clrs.HEADER + '[@] ' + clrs.ENDC
	user_input = clrs.OKGREEN + '[$] ' + clrs.ENDC
	@staticmethod
	def header(string):
		return  "%s" % (clrs.BOLD + clrs.OKBLUE + '---' + string.upper() + clrs.ENDC)
	@staticmethod
	def error(string):
		return "%s" % (clrs.FAIL + clrs.BOLD + '[*] ERROR: ' + string.upper() + clrs.ENDC)
	@staticmethod
	def success(string):
		return"%s" % (clrs.OKGREEN + string + clrs.ENDC)
	@staticmethod
	def fail(string):
		return"%s" % (clrs.FAIL + string + clrs.ENDC)	

# +++ FUNCTIONS +++
def promt(string, new_line=True):
	x = _Getch()
	if new_line:
		print "%s" % string,
	else:
		print "%s" % string
	return x()
def load_yaml(file_name):
	with open(file_name, 'r') as yaml_config_file:
		try:
			return yaml.load(yaml_config_file)
		except yaml.YAMLError as exc:
			print(info.error(exc))
def init_dir(directory):
	try: 
		os.makedirs(directory)
		print "%sfolder %s %s" % (info.process, directory, info.success("initialized"))
	except:
		print "%sfolder %s %s" % (info.process, directory, info.fail("not initialized"))
		if promt("Continue anyway? (y/n)") != 'y':
				sys.exit()
def importer(module):
	print "%sImporting %s" % (info.process, clrs.BOLD + module + clrs.ENDC),
	try:
		print info.success("succeeded")
		exec("import " + module, globals())
	except:
		print info.fail("failed")
		print "%sInstalling %s" % (info.process, module)
		try:
			os.system("pip install %s -q" % module)
		except:
			print info.error("pip required, install pip") 
def donwloader(module, path, priv_token):
	absolute_path = path + '/' + module['path'] + '/' + module['name'] + '.tar.gz'
	with open(absolute_path, "wb") as module_file:
		print "%sDownloading %s" % (info.process, clrs.BOLD + module['name'] + clrs.ENDC)
		response = requests.get(module['url'] + '&private_token=' + priv_token, stream=True)
		total_length = response.headers.get('content-length')
		if total_length is None: # no content length header
			module_file.write(response.content)
		else:
			data_length = 0
			total_length = int(total_length)
			for data in response.iter_content(chunk_size=4096):
				data_length += len(data)
				module_file.write(data)
				done = int(50 * data_length / total_length)
				sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
	 			sys.stdout.flush()
 			sys.stdout.write('\r'),
def decompresser(tar_archive_path):
	tar_archive = tar_archive_path.split('/')[-1]
	path = tar_archive_path.replace('/' + tar_archive, '')
	absolute_path = path + '/' + tar_archive.replace('.tar.gz', '')
	os.makedirs(absolute_path)
	with tarfile.open(tar_archive_path, 'r:gz') as tar:
		try:
			tar.extractall(absolute_path)
			os.remove(tar_archive_path)
			print "%sDecompressing %s %s" % (info.process, clrs.BOLD + tar_archive + clrs.ENDC, info.success('succeeded'))
		except:
			print "%sDecompressing %s %s" % (info.process, clrs.BOLD + tar_archive + clrs.ENDC, info.fail('failed'))
			os.remove(tar_archive_path)


def main():
	# +++ GATHERING INFORMATION +++
	config_options_setup = ['TEST']
	main_directory = 'BigBrother'
	print info.header("gathering information")
	print "%sReading YAML configuration file..." % info.process
	yaml_config = load_yaml('config.yml')
	# config lists
	user_private_token = raw_input("%s%sInsert the GitLab private token: %s" % (info.user_input, clrs.WARNING, clrs.ENDC))
	modules_directories = yaml_config['module_directories'] # modules directories
	modules_directories_subfolders = yaml_config['module_directories_subfolders']
	download_repositories = yaml_config['download_repositories']
	python_module_to_import = yaml_config['python_modules_needed']
	# info
	print "%s%sPRIVATE_TOKEN%s = %s" % (info.config, clrs.BOLD, clrs.ENDC, yaml_config['private_token'])
	print "%sTotal directories gathered: %s%s%s" % (info.info, clrs.BOLD, len(modules_directories) + len(modules_directories_subfolders), clrs.ENDC)
	print "%sPython modules needed: %s%s%s"% (info.info, clrs.BOLD, len(python_module_to_import), clrs.ENDC)
	if promt("%sContinue? (y/n)%s" % (clrs.BOLD + clrs.WARNING, clrs.ENDC)) != 'y':
		sys.exit()
	print '\r',


	# +++ IMPORTING +++
	for module in python_module_to_import:
		importer(module)


	# +++ INITIALIZING +++
	print "%s" % info.header("initialization")
	# main directory
	if not os.path.exists(main_directory):
		init_dir(main_directory)			
	else:
		print "%s" % info.error("folder called BigBrother")
		sys.exit()
	# modules directories
	for num, directory in enumerate(modules_directories):
		init_dir(main_directory + '/' + directory)
		# subfolder
		for module_directory in modules_directories_subfolders:
			init_dir(main_directory + '/' + directory + '/' + module_directory)


	# +++ DOWNLOADING MODULES +++
	print "%s" % info.header("downloading modules")
	for module in download_repositories:
		donwloader(module, main_directory + '/' + modules_directories[0], user_private_token)
	print "                                                    \r",
	print "%sDownloaded %s%d%s modules" % (info.info, clrs.BOLD, len(download_repositories), clrs.ENDC)


	# +++ DECOMPRESSING MODULES
	print "%s" % info.header("decompressing modules")
	for module in download_repositories: 
		decompresser(main_directory + '/' + modules_directories[0] + '/' + module['path'] + '/' + module['name'] + '.tar.gz')


	# ++ CONFIG ++
	config = ConfigParser.RawConfigParser()
	print "%s" % info.header("configuration")
	print "%s%s%sediting config.cfg%s" % (info.info, clrs.BOLD, clrs.FAIL, clrs.ENDC)
	config.add_section('user_profile')
	config.set('user_profile', 'PRIVATE_TOKEN', user_private_token)
	for option in config_options_setup:
		user_set = raw_input("%s%s: " % (info.user_input, clrs.BOLD + option + clrs.ENDC))
		config.set('user_profile', option, user_set)
	# write in config file
	with open('BigBrother/config.cfg', 'wb') as configfile:
		config.write(configfile)


if __name__ == "__main__":
	main()