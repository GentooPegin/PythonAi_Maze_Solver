# Maze Learning AI

A small maze-solving AI built from scratch in Python using Q-learning and Tkinter.

## What it does

Maze Learning AI lets you create your own maze and train an AI to find the exit.

You can:

* Choose the maze size from 3×3 to 20×20
* Place a starting position
* Place walls
* Place an exit
* Erase placed elements
* Choose how many training runs the AI performs
* See the final path the AI learned

# How the AI works

The AI uses Q-learning.

It has a Q-table that stores how useful each possible movement is from each position.

The AI receives rewards and penalties:

* Reaching the exit: +300
* Normal movement: -1
* Hitting a wall: -5
* Moving outside the maze: -10

Through repeated training runs, the AI updates its Q-table and learns which movements lead toward the exit.

# Running the program

# Using the `.exe`

No Python installation is required.

Run:

`maze_ui.exe`

from the `dist` folder.

# Running from Python

If you have Python installed, run:

`python maze_ui.py`

# Controls

- Place Start

Select this mode and click a square to place the AI's starting position.

- Place Walls

Select this mode and click squares to create walls.

- Place Goal

Select this mode and click a square to place the exit.

- Erase

Select this mode and click a square to remove a wall, start position, or exit.

- Maze Size

Choose a maze size between 3×3 and 20×20, then click "Apply Size".

Changing the maze size clears the current maze.

- Training Runs

Choose how many times the AI should train. (Doesnt need confimration, the number currently in the field will be used)

More training runs generally give the AI more opportunity to learn the maze.

# Finalize Maze

Builds the maze and starts AI training.

While training, the interface is disabled and the current training progress is displayed.

#Confirm

After training is complete, the AI's final learned path is displayed in orange.

Click "Confirm" to clear the displayed path and create another maze.

# Project Files

* `Main.py` — older version of the Ai running in a console in a static maze
* `maze_ui.py` — graphical user interface and maze creation
* `ai.py` — Q-learning algorithm and AI logic
* `disc\maze_ui.exe` — standalone Windows executable

NO PYTHON INSTALLATION REQUIERD FOR CURRENT version

Mladen Bukara
