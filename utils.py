import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def getchar():
    return getch_win() if os.name == 'nt' else getch_unix()

def getch_unix():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def getch_win():
    import msvcrt
    return msvcrt.getch().decode()
