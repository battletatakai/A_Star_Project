from sudokutools import valid

def empty_cells_cand(board):

    """
    Function used to find all empty cells and create a dictionary that sets keys as the coordiantes
    and values are the possible candidates for that specific cell.
    """

    # Dictionary for empty cells
    cell_cand = {}

    # Get all empty cells and candidates
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                # Initialize a list to store candidates
                candidates = []

                # Uses valid function to check for valid candidates
                for num in range(1, 10):
                    if valid(board, (i, j), num):
                        # If it is a valid number, appends it to the candidates list
                        candidates.append(num)

                if candidates:
                    # Creates the key for the dictionary as the cooridnates of empty cell and the value are possible candidates
                    cell_cand[(i, j)] = candidates

    return cell_cand

def update_candidates(cell_cand, board, coordinates_cell, num, add=True):
    """
    Function used to update dictionary once a cell has been solved
    Also updates all possible candidates as a way to dyanmically update what the next best choice for solving would be
    """

    if add:
        # Deletes specific empty cell once solved
        if coordinates_cell in cell_cand:
            del cell_cand[coordinates_cell]
    else:
        # Redoes the candidates

        # Initializes a list for candidates
        candidates = []
        for num in range(1, 10):
            if valid(board, coordinates_cell, num):
                # Appending candidates to candidates list
                candidates.append(num)
        if candidates:
            # Uses coordinates_cell as key to value for candidates
            cell_cand[coordinates_cell] = candidates

    # Update candidates for other cells in the same row, column, and box
    row, col = coordinates_cell
    for i in range(9):
        # Update row
        if (row, i) in cell_cand and num in cell_cand[(row, i)]:
            cell_cand[(row, i)].remove(num)
        # Update column
        if (i, col) in cell_cand and num in cell_cand[(i, col)]:
            cell_cand[(i, col)].remove(num)

    start_i, start_j = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            cell = (start_i + i, start_j + j)
            if cell in cell_cand and num in cell_cand[cell]:
                cell_cand[cell].remove(num)