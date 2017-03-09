from core import console
import curses

# GLOBAL VARS
stdscr = ''
stdpath = ''
# INIT FUNC
def __init__(scr, path):
	stdscr = scr
	stdpath = path
# SELECT
def back():
	stdscr.console.path = stdscr.console.path.split("modules/")[-1]
def select():
	stdscr.sign_border('select', console.clrs.BLUE)
	while len(console.extract_path(stdscr.console.path)) != 5:
		stdscr.erase_board()
		folders = os.listdir(stdscr.console.path)
		if len(folders) < 1:
			stdscr.write_log("Directory empty")
			sleep(1)
			stdscr.write_log("Back in 1 sec", 'process')
			sleep(1)
			back()
		else:

			# NORMALIZE START
			for n, folder in enumerate(folders):
				if n < stdscr.X - 1:
					stdscr.screen.move(n+1, 3)
				elif n < 2(stdscr.X - 1) and 28 < stdscr.Y:
					stdscr.screen.move(n+1, 18)
				else:
					curses.endwin()
					raise Exception
				self.screen.addstr(folder, console.use_color('008') + curses.A_BOLD)
			# ADD REVERSE SELECT
			self.console.set_path()
			self.screen.refresh()
			self.console.refresh()
			try:
				self.console.path = os.path.join(self.console.path, folders[alphabet.index(self.console.scr.getkey())])
			except:
				pass
			# NORMALIZE END


# DEBUG
def debug(scr):
	cnsl = console.console_window(scr)
	screen = console.screen_window(scr, cnsl)
	__init__(screen, stdpath)


if __name__ == "__main__":
	curses.wrapper(debug)