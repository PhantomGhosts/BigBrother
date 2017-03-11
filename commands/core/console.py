import curses, os.path, sys

# CLASSES
class console_window(object):
	# Defining a console_window class to
	# make a default console_window
	def __init__(self, scr, path):
		self.path = path
		self.scr = scr
		Y, X = self.scr.getmaxyx()
		self.X, self.Y = X, Y
		curses.echo()
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i, i, -1)

	def prompt(self, command=None):
		if command != None:
			prompted = command
		else:
			prompted = self.scr.getstr()
		self.refresh()
		return prompted.strip(' ')
	def set_path(self):
		folders = extract_path(self.path)
		self.scr.move(self.Y - 2, 2)
		self.scr.addstr("BBro", curses.A_UNDERLINE)
		try:
			folders[0]
			self.scr.addstr(' ')
			self.scr.addstr(folders[0], use_color('003') + curses.A_BOLD)
			try:
				folders[3]
				self.scr.addstr('[')
				self.scr.addstr(folders[-2], use_color('008') + curses.A_BOLD)
				self.scr.addstr(']')
				try:
					folders[4]
					self.scr.addstr('(')
					self.scr.addstr(folders[-1], use_color('006') + curses.A_BOLD)
					self.scr.addstr(')')
				except:
					pass
			except:
				pass
		except:
			pass
		self.scr.addstr(' > ')
		self.scr.refresh()
	def erase_board(self):
		self.scr.move(self.Y - 3, 2)
		self.scr.clrtobot()
	def refresh(self):
		self.erase_board()
		self.set_path()
class screen_window(object):
	def __init__(self, scr, console):
		self.state = ''
		self.scr = scr
		self.console = console
		Y, X = self.scr.getmaxyx()
		self.X_win, self.Y_win = X-2, Y-2-1
		self.screen = curses.newwin(self.Y_win-4, self.X_win-4, 2, 2)
		Y, X = self.screen.getmaxyx()
		self.X, self.Y = X, Y
		self.screen.clear()

	def erase_board(self):
		self.screen.move(0, 0)
		self.screen.clrtobot()
		self.screen.refresh()
	def sign_border(self, name, color):
		console_string = color_translation(color + clrs.BOLD + (self.X_win-4-len(name))/2*'#' + ' ' + name + ' ' + (self.X_win-4-len(name))/2*'#' + len(name)%2*'#' + clrs.ENDC)
		for n in range(len(console_string)):
			self.scr.addstr(1, 2, console_string[n][0], use_color(console_string[n][1]) + eval("curses.%s" % console_string[n][2]))
			self.scr.addstr(self.Y_win-1, 2, ((self.X_win-2)*'#'), use_color(console_string[n][1]) + eval("curses.%s" % console_string[n][2]))
	def write_log(self, string, method='info'):
		if self.state != 'log':
			self.erase_board()
		self.state = 'log'
		self.sign_border("console log", clrs.RED)
		# writing
		string_list = color_translation(string)
		self.screen.move(0, 0)
		for elem in string_list:
			self.screen.insertln()
			info.method(self.screen, method)
			if elem[2] != 0:
				effectt = eval("curses.%s" % elem[2])
				self.screen.addstr(elem[0], use_color(elem[1]) + effectt)
			else:
				self.screen.addstr(elem[0], use_color(elem[1]))
		self.screen.refresh()
		self.console.refresh()
	def write_path(self):									# OBSOLETE
		if self.state != 'path':
			self.erase_board()
		self.state = 'path'
		self.sign_border("path list", clrs.BLUE)
		# writing
		alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		while len(extract_path(self.console.path)) != 5:
			self.erase_board()
			folders = os.listdir(self.console.path)
			try:
				folders[0]
			except:
				self.write_log("%s%sEmpty directory%s" % (clrs.RED, clrs.BOLD, clrs.ENDC))
				self.write_log("Back to folders?")
				break
			for n, elem in enumerate(folders):
				try:
					self.screen.move(n+1, 3)
				except:
					curses.endwin()
				self.screen.addstr(alphabet[n] + ' - ')
				self.screen.addstr(elem, use_color('008') + curses.A_BOLD)
			self.console.set_path()
			self.screen.refresh()
			self.console.refresh()
			try:
				self.console.path = os.path.join(self.console.path, folders[alphabet.index(self.console.scr.getkey())])
			except:
				pass

class clrs(object):
	BLACK = "color.001 "
	BLUE = "color.002 "
	CYAN = "color.003 "
	GREEN = "color.004 "
	MAGENTA = "color.005 "
	RED = "color.006 "
	WHITE = "color.007 "
	YELLOW = "color.008 "
	BOLD = "effect.A_BOLD "
	UNDERLINE = "effect.A_UNDERLINE"
	REVERSE = "effect.A_REVERSE"
	ENDC = "clr.ENDC"
	TRUE_BLACK = "001"
	TRUE_BLUE = "002"
	TRUE_CYAN = "003"
	TRUE_GREEN = "004"
	TRUE_MAGENTA = "005"
	TRUE_RED = "006"
	TRUE_WHITE = "007"
	TRUE_YELLOW = "008"
class info(object):
	@staticmethod
	def method(scr, meth, **coordinates):
		method = {'info': {'symbol': '#', 'color': clrs.TRUE_BLUE}, 'process': {'symbol': '+', 'color': clrs.TRUE_YELLOW}}
		if 'x' in coordinates and 'y' in coordinates:
			scr.move(coordinates['y'], coordinates['x'])
		scr.addstr("[")
		if meth in method:
			scr.addstr(method[meth]['symbol'], use_color(method[meth]['color']))
		else:
			scr.addstr('-', use_color(clrs.CYAN))
		scr.addstr("] ")
		scr.refresh()

# +++ FUNCTIONS +++
# BASIC LEVEL
def color_translation(string):
	# color translation
	string_list = []
	if string.find("color.") != -1:
		string_array = string.split("color.")
		for elem in string_array:
			if elem == '':
				continue
			elif elem.find("effect.") != -1:
				effect = elem.split('effect.')[-1].split(' ')[0]
				elem = elem.replace('effect.%s '% effect, '')
			else:
				effect = 0
			elem_color = elem[0:3]
			elem = elem.replace(elem_color + ' ', '')
			elem_string = elem.split('clr.ENDC')[0]
			string_list.append((elem_string, elem_color, effect))
	else:
		string_list = [(string, "007", 0)]
	return string_list
def use_color(color):
		color_dict = {'001': curses.COLOR_BLACK, '002': curses.COLOR_BLUE, '003': curses.COLOR_CYAN, 
					  '004': curses.COLOR_GREEN, '005': curses.COLOR_MAGENTA, '006': curses.COLOR_RED, 
					  '007': curses.COLOR_WHITE, '008': curses.COLOR_YELLOW}
		try:
			return curses.color_pair(color_dict[color])
		except curses.ERR:
			pass
def extract_path(path):
	if path.find('modules/') == -1:
		raise Exception
	path = path.split('modules/')[-1]
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

def debug(stdscr):
	standard_path = "/home/mr_robot/Desktop/Operations/test/BigBrother/modules/windows"
	console = console_window(stdscr, standard_path)		# - initializing 
	screen = screen_window(stdscr, console)				# - window objects
	screen.write_path()
	while (1):
		command = console.prompt()
		if command == 'q':
			sys.exit()

if __name__ == "__main__":
	curses.wrapper(debug)