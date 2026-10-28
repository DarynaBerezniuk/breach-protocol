
<h1 align="center">Breach protocol</h1>
<p align="center"><i>Basics of Programming project</i></p>
<div align="center">
  <a href="">Daryna Berezniuk</a>




       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⡔⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        
    ⠀⠀⠀    ⠀⠀⠀⠀⠀⠀⢀⡠⢚⣉⣠⡽⠂⠀⠀⠀⠀⡰⢋⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢴⡆⠀     
       ⠀⠀⠀⠀⠀⢀⡤⠐⢊⣥⠶⠛⠁⢀⠄⡆⣠⠤⣤⠞⢠⠿⢥⡤⠀⠀⠠⢤⠀⠀⠀⠤⠤⠤⡄⢠⠤⠄⠤⠀⠀⠀⠒⣆⡜⣿⣄⠀⡤⢤⠖⣠⣀⠤⢒⣭⠶⠛⠃⠀⠀     
       ⢀⣀⡠⢴⣎⣥⣴⣾⣟⡓⠒⠒⠒⠺⣄⡋⢀⡾⢃⣴⢖⣢⣞⢁⣋⣉⣹⠏⠚⠛⢛⣉⣤⡴⢞⠃⣰⠾⠟⣛⣩⢵⢶⡟⣰⠇⠘⡼⢡⡟⣀⡋⢵⡞⠋⠁⠀⠀⠀   ⠀⠀  
       ⠈⠢⠄⠤⠤⠤⠤⠤⠴⠤⠴⠶⠶⢾⠟⣱⡿⢤⢿⣕⠾⣿⣿⣩⡭⢤⠞⣰⠶⢤⣀⡉⠓⢾⡍⣠⠴⠾⠛⠹⠡⣟⡁⢰⢏⣼⡇⢰⣿⢀⠟⠳⣤⣌⣦⡀⠀⠀⠀⠀      
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⢃⡼⠋⠛⠾⠚⠁⠀⠈⠉⠀⠀⠸⣄⠏⠀⠀⠈⠙⠓⡟⣰⠏⠀⠀⠀⠘⠾⠛⠳⠞⠉⠁⠙⠋⠙⠚⠀⠀⠀⠙⠛⢿⣷⣤⣀       
    ⠀⠀⠀    ⠀⠀⠀⠀⠀⠀⠀⢀⣜⡵⠟⠀⠀⠀⠀⠀⠀⣼⣿⣾⣿⣽⣽⣿⣿⢏⢫⣻⡹⡽⣰⢏⣯⠍⡭⡍⣭⢩⡭⢩⡍⡏⡏⣯⡍⣍⠙⡭⢹⣄⣤⠄⢠⠉⠓⢿⣕⡄    
    ⠀⠀⠀⠀⠀⠀⠀    ⠀⠀⠠⣯⠃⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣽⣾⣾⣟⣯⣣⣱⣾⣟⣞⣸⣇⣳⣃⣿⣛⣷⣬⠧⠳⠇⠿⢧⢿⢀⣷⢸⠧⢾⢃⠇⠀⠀⠀⠀⠁    

</div>  

---


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Documentation](#documentation)
- [Software](#software)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

---

## Overview

Breach protocol is a recreation of the hacking mini-game from *Cyberpunk 2077*. The goal is to hack an enemy system or an access point in order to gain bonuses, weaken opponents, and earn resources.

The player picks codes from a matrix under specific movement rules, trying to complete at least one target sequence (a "daemon") within a limited number of moves. The reward depends on the difficulty of the completed sequence.

## Features

- **Animated start-up sequence** with a flickering logo of the original game (built with the `sys` and `time` libraries).
- **Main menu** with four options: Start Game, Rules, Credits, Exit Game. Navigate with `w` / `s` and confirm with `Enter`.
- **Matrix and target sequences** generated for every round, with the remaining moves shown in the top-left corner and the sequences to collect shown to the right of the matrix.
- **Live highlighting**: codes that belong to a target sequence are highlighted in blue as they are selected.
- **Tiered rewards** (Low, Medium, High security) with eurodollars, components, and quickhacks.
- **Defeat screen** ("MILITECH NETSEC RESPONSE") when all moves are spent without completing a sequence.
- **Pause / resume menu** after each round: continue hacking or return to the main menu.
- **In-game rules** that are typed out dynamically on screen.
- **Credits screen** and a farewell message with ASCII art on exit.
- **Cross-platform input**: the game detects the player's platform and defines `get_key()` and `clear_terminal()` accordingly.

## Repository Structure

```
.
├── main.py                  # Entry point: start-up screen, menus, game loop
├── breach_protocol.py       # Game logic library
├── ascii_art.py             # ASCII art, rules text, credits, logos
├── main_menu.txt            # Frames of the main menu (one per selected button)
├── resume_menu.txt          # Frames of the pause / resume menu
├── grid_variations.txt      # Grid frames used for rendering
└── sequence_variations.txt  # Sequence frames with progressive highlighting
 
```

## Documentation

### Rules

**Movement**

- The first selection can be any code in the top row of the matrix.
- After that, the direction alternates automatically: one move is chosen from the same column as the previous one, the next from the same row, and so on.
- The player cannot move outside the boundaries of the matrix.
- The player cannot press the same element twice in order to change the direction of the cursor. In that case, the number of moves does not change.
- The player may choose another element with the same symbol as the next one without losing the selected elements of a sequence, but this costs 1 move.
- The keyboard layout must be set to **English** for movement to work.

**Sequence tracking**

- When the player selects an element that belongs to one of the target sequences, it is highlighted in blue.
- If the first element of a sequence is selected correctly but the next one is wrong, the progress for that sequence is reset.
- If the first element of a sequence is selected as the third (or later) element, the previously selected symbols of that sequence are reset, but the last selected element is counted as the new first element and highlighted in blue.

**Winning and losing**

- The player has **5 moves** to complete one of the sequences.
- A sequence counts as uploaded if it appears as a **contiguous substring** of the buffer.
- If a sequence is completed on the last move (moves reach 0), the player still wins.
- If all moves are spent without completing a sequence, the player loses.
- The reward depends on the difficulty of the completed sequence.
## Software

The game is written in **Python** and split into three modules:

- **`main.py`** initializes the start-up screen, the game itself, and the menus, using functions from `breach_protocol.py`.
- **`breach_protocol.py`** is a library of functions that implement the game: goal and path generation, grid generation, move registration, sequence checking, and the cross-platform `get_key()` and `clear_terminal()` helpers.
- **`ascii_art.py`** contains the variables holding the artwork and text used in the game.

### Implementation notes

- **Sequence checking.** Checking whether the selected elements match a target sequence was the biggest challenge. It is solved with dictionaries that track which elements of each sequence have been selected correctly.
- **Highlighting.** The highlighted sequence is represented by a dictionary showing which elements were selected correctly, so progress can be rendered in blue.
- **Matrix generation.** The matrix is built so that it contains all the paths between the elements of the target sequences.
- **Menus.** The menu images are stored in text files (`main_menu.txt`, `resume_menu.txt`), split into frames, and the frame matching the selected button is printed.
- **Cross-platform support.** The `msvcrt` library, originally used to detect key presses, did not work on the testing platform. The game now checks the platform and defines `get_key()` and `clear_terminal()` accordingly, so keys can be read in real time on any supported system.

## Theoretical improvements
This project is not in development anymore, but maybe in the future I decide to upgrade it to another level. Here are small improvements I wanted to make in the first place, but didn't get to do it:
- Emphasis on current available row/column for moving with different color;
- Musical accompaniment;
- Different text color for different terminals;
- Tutorial stage and controls explanation before user can access the game;
- Proper ASCII art for MacOS;
- Advanced matrix generator.

## Usage

**Requirements**

- Python 3.10 or newer
- A terminal with ANSI escape code support
- English keyboard layout

**Run**

```bash
python main.py
```

Run the command from the project directory so the `.txt` menu files can be found.

**Controls**

| Key | Action |
|---|---|
| `w` / `s` | Move between menu buttons / move the cursor |
| `Enter` | Confirm the selected option |
| `q` | Open or close the pause menu during a game |

## Acknowledgments

Working on this game was truly meaningful to me, as I am a big fan of *Cyberpunk 2077*. The game may not be complex, but I am proud of what I have made.

Some ASCII art taken from this [website](https://emojicombos.com/cyberpunk-2077-ascii-art). The underlying artwork and characters are CD PROJEKT RED. The menus, reward screens, rules and credits frames were created by me.

If you are the original author of any of this art and would like it credited or removed, please open an issue.

*Breach protocol* is a fan project inspired by the mini-game from *Cyberpunk 2077* by CD PROJEKT RED. It is not affiliated with or endorsed by CD PROJEKT RED.