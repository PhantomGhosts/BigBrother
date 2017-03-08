import curses, os.path, sys

# CLASSES
class console_window:
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

	def prompt(self):
		prompted = self.scr.getstr()
		if prompted.strip(' ') == 'quit' or prompted.strip(' ') == 'q':
			return 'q'
		else:
			self.refresh()
	def set_path(self):
		folders = extract_path(self.path)
		self.scr.move(self.Y - 2, 2)
		self.scr.addstr("BBro", curses.A_UNDERLINE)
		try:
			folders[0]
			self.scr.addstr(' ')
			self.scr.addstr(folders[0], use_color('default_cyan') + curses.A_BOLD)
			try:
				folders[3]
				self.scr.addstr('[')
				self.scr.addstr(folders[-2], use_color('default_yellow') + curses.A_BOLD)
				self.scr.addstr(']')
				try:
					folders[4]
					self.scr.addstr('(')
					self.scr.addstr(folders[-1], use_color('default_red') + curses.A_BOLD)
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
		try:
			self.set_path()
		except:
			pass
class screen_window:
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
		self.console.refresh()
	def write_log(self, string):
		if self.state != 'log':
			self.erase_board()
		self.state = 'log'
		string_list = color_translation(string)
		console_log_string = color_translation(clrs.RED + clrs.BOLD + (self.X_win-2-13)/2*'#' + " console log " + (self.X_win-2-13)/2*'#' + '#' + clrs.ENDC)
		for n in range(len(console_log_string)):
			self.scr.addstr(1, 2, console_log_string[n][0], use_color(console_log_string[n][1]) + eval("curses.%s" % console_log_string[n][2]))
			self.scr.addstr(self.Y_win-1, 2, ((self.X_win-2)*'#'), use_color(console_log_string[n][1]) + eval("curses.%s" % console_log_string[n][2]))
		# writing
		self.screen.move(0, 0)
		for elem in string_list:
			self.screen.insertln()
			if elem[2] != 0:
				effectt = eval("curses.%s" % elem[2])
				self.screen.addstr(0, 0, elem[0], use_color(elem[1]) + effectt)
			else:
				self.screen.addstr(elem[0], use_color(elem[1]))
		self.screen.refresh()
		self.console.refresh()
	def show_path(self):
		if self.state != 'path':
			self.erase_board()
		self.state = 'path'
		console_log_string = color_translation(clrs.BLUE + clrs.BOLD + (self.X_win-2-11)/2*'#' + " path list " + (self.X_win-2-11)/2*'#' + '#' + clrs.ENDC)
		for n in range(len(console_log_string)):
			self.scr.addstr(1, 2, console_log_string[n][0], use_color(console_log_string[n][1]) + eval("curses.%s" % console_log_string[n][2]))
			self.scr.addstr(self.Y_win-1, 2, ((self.X_win-2)*'#'), use_color(console_log_string[n][1]) + eval("curses.%s" % console_log_string[n][2]))
		# writing
		alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		while len(extract_path(self.console.path)) != 5:
			self.erase_board()
			folders = os.listdir(self.console.path)
			try:
				folders[0]
			except:
				self.write_log("%s%sEmpty directory%s" % (clrs.RED, clrs.BOLD, clrs.ENDC))
			for n, elem in enumerate(folders):
				try:
					self.screen.move(n+1, 3)
				except:
					curses.endwin()
				self.screen.addstr(alphabet[n] + ' - ')
				self.screen.addstr(elem, use_color('default_yellow') + curses.A_BOLD)
			self.console.set_path()
			self.screen.refresh()
			self.console.refresh()
			self.console.path = os.path.join(self.console.path, folders[alphabet.index(self.console.scr.getkey())])
		self.write_log("%s%sWindows_api keylogger%s" % (clrs.BLUE, clrs.BOLD, clrs.ENDC))

class clrs:
	BLACK = "color.default_black "
	BLUE = "color.default_blue "
	CYAN = "color.default_cyan "
	GREEN = "color.default_green "
	MAGENTA = "color.default_magenta "
	RED = "color.default_red "
	WHITE = "color.default_white "
	YELLOW = "color.default_yellow "
	BOLD = "effect.A_BOLD "
	UNDERLINE = "effect.A_UNDERLINE"
	REVERSE = "effect.A_REVERSE"
	ENDC = "clr.ENDC"

# FUNCTIONS
def color_translation(string):
	# color translation
	string_list = []
	if string.find("color.") != -1:
		string_array = string.split("color.")
		for elem in string_array:
			if elem == '':
				continue
			if elem.find("effect.") != -1:
				effect = elem.split('effect.')[-1].split(' ')[0]
				elem = elem.replace('effect.%s '% effect, '')
			else:
				effect = 0
			elem_color = elem.split(' ')[0]
			elem = elem.replace(elem_color + ' ', '')
			elem_string = elem.split('clr.ENDC')[0]
			string_list.append((elem_string, elem_color, effect))
	else:
		string_list = [(string, "default_white", 0)]
	return string_list
def use_color(color):
		color_dict = {'default_black': curses.COLOR_BLACK, 'default_blue': curses.COLOR_BLUE, 'default_cyan': curses.COLOR_CYAN, 
					  'default_green': curses.COLOR_GREEN, 'default_magenta': curses.COLOR_MAGENTA, 'default_red': curses.COLOR_RED, 
					  'default_white': curses.COLOR_WHITE, 'default_yellow': curses.COLOR_YELLOW}
		try:
			return curses.color_pair(color_dict[color])
		except curses.ERR:
			pass
def extract_path(path):
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

def main(stdscr):
	standard_path = "/home/mr_robot/Desktop/Operations/test/BigBrother/modules/windows"
	console = console_window(stdscr, standard_path)		# - initializing 
	screen = screen_window(stdscr, console)				# - window objects
	screen.show_path()
	while (1):
		command = console.prompt()
		if command == 'q':
			sys.exit()

if __name__ == "__main__":
	curses.wrapper(main)