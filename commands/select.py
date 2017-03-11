from core import console
import curses

# GLOBAL VARS
stdscr = ''
stdpath = ''
# INIT FUNC
def __init__(scr, path):
	stdscr = scr
	stdpath = path
# LOW LEVEL FUNCTIONS
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
# SELECT
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
			stdscr.screen.addstr(folder, console.use_color('008') + curses.A_BOLD)
			# NORMALIZE END

	curses.curs_set(0)													# + hide cursor
	stdscr.screen.keypad(1)												# + allow keypad getchar
	curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_YELLOW)		# + init pair highlight
	highlight = curses.color_pair(20)									# + highlight effect
	normal = curses.A_NORMAL											# + normal effect
	position = 1														# + position to highlight
	max_row = stdscr.Y - 1												# + max row
	while (1):
		row_num = len(os.listdir(stdpath))								# + len of row
		if row_num < max_row:											# - if too many elements
			stdscr.console.write_log("ERROR.0001: Too many elements in thys folder to display it")
			break														# -
		stdscr.
	stdscr.screen.keypad(0)
	curses.curs_set(2)

			# NORMALIZE START
			# ADD REVERSE SELECT
			self.console.set_path()
			self.screen.refresh()
			self.console.refresh()
			try:
				self.console.path = os.path.join(self.console.path, folders[alphabet.index(self.console.scr.getkey())])
			except:
				pass

			# NORMALIZE END

			# NORMALIZE START
"""			from __future__ import division  #You don't need this in Python3
			import curses
			from math import *


			screen = curses.initscr()
			curses.noecho()
			curses.cbreak()
			curses.start_color()
			screen.keypad( 1 )
			curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
			highlightText = curses.color_pair( 1 )
			normalText = curses.A_NORMAL
			screen.border( 0 )
			curses.curs_set( 0 )
			max_row = 10 #max number of rows
			box = curses.newwin( max_row + 2, 64, 1, 1 )
			box.box()


			strings = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n" ] #list of strings
			row_num = len( strings )

			pages = int( ceil( row_num / max_row ) )
			position = 1
			page = 1
"""			for i in range( 1, max_row + 1 ):
			    if row_num == 0:
			        box.addstr( 1, 1, "There aren't strings", highlightText )
			    else:
			        if (i == position):
			            box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
			        else:
			            box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
			        if i == row_num:
			            break

			screen.refresh()
			box.refresh()

			x = screen.getch()
			while x != 27:
			    if x == curses.KEY_DOWN:
			        if page == 1:
			            if position < i:
			                position = position + 1
			            else:
			                if pages > 1:
			                    page = page + 1
			                    position = 1 + ( max_row * ( page - 1 ) )
			        elif page == pages:
			            if position < row_num:
			                position = position + 1
			        else:
			            if position < max_row + ( max_row * ( page - 1 ) ):
			                position = position + 1
			            else:
			                page = page + 1
			                position = 1 + ( max_row * ( page - 1 ) )
			    if x == curses.KEY_UP:
			        if page == 1:
			            if position > 1:
			                position = position - 1
			        else:
			            if position > ( 1 + ( max_row * ( page - 1 ) ) ):
			                position = position - 1
			            else:
			                page = page - 1
			                position = max_row + ( max_row * ( page - 1 ) )
			    if x == curses.KEY_LEFT:
			        if page > 1:
			            page = page - 1
			            position = 1 + ( max_row * ( page - 1 ) )

			    if x == curses.KEY_RIGHT:
			        if page < pages:
			            page = page + 1
			            position = ( 1 + ( max_row * ( page - 1 ) ) )
			    if x == ord( "\n" ) and row_num != 0:
			        screen.erase()
			        screen.border( 0 )
			        screen.addstr( 14, 3, "YOU HAVE PRESSED '" + strings[ position - 1 ] + "' ON POSITION " + str( position ) )

			    box.erase()
			    screen.border( 0 )
			    box.border( 0 )

			    for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
			        if row_num == 0:
			            box.addstr( 1, 1, "There aren't strings",  highlightText )
			        else:
			            if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
			                box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
			            else:
			                box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], normalText )
			            if i == row_num:
			                break



			    screen.refresh()
			    box.refresh()
			    x = screen.getch()

			curses.endwin()
			exit()
			# NORMALIZE END


# DEBUG
def debug(scr):
	cnsl = console.console_window(scr)
	screen = console.screen_window(scr, cnsl)
	__init__(screen, stdpath)


if __name__ == "__main__":
	curses.wrapper(debug)