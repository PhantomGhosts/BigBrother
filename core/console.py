import curses, os.path, sys

# VARIABLES
standard_path = "/usr/share/BigBrother/"

# CLASSES
class console_window:
	# Defining a console_window class to
	# make a default console_window
	def __init__(self, scr):
		self.scr = scr
		Y, X = self.scr.getmaxyx()
		self.X, self.Y = X, Y
		curses.echo()
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i, i, -1)

	def show_path(self, path, **coordinates):
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
		try:
			self.scr.move(coordinates['Y'], coordinates['X'])
		except:
			pass
		self.scr.addstr("BBro", curses.A_UNDERLINE)
		self.scr.addstr(' ' + folders[0] + '[')
		self.scr.addstr(folders[-2], use_color('default_yellow') + curses.A_BOLD)
		self.scr.addstr('](')
		self.scr.addstr(folders[-1], use_color('default_red') + curses.A_BOLD)
		self.scr.addstr(') > ')
		self.scr.refresh()
class screen_window:
	def __init__(self, scr):
		self.scr = scr
		self.line = 0
		Y, X = self.scr.getmaxyx()
		self.X, self.Y = X-2, Y-2-1
		self.scr.clear()

	def erase_board(self):
		self.scr.move(1, 2)
		for x in range(50): self.scr.deleteln()
	def write_log(self, string):
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
		# writing
		self.scr.move(1, 2)
		for elem in string_list:
			self.scr.insertln()
			if elem[2] != 0:
				effectt = eval("curses.%s" % elem[2])
				self.scr.addstr(1, 2, elem[0], use_color(elem[1]) + effectt)
			else:
				self.scr.addstr(elem[0], use_color(elem[1]))
			self.line += 1
			self.scr.move(self.Y, 1)
			self.scr.clrtoeol()
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
def use_color(color):
		color_dict = {'default_black': curses.COLOR_BLACK, 'default_blue': curses.COLOR_BLUE, 'default_cyan': curses.COLOR_CYAN, 
					  'default_green': curses.COLOR_GREEN, 'default_magenta': curses.COLOR_MAGENTA, 'default_red': curses.COLOR_RED, 
					  'default_white': curses.COLOR_WHITE, 'default_yellow': curses.COLOR_YELLOW}
		try:
			return curses.color_pair(color_dict[color])
		except curses.ERR:
			pass


def main(stdscr):
	stdscr.clear()
	screen = screen_window(stdscr)
	screen.scr.scrollok(1)
	screen.scr.idlok(1)
	for x in range (0,45):
		screen.write_log("%s%s%s BigBrother %s%s" % (clrs.RED, clrs.BOLD, (screen.X-2-12)/2*'#', (screen.X-2-12)/2*'#', clrs.ENDC))
	screen.erase_board()
	console = console_window(stdscr)
	console.show_path(standard_path + "modules/windows/anagenesis/katascopos/keylogger/windows_api", Y=console.Y - 2, X=2)
	stdscr.getstr()


if __name__ == "__main__":
	curses.wrapper(main)