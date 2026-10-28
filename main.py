"""
============= CYBERPUNK 2077 =============

------------ BREACH PROTOCOL -------------



This is the main module of the mini-game called 
"BREACH PROTOCOL" from Cyberpunk 2077


--------------------------------------------

The main goal of the game is:
    Complete as many Daemons (special code sequences) 
    as possible within player's buffer size by selecting 
    codes from the grid under specific movement rules. Completing 
    daemons gives rewards (eurodolars, quickhacks and components
                           of different rarity)

--------------------------------------------

The movement rules:
    1. All the uneven moves are horizontal
    2. All the even moves are vertical
    3. If player presses the element that is not the next one
       in one of the goals, bool_dict for that goal resets to False.
       However, is the same element is in another goal, it modifies
       bool_dict[current index] to True
    4. If player presses the same value but in a different position,
       it counts as a move, but does not reset succsessful picks
    5. If player presses the same value as the first one in a sequence
       but in a third or more position in an index_dict, the bool_dict 
       modifies to False, but the first element remains True
    
    Notes: player cannot choose the same position to change the direction
           of the cursor
           player can choose the same element as the previous one
           and it will not ruin the sequence

--------------------------------------------

To win or lose player must:
    1. Finish at least one sequence to win. The reward is determined
       by the difficulty of the sequence
    2. Spend all the atempts in vain to lose

    Note: if player finishes the sequence at the last attempt,
          player wins

--------------------------------------------

After player wins or loses, player gets a message about either reward
or about the defeat. Then player is directed to the menu where player
can choose whether to continue hacking or return to main meny
"""

import time as t
import sys
import breach_protocol as bp
import ascii_art

def init() -> None:
    """
    Initializes the main screen of the game
    """
    print('\033[?2J')
    print('\033[?25l')
    print('\033[u')
    bp.clear_terminal()
    count = 1
    while count <= 9:
        sys.stdout.write('\033[31m. \033[0m')
        sys.stdout.flush()
        t.sleep(0.5)

        if count % 3 == 0:
            bp.clear_terminal()
        count += 1

    count = 0
    while count <= 12:
        sys.stdout.write('\033[31m\x1B[3mmain.__init__\x1B[0m\033[0m')
        sys.stdout.flush()
        t.sleep(0.2)
        bp.clear_terminal()

        count += 1

    t.sleep(1)
    count = 0

    while count < 3:
        for _ in range(5):
            bp.clear_terminal()
            sys.stdout.write('\033[0;33m' + ascii_art.MAIN_LOGO + '\033[0m')
            sys.stdout.flush()
            t.sleep(0.1)
        t.sleep(0.5)
        count += 1

    t.sleep(1)
    bp.clear_terminal()

def init_game() -> None:
    """
    Initializes the game itself
    """
    print('\033[H')
    print("\033[s")
    goals = bp.generate_goals()
    paths = bp.generate_path_for_all_goals(goals)
    grid = bp.generate_grid(goals, paths)
    bp.write_grid_variations(grid)

    bp.register_movement(goals)

def rules() -> None:
    """
    Prints out the rules of the game
    """
    bp.clear_terminal()
    print('\033[H')
    for line in ascii_art.RULES:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            t.sleep(0.002)

    while True:
        try:
            key = bp.get_key()

        except UnicodeDecodeError:
            continue

        if key == '\r':
            return True

def credit() -> None:
    """
    Prints out the credits of the game
    """
    bp.clear_terminal()
    print('\033[H')
    for line in ascii_art.CREDITS:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            t.sleep(0.001)

    while True:
        try:
            key = bp.get_key()

        except UnicodeDecodeError:
            continue

        if key == '\r':
            return True

def menu(pathname: str = 'main_menu.txt') -> bool | int:
    """
    Initializes the main menu of the game

    Args:
        pathname str: Set to 'main_menu.txt' by default.
                      Does not change throughout the code, 
                      but can be changed if needed. Path to
                      the file with pictures of the main menu

    Returns:
        bool | int: True if player chooses to start a game
                    1 if player chooses to read rules
                    2 if player chooses to read credits
                    3 if player chooses to exit the game
    """
    bp.clear_terminal()
    index = 0

    with open(pathname, 'r', encoding='utf-8') as f:
        menu_list = f.read().split('\n\n')

    print('\033[u')
    print('\033[30m' + menu_list[index] + '\033[0m')

    while True:
        print('\033[u')
        try:
            key = bp.get_key()

        except UnicodeDecodeError:
            continue

        if key == 'w' and index > 0:
            index -= 1

        elif key == 's' and index < 3:
            index += 1

        elif key not in 'ws':
            pass

        if key == '\r':
            if index == 3:
                bp.clear_terminal()
                return 3

            if index == 1:
                bp.clear_terminal()
                return 1

            if index == 2:
                bp.clear_terminal()
                return 2

            if index == 0:
                return True

        print('\033[30m' + menu_list[index] + '\033[0m')



def end_game(pathname='resume_menu.txt') -> bool:
    """
    Initializes the menu after winning or losing
    the game

    Args:
        pathname str: Set to 'resume_menu.txt' by default.
                      Does not change throughout the code, 
                      but can be changed if needed. Path to
                      the file with pictures of the resume menu

    Returns:
        bool: True if player chooses to continue hacking
              False if player chooses to exit to the main menu
    """
    index = 0

    bp.clear_terminal()
    print('\033[u')

    with open(pathname, 'r', encoding='utf-8') as f:
        output_list = f.read().split('\n\n')

    print('\033[30m' + output_list[index] + '\033[0m')

    while True:
        try:
            key = bp.get_key()

        except UnicodeDecodeError:
            continue

        if key == 'w' and index == 1:
            index -= 1

        elif key == 's' and index == 0:
            index += 1

        elif key not in 'ws':
            pass

        if key == '\r':
            if index == 1:
                bp.clear_terminal()
                return False

            elif index == 0:
                return True

        print('\033[u')
        print('\033[30m' + output_list[index] + '\033[0m')

def main():
    """
    Main function of the game. Initializes the screen,
    the game itself and the menu

    Note: this is the main function, it does not return
          anything
    """
    init()
    while True:
        menu_return = menu()
        if menu_return is True:
            init_game()
        elif menu_return == 1:
            if rules() is True:
                continue
        elif menu_return == 2:
            if credit() is True:
                continue
        elif menu_return == 3:

            for _ in range(10):
                bp.clear_terminal()
                sys.stdout.write('\033[0;33m' + ascii_art.ENDING + '\033[0m')
                sys.stdout.flush()
                t.sleep(0.05)
            bp.clear_terminal()
            print('\033[31m\x1B[3mThanks for playing! Hope you enjoyed it!\x1B[0m\033[0m')
            print('\033[30m' + ascii_art.REBECCA + '\033[0m')
            break

        while end_game() is True:
            init_game()


if __name__ == '__main__':
    main()
