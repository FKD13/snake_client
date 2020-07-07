import curses
import connection
import threading

# Init curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.nodelay(True)


class State:
    def __init__(self):
        self.do_update = False,
        self.data = None


def update(data):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(0, 0, f"{curses.LINES},{curses.COLS} Players: {len(data['snakes'])}")
    for i in data['apples']:
        if 1 < i[1]+1 < curses.LINES-1 and 1 < i[0]+1 < curses.COLS-1:
            stdscr.addstr(i[1]+1, i[0]+1, "A")
    for snake in data['snakes']:
        for i in snake['snake']:
            if 0 < i[1]+1 < curses.LINES-1 and 0 < i[0]+1 < curses.COLS-1:
                stdscr.addstr(i[1]+1, i[0]+1, "S")
    stdscr.refresh()


c = connection.Connection()
state = State()

t = threading.Thread(target=c.receive, args=[state])
t.start()

while True:
    char = stdscr.getch()
    if char == ord('\n'):
        break
    elif char == ord('z'):
        c.send('N\n')
    elif char == ord('d'):
        c.send('E\n')
    elif char == ord('s'):
        c.send('S\n')
    elif char == ord('q'):
        c.send('W\n')
    if state.do_update:
        if state.data is not None:
            update(state.data)
            state.do_update = False

stdscr.clear()
stdscr.addstr(0, 0, "Disconnecting...")
stdscr.refresh()

c.running = False
t.join()

# Stop curses
curses.echo()
curses.nocbreak()
stdscr.nodelay(False)
curses.curs_set(1)
curses.endwin()
