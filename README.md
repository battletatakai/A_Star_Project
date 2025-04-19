# Description
A GUI implementation of Sudoku that comes with Backtracking and A* algorithms for solving the puzzle. Comes with a GUI application and a program used to evaluate and compare Backtracking to A*. Built for CPSC 481 Artifical Intelligence course project at California State University, Fullerton. Based on Sudoku Solver by Dhruv Panchal.

# Team Members
* Julian Matuszewski
* Harrison Battle
* George Hanna
* Ethan Jin

# Installation and Setup

## Requirements
- Python 3.x
- Pygame library for GUI program

## How to Install
1. Download this repository to your computer
2. Make sure Python is installed on your system
3. Install the required package by running:
```  
pip install -r requirements.txt  
```

## Running Sudoku using the GUI (requires Pygame)
```
python SudokuGUI.py
```
* Press 'SPACE' to solve the Sudoku board using the A* algorithm
* Press 'G' to solve the Sudoku board using the traditional Backtracking Algorithm
* Press 'R' to reset the Board to a random puzzle
* Press 'ESC' to close the program

## Running the Evaluation Program
* Before running, set up desired parameters in the source file:
```
DIFFICULTY_RANGE = range(1, 65)
NUM_PUZZLES = 10
NUM_BEST_OF = 3
```
* Run the application:
```
python evaluation.py
```

# Layout

## Files

- **SudokuGUI.py**: The main program file containing the game interface and visualization
- **astar.py**: Helper functions for the A\* algorithm
- **sudokutools.py**: Helper functions for Sudoku puzzle generation and validation
- **evaluation.py**: Tools for evaluating algorithm performance
- **requirements.txt**: List of required Python packages

## Components

### SudokuGUI.py

#### visualSolve function
* Called on the Sudoku board to find the solution using the Backtracking implementation
* Has a built-in time delay so that it can be visualized

#### visualSolve_A function
* Called on the Sudoku board to find the solution using our A* implementation
* Has a built-in time delay so that it can be visualized

#### Board Class
* Stores state of the Board and functions for modifying state
* Contains rendering and gameplay logic using Pygame
* Handles rendering help panel
* Backtracking and A* functions are defined here for visual solving

#### Tile Class
* Stores state of a single Sudoku tile
* Has functions for modifying tiles and rendering using Pygame

#### main function
* Pygame initialization and Board Class initialization
* Variables used for handling Program logic
* Main game loop used for handling user input, updating render state, and checking if puzzle is solved

### sudokutools.py

#### find_empty function
* Locates the first empty cell (value 0) in the sudoku board
* Returns the position as a tuple of (row, column) or None if no empty cells exist

#### valid function
* Validates if a number can be placed in a specific position on the board
* Checks row, column, and 3×3 box constraints for the number

#### solve_A function
* A* algorithm implementation for solving Sudoku puzzles with no time delay (realtime performance)
* Uses a heap-based priority queue to select cells with the fewest candidates

#### solve function
* Backtracking algorithm implementation for solving Sudoku puzzles with no time delay (realtime performance)
* Recursively tries valid numbers in empty cells until solution is found

#### generate_board function
* Creates a random, valid Sudoku puzzle
* Fills diagonal boxes first, then uses backtracking to fill the rest
* Removes a specified number of cells to create the puzzle

### astar.py

#### empty_cells_cand function
* Identifies all empty cells and their number candidates
* Creates a dictionary mapping cell positions to valid candidate numbers

#### update_candidates function
* Used to update dictionary once a cell has been solved
* Updates all possible candidates as a way to dyanmically update what the next best choice for solving would be

### evaluation.py

#### measure_solving_time function
* Measures time for each algorithm to solve a Board
* Takes the best of n time it takes (n can be modified for testing)

#### compare_algorithms function
* Benchmarks different solving algorithms on the same puzzle
* Generates statistics on solution times and steps required

#### 'main' function
* Tests algorithms' performance by iterating through a list of integers where each integer is the number of pieces removed from the puzzle
* Set up to compare the A* solving function and the Backtracking solving function
* Uses parameters defined by the user to set up testing
* Formats and prints table in the command line output showing the testing results