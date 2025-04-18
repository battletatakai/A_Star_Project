#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint, shuffle

def find_empty(board):
    """
    Finds an empty cell in the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        tuple[int, int]|None: The position of the first empty cell found as a tuple of row and column indices, or None if no empty cell is found.
    """

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def valid(board, pos, num):
    """
    Checks whether a number is valid in a cell of the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.
        pos (tuple[int, int]): The position of the cell to check as a tuple of row and column indices.
        num (int): The number to check.

    Returns:
        bool: True if the number is valid in the cell, False otherwise.
    """

    for i in range(9):
        if board[i][pos[1]] == num:
            return False

    for j in range(9):
        if board[pos[0]][j] == num:
            return False

    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[start_i + i][start_j + j] == num:
                return False
    return True


def solve_A(board, cell_cand=None):

    """ Function created to solve sudoku using our A* algorithm 
    
    Recycled some components from the backtracking algorithm that was provided """
    
    # Imports needed for this specific function
    from astar import empty_cells_cand, update_candidates
    import heapq

    if cell_cand is None:
        # Initialize the dictionary of empty cells with candidates
        cell_cand = empty_cells_cand(board)

    if not cell_cand:
        return True  # Board has been solved

    # Use a priority queue to get the cell with the fewest candidates
    priority_queue = [(len(candidates), (i, j), candidates) for (i, j), candidates in cell_cand.items()]
    heapq.heapify(priority_queue)

    while priority_queue:
        dont_use, (i, j), candidates = heapq.heappop(priority_queue)

        for num in candidates:
            if valid(board, (i, j), num):
                # Place the number on the board
                board[i][j] = num
                # Update the candidates dictionary
                update_candidates(cell_cand, board, (i, j), num, add=True)

                
                if solve_A(board, cell_cand): # Recursive step
                    return True

                board[i][j] = 0
                update_candidates(cell_cand, board, (i, j), num, add=False)

        return False

    return False


def solve(board):
    """
    Solves the sudoku board using the backtracking algorithm.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        bool: True if the sudoku board is solvable, False otherwise.
    """

    empty = find_empty(board)
    if not empty:
        return True

    for nums in range(1, 10):
        if valid(board, empty, nums):
            board[empty[0]][empty[1]] = nums

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False


def generate_board(removed_cells=45):
    """
    Generates a random sudoku board with fewer initial numbers.

    Returns:
        list[list[int]]: A 9x9 sudoku board represented as a list of lists of integers.

    Raises:
        ValueError: If removed_cells is greater than or equal to 65, resulting in 16 or fewer filled cells.
    """

    # Check if removed_cells would result in 16 or fewer filled cells (unsolvable)
    if removed_cells >= 65:
        raise ValueError("Cannot create a board with 16 or fewer filled cells. The minimum number of clues for a solvable Sudoku is 17.")

    board = [[0 for i in range(9)] for j in range(9)]

    # Fill the diagonal boxes
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    # Fill the remaining cells with backtracking
    def fill_cells(board, row, col):
        """
        Fills the remaining cells of the sudoku board with backtracking.

        Args:
            board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.
            row (int): The current row index to fill.
            col (int): The current column index to fill.

        Returns:
            bool: True if the remaining cells are successfully filled, False otherwise.
        """

        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)

        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        for num in range(1, 10):
            if valid(board, (row, col), num):
                board[row][col] = num

                if fill_cells(board, row, col + 1):
                    return True

        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)

    for _ in range(removed_cells):
        row, col = randint(0, 8), randint(0, 8)
        board[row][col] = 0

    return board