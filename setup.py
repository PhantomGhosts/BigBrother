import ConfigParser
import tarfile
import yaml
import sys, shutil, os, os.path

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
		return "%s" % (clrs.BOLD + clrs.OKBLUE + '---' + string.upper() + clrs.ENDC)
	@staticmethod
	def error(string):
		return "%s" % (clrs.FAIL + clrs.BOLD + '[*] ERROR: ' + string.upper() + clrs.ENDC)
	@staticmethod
	def success(string):
		return "%s" % (clrs.OKGREEN + string + clrs.ENDC)
	@staticmethod
	def fail(string):
		return "%s" % (clrs.FAIL + string + clrs.ENDC)	
	@staticmethod
	def bold(string):
		return "%s" % (clrs.BOLD + str(string) + clrs.ENDC)

# +++ FUNCTIONS +++
def prompt(string, new_line=True):
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
def authenticate():
	euid = os.geteuid()
	if euid != 0:
		print "%s%sPlease run as root%s" % (info.info, clrs.FAIL + clrs.BOLD, clrs.ENDC)
		sys.exit()
def init_dir(directory):
	try: 
		os.makedirs(directory)
		print "%sfolder %s %s" % (info.process, directory, info.success("initialized"))
	except:
		print "%sfolder %s %s" % (info.process, directory, info.fail("not initialized"))
		if prompt("Continue anyway? (y/n)") != 'y':
				sys.exit()
def importer(module):
	print "%sImporting %s" % (info.process, info.bold(module)),
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
	absolute_path = '/'.join([path, module['path'], module['name'] + '.tar.gz'])
	with open(absolute_path, "wb") as module_file:
		print "%sDownloading %s" % (info.process, info.bold(module['name']))
		try:
			response = requests.get(module['url'] + '&private_token=' + priv_token, stream=True)
		except:
			print info.error("you are offline")
			sys.exit()
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
	try:
		with tarfile.open(tar_archive_path, 'r:gz') as tar:
			tar.extractall(absolute_path)
			print "%sDecompressing %s %s" % (info.process, info.bold(tar_archive), info.success('succeeded'))
			return 1
	except:
		print "%sDecompressing %s %s" % (info.process, info.bold(tar_archive), info.fail('failed'))
		return 0
	finally:
		os.remove(tar_archive_path)
def cleaner(path, file_to_del):
	target = os.path.join(path, os.listdir(path)[0])		# -
	for file in os.listdir(target):							# | Move all files in directory
		shutil.move(os.path.join(target, file), path)		# | extracted in external dir
	shutil.rmtree(target)									# -
	for file in os.listdir(path):							# -
		for entry in file_to_del:							# | Remove all files that have
			if file == entry:								# | to be deleted in config.yml
				if os.path.isdir(file):						# | 
					shutli.rmtree(os.path.join(path, file))	# | 
				else:										# | 
					os.remove(os.path.join(path, file))		# -


def main():
	# authentication
	authenticate()
	
	# +++ GATHERING INFORMATION +++
	config_options_setup = ['TEST']
	main_directory = '/usr/share/BigBrother'
	print info.header("gathering information")
	print "%sReading YAML configuration file..." % info.process
	yaml_config = load_yaml('config.yml')
	print "%sSearching %s" % (info.process, info.bold(".gitlab_priv_token")),
	try:
		with open(os.path.join(os.path.expanduser('~'), '.gitlab_priv_token'), 'r') as private_file:
			user_private_token = private_file.readline().replace('\n', '')
		print info.success("found")
	except:
		print info.fail("not found")
		user_private_token = raw_input("%s%sInsert the GitLab private token: %s" % (info.user_input, clrs.WARNING, clrs.ENDC))
	# config lists
	modules_directories = yaml_config['module_directories'] # modules directories
	modules_directories_subfolders = yaml_config['module_directories_subfolders']
	download_repositories = yaml_config['download_repositories']
	python_module_to_import = yaml_config['python_modules_needed']
	file_to_delete = yaml_config['file_to_delete']
	# info
	print "%s%s = %s" % (info.config, info.bold("PRIVATE_TOKEN"), user_private_token)
	print "%sTotal directories gathered: %s" % (info.info, info.bold(len(modules_directories) + len(modules_directories_subfolders)))
	print "%sPython modules needed: %s" % (info.info, info.bold(len(python_module_to_import)))
	print "%sModules to download: %s" % (info.info, info.bold(len(download_repositories)))
	if prompt("%sContinue? (y/n)%s" % (clrs.BOLD + clrs.WARNING, clrs.ENDC)) != 'y':
		sys.exit()
	print '\r',


	# +++ IMPORTING +++
	for module in python_module_to_import:
		importer(module)


	# +++ INITIALIZING +++
	print info.header("initialization")
	# main directory
	if not os.path.exists(main_directory):
		init_dir(main_directory)			
	else:
		print info.error("folder called BigBrother")
		sys.exit()
	# modules directories
	for num, directory in enumerate(modules_directories):
		init_dir(os.path.join(main_directory, directory))
		# subfolder
		for module_directory in modules_directories_subfolders:
			init_dir(os.path.join(main_directory, directory, module_directory))


	# +++ DOWNLOADING MODULES +++
	print info.header("downloading modules")
	for module in download_repositories:
		donwloader(module, os.path.join(main_directory, modules_directories[0]), user_private_token)
	print "                                                    \r",
	print "%sDownloaded %s modules" % (info.info, info.bold(len(download_repositories)))


	# +++ DECOMPRESSING MODULES
	print info.header("decompressing modules")
	pre_path = os.path.join(main_directory, modules_directories[0])
	decompressed_files_count = 0
	for module in download_repositories: 
		decompressed_files_count += decompresser(os.path.join(pre_path, module['path'], module['name'] + '.tar.gz'))
	print "%sTotal decompressed files: %s" % (info.info, info.bold(decompressed_files_count))


	# +++ CLEANING +++
	print info.header("cleaning")
	print "%sFiles to remove: %s" % (info.info, info.bold(len(file_to_delete)))
	print "%sTotal files to remove: %s" % (info.info, info.bold(decompressed_files_count * 3))
	for module in download_repositories:
		print "%s%s" % (info.process, module['name']),
		try:
			cleaner(os.path.join(pre_path, module['path'], module['name']), file_to_delete)
			print info.success("cleaned")
		except:
			print info.fail("not cleaned")

	# +++ CONFIG +++
	config = ConfigParser.RawConfigParser()
	print "%s" % info.header("configuration")
	print "%s%s%sediting config.cfg%s" % (info.info, clrs.BOLD, clrs.FAIL, clrs.ENDC)
	config.add_section('user_profile')
	config.set('user_profile', 'PRIVATE_TOKEN', user_private_token)
	for option in config_options_setup:
		user_set = raw_input("%s%s: " % (info.user_input, info.bold(option)))
		config.set('user_profile', option, user_set)
	# write in config file
	with open('BigBrother/config.cfg', 'wb') as configfile:
		config.write(configfile)


if __name__ == "__main__":
	main()