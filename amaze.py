import os
import sys
from itertools import chain


WALL = '#'
SPACE = ' '
PASSED = '.'
PLAYER = '@'
VALID_ACTIONS = ['W', 'S', 'A', 'D', 'Q']


def new_game(level):
    file_list = os.listdir("levels")
    levels = sorted(file_list, key=name_without_extension)
    # get the levels from the starting level onwards (not including the starting level)
    levels = levels[levels.index(level) + 1:]
    maze_array = get_maze_from_level(level)
    missing_spaces = get_missing_spaces(maze_array)
    current_position = get_current_position(maze_array)

    while True:
        print_headers(level, maze_array)
        current_position = move(current_position, maze_array, missing_spaces)
        if not missing_spaces:
            if not levels:
                break
            print_headers(level, maze_array)
            print("Press a key to go to the next level")
            getch()
            level = levels.pop(0)
            maze_array = get_maze_from_level(level)
            missing_spaces = get_missing_spaces(maze_array)
            current_position = get_current_position(maze_array)            

    os.system("clear")
    print_rules()
    print("----------")
    print_maze(maze_array)
    print("-------------------")
    print("Congratulations :-)")
    print("-------------------")
    getch()


def print_headers(level, maze_array):
    os.system("clear")
    print_rules()
    print("----------")
    print(f"Level {name_without_extension(level)}")
    print("----------")
    print_maze(maze_array)


def name_without_extension(filename):
    return int(filename.split(".")[0])


def get_maze_from_level(level):
    maze = []

    with open(f"levels/{level}") as f:
        content = f.readlines()

    maze_content = [x.strip().replace('.', ' ') for x in content]
    maze.extend(list(c) for c in maze_content)
    return maze


def get_missing_spaces(maze):
    missing_spaces = []

    for x, xvalue in enumerate(maze):
        for y, yvalue in enumerate(xvalue):
            if maze[x][y] == ' ':
                missing_spaces.append((x,y))
    
    return missing_spaces
        
def move(position, maze, missing_spaces):
    while True:
        action = getch().upper()

        if action in VALID_ACTIONS:
            return execute_action(action, position, maze, missing_spaces)


def execute_action(action, position, maze, missing_spaces):
    if action == 'Q':
        os.system("clear")
        sys.exit(0)

    if action == 'W':
        return go_up(position, maze, missing_spaces)

    if action == 'S':
        return go_down(position, maze, missing_spaces)

    if action == 'A':
        return go_left(position, maze, missing_spaces)

    if action == 'D':
        return go_right(position, maze, missing_spaces)


def can_move(x, y, maze):
    if x < 0 or y < 0 or x > len(maze) or y > len(maze[x]):
        return False

    return maze[x][y] != WALL


def go_up(position, maze, missing_spaces):
    x_position = position[0]
    y_position = position[1]

    while can_move(x_position - 1, y_position, maze):
        x_position = x_position - 1
        maze[x_position + 1][y_position] = PASSED
        maze[x_position][y_position] = PLAYER

        try:
            missing_spaces.remove((x_position, y_position))
        except ValueError:
            pass
    return x_position, y_position


def go_down(position, maze, missing_spaces):
    x_position = position[0]
    y_position = position[1]

    while can_move(x_position + 1, y_position, maze):
        x_position = x_position + 1
        maze[x_position - 1][y_position] = PASSED
        maze[x_position][y_position] = PLAYER

        try:
            missing_spaces.remove((x_position, y_position))
        except ValueError:
            pass
    return x_position, y_position


def go_left(position, maze, missing_spaces):
    x_position = position[0]
    y_position = position[1]

    while can_move(x_position, y_position - 1, maze):
        y_position = y_position - 1
        maze[x_position][y_position + 1] = PASSED
        maze[x_position][y_position] = PLAYER

        try:
            missing_spaces.remove((x_position, y_position))
        except ValueError:
            pass
    return x_position, y_position


def go_right(position, maze, missing_spaces):
    x_position = position[0]
    y_position = position[1]

    while can_move(x_position, y_position + 1, maze):
        y_position = y_position + 1
        maze[x_position][y_position - 1] = PASSED
        maze[x_position][y_position] = PLAYER

        try:
            missing_spaces.remove((x_position, y_position))
        except ValueError:
            pass
    return x_position, y_position


def print_maze(maze_array):
    for row in maze_array:
        print(*row)


def get_current_position(maze_array):
    for index, value in enumerate(maze_array):
        for another_index, another_value in enumerate(value):
            if another_value == PLAYER:
                return index, another_index


def print_rules():
    """ The rules of this simple game"""
    print("Move in straight lines. The goal is to pass through every spot")
    print("- use 'W' to move up")
    print("- use 'S' to move down")
    print("- use 'A' to move left")
    print("- use 'D' to move right")
    print("- use 'Q' to quit")
    print()


# trick to get only one character input from the user
# it works with Unix and Windows
class _Getch:
    """Gets a single character from standard input.  
       Does not echo to the screen."""
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


getch = _Getch()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Only one argument is valid, the level (<level_number>.txt for example)")
        exit()

    level = sys.argv[1] if len(sys.argv) == 2 else '1.txt'

    new_game(level)
