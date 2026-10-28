"""
This module provides user with all the functions that are needed
to initialize the game

It includes functions for:
    0. Getting info about pressed keys and clearing the terminal
       accordingly to platform player uses

    1. Generating the grid, goals and paths for the goals 
    2. Creating files with different variations of the grid
       and sequence
    3. Moving through the matrix
    4. Getting an element player chose
    5. Checking if the chosen element represent the sequence
       that was generated
    6. Checking if player has won
    7. Printing the current state of the game
    8. Registering player's moves
"""

from random import sample, randint, choice
import sys
import os
import ascii_art

MATRIX_ELEMENTS = ['BD', '1C', '55', 'E9', '7A']

# Creates functions accordingly to the platform player uses
if sys.platform.startswith('win'):
    import msvcrt
    def get_key():
        """
        Reads and returns what key is pressed
        without the need to press enter to register
        key press
        """
        return msvcrt.getch().decode()

    def clear_terminal():
        """
        Inserts command in a terminal to clear it
        """
        return os.system('cls')

else:
    import termios
    import tty

    def get_key():
        """
        Reads and returns what key is pressed
        without the need to press enter to register
        key press
        """
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def clear_terminal():
        """
        Inserts command in a terminal to clear it
        """
        return os.system('clear')

def generate_goals() -> dict[int: list[str]]:
    """
    Generates dictionary with keys from 1 to 3 where 1 is the
    the lowest level of difficulty with 3 elements to 
    collect, 2 is the medium level of difficulty with either
    3 or 4 elements to collect, and 3 is the highest level
    of difficulty with 4 elements to collect

    Returns:
        dict[int: list[str]]: A dictionary with three goals to
                              meet
    """
    goal_dict = {}

    for i in range(1, 4):
        needed_elements = 3
        if i == 2:
            needed_elements = randint(3, 4)

        if i > 2:
            needed_elements = 4

        goal_dict[i] = sample(MATRIX_ELEMENTS, needed_elements)

    return goal_dict


def generate_path_for_goal(goal: list[str]) -> list[tuple[int]]:
    """
    Generates list of tuples with coordinates for one goal
    that are connected. If step is uneven, changes the row
    for next element, if step is even changes the column
    for next element

    Args:
        goal: list[str]: One of the goals we process
                        to get path coordinates

    Returns:
        list[tuple[int, int]]: A list of tuples of coordinates
                               for given elements in a goal
    """
    path = []

    row = 0
    column = randint(0, 5)
    path.append((row, column))

    for step in range(1, len(goal)):
        if step % 2 == 1:
            row = randint(1, 5)

        else:
            column = randint(1, 5)

        path.append((row, column))

    return path

def generate_path_for_all_goals(goals: dict[int: list[str]]) -> \
                                dict[int: list[tuple[int, int]]]:
    """
    Generates a dictionary where keys are either 1, 2, 3 according
    to the difficulty of a goal, and values are lists of paths
    generated for given dictionary of goals

    Args:
        goals dict[int: list[str]]: A dictionary of goals where
                                    key: level of difficulty (1, 2, 3)
                                    value: a goal to meet

    Returns:
        dict[int: list[tuple[int, int]]]: A dictionary of paths where
                                          key: level of difficulty (1, 2, 3)
                                          value: a path for a goal
    """
    paths_dict = {}
    for k, v in goals.items():
        paths_dict[k] = generate_path_for_goal(v)

    return paths_dict



def generate_grid(goals: dict[int: list[str]], paths: dict[int: list[tuple[int, int]]]) -> \
                  list[list[str]]:
    """
    Generates grid based on the paths we created for the goal. Takes
    paths and fills empty grid with elements from goals, taking into
    an account the path we generated for the goal. Then randomly fills
    the rest of the grid with elements from MATRIX_ELEMENTS

    Args:
        goals dict[int: list[str]]: A dictionary of goals where
                                    key: level of difficulty (1, 2, 3)
                                    value: a goal to meet
        paths dict[int: list[tuple[int, int]]]: A dictionary of paths where
                                          key: level of difficulty (1, 2, 3)
                                          value: a path for a goal

    Returns:
        list[list[str]]: A list of rows in a matrix filled with elements from
                         MATRIX_ELEMENTS
    """
    grid = [[' ' for _ in range(6)] for _ in range(6)]

    for i in range(1, 4):
        for (row, column), value in zip(paths[i], goals[i]):
            grid[row][column] = value


    for row in range(6):
        for column in range(6):
            if grid[row][column] == ' ':
                grid[row][column] = choice(MATRIX_ELEMENTS)

    return grid

def write_grid_variations(grid: list[list[str]], pathname='grid_variations.txt') -> None:
    """
    Creates a file with 36 matrix where each new element is highlighted
    in blue

    Args:
        grid list[list[str]]: A list of rows in a matrix filled with elements from
                              MATRIX_ELEMENTS
        pathname str: Set to 'grid_variations.txt' by default. Does not change throughout
                      the code, but can be changed if needed. Path to the file that we
                      want to write our matrix variations in

    Note: this function does not return anything, it creates a file with pathname as
          file name
    """
    rows = len(grid)
    columns = len(grid[0])

    with open(pathname, 'w', encoding='utf-8') as f:
        for row in range(rows):
            for column in range(columns):
                variation = [[f'\033[0;33m{el}\033[0m' for el in line] for line in grid]
                variation[row][column] = f'\033[0;36m{grid[row][column]}\033[0m'

                for line in variation:
                    f.write(' | '.join(line) + ' \n')

                f.write('\n')

def move(key: str, count_move: int, pos=(0, 0)) -> tuple[int, int]:
    """
    Register the change in player's position. If count_move is even,
    player can only move horizontally. If count_move is uneven, player 
    can only move vertically. Checks if player has reached the border
    of matrix. If yes, does not let player move and does not count it
    as a step

    Args:
        key str: Value of a key that is pressed
        count_move int: Count whether player should move vertically or
                        horizontally
        pos tuple[int, int]: Current position of player. (0, 0) by\
                             by default
    
    Returns:
        tuple[int, int]: New position of player
    """
    row, column = pos

    if count_move % 2 != 0:
        if key == 'w' and row > 0:
            row -= 1
        elif key == 's' and row < 5:
            row += 1

    else:
        if key == 'a' and column > 0:
            column -= 1
        elif key == 'd' and column < 5:
            column += 1

    return row, column

def get_current_grid(pos: tuple[int, int], pathname='grid_variations.txt') -> str:
    """
    Reads file with all the variations of current grid and finds matrix
    that has given pos that is highlighted

    Args:
        pos tuple[int, int]: A position we want to check for
        pathname str: Set to 'grid_variations.txt' by default. Does not change throughout
                      the code, but can be changed if needed. Path to the file with
                      all the variations of our matrix
    
    Returns:
        str: A grid with given position as highlighted
    """
    x, y = pos

    with open(pathname, 'r', encoding='utf-8') as f:
        grids = [grid.strip() for grid in f.read().split('\n\n') if grid.strip()]
        for grid in grids:
            rows = grid.split('\n')

            for count, columns in enumerate(rows):
                has_cell = False
                columns = columns.split('|')
                for index, cell in enumerate(columns):
                    cell = cell.strip()
                    if index == y and cell.startswith('\x1b[0;36m'):
                        has_cell = True
                        break

                if count == x and has_cell is True:
                    return grid

def write_sequence_variations(goals: dict[int: list[str]], pathname='sequence_variations.txt'):
    """
    Creates a file with either 13 or 14 lines where each subsequent element 
    is highlighted together with the previous one

    Args:
        goals dict[int: list[str]]: A dictionary of goals where
                                    key: level of difficulty (1, 2, 3)
                                    value: a goal to meet
        pathname str: Set to 'sequence_variations.txt' by default. Does not change throughout
                      the code, but can be changed if needed. Path to the file with
                      all the variations of our sequences

    Note: this function does not return anything, but creates a file
          with all the needed variations of our sequences
    """
    with open(pathname, 'w', encoding='utf-8') as f:
        for v in goals.values():
            for n in range(0, len(v) + 1):
                colored = []
                for i, el in enumerate(v):
                    if i < n:
                        colored.append(f'\x1b[0;36m{el}\x1b[0m')
                    else:
                        colored.append(f'\x1b[0;33m{el}\x1b[0m')

                f.write(' | '.join(colored) + '\n')

            f.write('\n')


def get_element(grid: str, pos: tuple[int, int]) -> str:
    """
    Returns an element that we entered from a grid

    Args:
        grid str: Current grid with highlighted position
        pos tuple[int, int]: Current position of player

    Returns:
        str: An element that we chose from the grid
    """
    row, column = pos
    el = grid.split('\n')[row].split(' | ')[column]

    return el

def get_check(goals: dict[int: list[str]], el: str = None, \
              bool_dict: dict[int: list[bool]] = None, index_dict: dict[int: int] = None):
    """
    Takes a chosen elements and checks if he is in one of
    the goals. If yes, modifies bool_dict and index_dict
    so we remember what position we already filled in a goal

    Rules:
        1. If player presses the element that is not the next one
           in one of the goals, bool_dict for that goal resets to False.
           However, is the same element is in another goal, it modifies
           bool_dict[current index] to True
        2. If player presses the same value but in a different position,
           it counts as a move, but does not reset succsessful picks
        3. If player presses the same value as the first one in a sequence
           but in a third or more position in an index_dict, the bool_dict 
           modifies to False, but the first element remains True

    Args:
        goals dict[int: list[str]]: A dictionary of goals where
                                    key: level of difficulty (1, 2, 3)
                                    value: a goal to meet
        el str: An element we choose from the grid. Set to None by default
        bool_dict dict[int: list[bool]]: A dictionary of bool statements that
                                         we use for checking whether player 
                                         succsessfully chose an element or not
                                         key: level of difficulty (1, 2, 3)
                                         value: list of bools that check
                                                whether player chose the right
                                                element or not
                                         Set to None by default
        index_dict dict[int: int]: A dictionary of indexes that we use to remember
                                   the index of an element in a sequence that we
                                   are one
                                   key: level of difficulty (1, 2, 3)
                                   value: an index of an element player is currently
                                          choosing if previous choices were correct
                                   Set to None by default
    
    Returns:
        bool_dict dict[int: list[bool]]: To remember if player chose correctly
        index_dict dict[int: int]: To remember what index of an element player is 
                                   currently guessing
    """
    if el:
        el = el[7:]
        el = el[:2]

    if not bool_dict:
        bool_dict = {}
    if not index_dict:
        index_dict = {}

    for k, v in goals.items():
        if k not in bool_dict:
            bool_dict[k] = [False for _ in v]
            index_dict[k] = 0

        current_index = index_dict[k]

        previous_index = current_index - 1
        first_el = goals[k][0]

        if el == v[current_index]:
            bool_dict[k][current_index] = True
            index_dict[k] += 1

        elif el == v[previous_index]:
            pass

        elif el == first_el:
            bool_dict[k] = [False for _ in v]
            index_dict[k] = 1
            bool_dict[k][0] = True

        elif el:
            bool_dict[k] = [False for _ in v]
            index_dict[k] = 0

    return bool_dict, index_dict

def get_current_sequence(bool_dict: dict[int: list[bool]] = None,\
                         pathname: str ='sequence_variations.txt') -> str:
    """
    Reads file with all the variations of current sequence and finds lines
    that represent current state of bool_dict, where True is highlighted in
    blue and False is highlighted in Yellow

    Args:
        bool_dict dict[int: list[bool]]: A dictionary of bool statements that
                                         we use for checking whether player 
                                         succsessfully chose an element or not
                                         key: level of difficulty (1, 2, 3)
                                         value: list of bools that check
                                                whether player chose the right
                                                element or not
                                         Set to None by default
        pathname str: Set to 'sequence_variations.txt' by default. Does not change throughout
                      the code, but can be changed if needed. Path to the file with
                      all the variations of our sequences
    
    Returns:
        str: Current sequences that represent bool_dict
    """
    with open(pathname, 'r', encoding='utf-8') as f:
        sections = f.read().strip().split('\n\n')

    output_list = [None for _ in sections]

    for index, section in enumerate(sections):
        rows = section.split('\n')
        for row in rows:
            elements = [el.strip() for el in row.split(' | ')]

            match = True
            for el, check in zip(elements, bool_dict[index + 1]):
                if check and not el.startswith('\x1b[0;36m'):
                    match = False
                    break
                if not check and not el.startswith('\x1b[0;33m'):
                    match = False
                    break

            if match:
                output_list[index] = row
                break



    return '\n'.join(output_list)


def check_for_victory(bool_dict: dict[int: list[bool]], count_attempts: int) -> bool:
    """
    Checks if player has won or not
    
    Rules:
        1. Player wins if completes one of the sequences
        2. Player loses if exceeds the number of given attempts

    Args:
        bool_dict dict[int: list[bool]]: A dictionary of bool statements that
                                         we use for checking whether player 
                                         succsessfully chose an element or not
                                         key: level of difficulty (1, 2, 3)
                                         value: list of bools that check
                                                whether player chose the right
                                                element or not
        count_attempts int: The amount of attempts that player can make

    Returns:
        bool: True if player won
              False if player loses
    """
    for k in bool_dict:
        if all(bool_dict[k]):
            clear_terminal()
            print('\033[H')
            if k == 3:
                print('\033[30m' + ascii_art.REWARD_HIGH + '\033[0m')
            elif k == 2:
                print('\033[30m' + ascii_art.REWARD_MEDIUM + '\033[0m')
            elif k == 1:
                print('\033[30m' + ascii_art.REWARD_LOW + '\033[0m')

            print('\033[30m' + ascii_art.PROCEEDE_MENU + '\033[0m')

            while True:
                try:
                    key = get_key()
                except UnicodeDecodeError:
                    pass

                if key == '\r':
                    return True


    if count_attempts == 0:
        clear_terminal()
        print('\033[H')
        print('\033[30m' + ascii_art.LOST_MENU + '\033[0m')
        while True:
            key = get_key()

            if key == '\r':
                return True

    return False

def print_game_state(current_sequence: str, current_grid: str, count_attempts: int) -> None:
    """
    Prints the field in the current state

    Args:
        current_sequence str: Current sequence that represents bool_dict
        current_grid str: Current grid that represents the position player
                          is at
        count_attempts int: The amount of attempts that player can make

    Note: this function does not return anything, but prints the current state
          of field
    """
    grid_list = list(current_grid.splitlines())
    print_list = []
    current_sequence = current_sequence.split('\n')
    for index, el in enumerate(current_sequence):

        append_str = grid_list[index] + '\t  ' + el
        print_list.append(append_str)

    for index in range(3, 6):
        print_list.append(grid_list[index])

    print_grid = '\n'.join(print_list)
    print_grid = '\n'.join('\t\t' + line for line in print_grid.splitlines())
    print('\033[H', end='')
    print('\033[33m' + '\t' + ascii_art.MAIN_LOGO_RAW + '\033[0m', end='')
    print('\033[30m     ___________________________________________\
__________________________\033[0m', end='\n\n')
    print(ascii_art.COUNT_ATEMPTS + '  ' + f'{count_attempts}', end='\n\n')
    print(print_grid, end='\n\n')
    print('\033[30m     ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞\
 ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ \033[0m')


def register_movement(goals: dict[int: list[str]]) -> None:
    """
    Main function of this module. Registers pressed keys and changes
    the game state accordingly to the move

    Args:
        goals dict[int: list[str]]: A dictionary of goals where
                                    key: level of difficulty (1, 2, 3)
                                    value: a goal to meet

    Note: this function does not return anything, it just registers pressed keys
          and changes the game state accordingly to the move
    """
    pos = (0, 0)
    count_move = 0
    last_pos = None
    count_attempts = 5

    current_grid = get_current_grid(pos=pos)
    write_sequence_variations(goals)
    bool_dict, index_dict = get_check(goals)
    current_sequence = get_current_sequence(bool_dict=bool_dict)

    clear_terminal()
    print_game_state(current_sequence, current_grid, count_attempts)

    while True:
        if check_for_victory(bool_dict, count_attempts):
            clear_terminal()
            break

        try:
            key = get_key()
        except UnicodeDecodeError:
            continue

        if key not in ('w', 'a', 's', 'd', 'q', '\r', '\n'):
            continue

        if key == '\r':
            el = get_element(current_grid, pos)

            # Checks if new position is not the same as previous one
            # therefore counts a move and reduces the number of attempts
            if pos != last_pos:
                count_attempts -= 1
                count_move += 1
                last_pos = pos

            bool_dict, index_dict = get_check(goals, el=el, bool_dict=bool_dict, \
                                              index_dict=index_dict)
            current_sequence = get_current_sequence(bool_dict=bool_dict)

            current_grid = get_current_grid(pos=pos)
            print_game_state(current_sequence, current_grid, count_attempts)

        if key == 'q':
            clear_terminal()
            break

        if key in 'wasd':
            pos = move(key, count_move, pos)
            current_grid = get_current_grid(pos=pos)
            print_game_state(current_sequence, current_grid, count_attempts)
