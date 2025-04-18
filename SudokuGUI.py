#!/usr/bin/python
# -*- coding: utf-8 -*-
from sudokutools import valid, find_empty, generate_board, solve
from copy import deepcopy
from sys import exit
import pygame
import time
import random

pygame.init()


class Board:
    def __init__(self, window):
        """
        Initializes a Board object.

        Args:
            window: The Pygame window object.
        """
        # Generate a new Sudoku board and create a solved version of it.
        self.board = generate_board()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        # Create a 2D list of Tile objects to represent the Sudoku board.
        self.tiles = [
            [Tile(self.board[i][j], window, i * 60, j * 60) for j in range(9)]
            for i in range(9)
        ]
        self.window = window
        
        # Dictionary of available user inputs for the help panel
        self.user_inputs = {
            "1-9": "Enter numbers",
            "Backspace": "Clear cell",
            "Enter": "Confirm value",
            "H": "Get hint",
            "R": "Restart game",
            "Space": "Solve (A*)",
            "D": "Solve (backtracking)",
            "Esc": "Exit game"
        }

    def draw_board(self):
        """
        Draws the Sudoku board on the Pygame window.
        """
        for i in range(9):
            for j in range(9):
                # Draw vertical lines every three columns.
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (j // 3 * 180, 0),
                        (j // 3 * 180, 540),
                        4,
                    )
                # Draw horizontal lines every three rows.
                if i % 3 == 0 and i != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (0, i // 3 * 180),
                        (540, i // 3 * 180),
                        4,
                    )
                # Draw the Tile object on the board.
                self.tiles[i][j].draw((0, 0, 0), 1)

                # Display the Tile value if it is not 0 (empty).
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].display(
                        self.tiles[i][j].value, (21 + j * 60, 16 + i * 60), (0, 0, 0)
                    )
        # Draw a horizontal line at the bottom of the board.
        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (0, (i + 1) // 3 * 180),
            (540, (i + 1) // 3 * 180),
            4,
        )

    def deselect(self, tile):
        """
        Deselects all tiles except the given tile.

        Args:
            tile (Tile): The tile that should remain selected.

        Returns:
            None
        """
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys, wrong, time):
        """
        Redraws the Sudoku board on the game window, highlighting selected, correct, and incorrect tiles, displaying the
        current wrong count and time, and rendering the current keys (potential values) for each tile.

        Args:
            keys (dict): A dictionary containing tuples of (x, y) coordinates as keys and potential values as values.
            wrong (int): The current wrong count.
            time (int): The current time elapsed.

        Returns:
            None
        """
        self.window.fill((255, 255, 255))  # fill the window with white
        self.draw_board()  # draw the Sudoku board
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected:
                    # highlight selected tiles in green
                    self.tiles[j][i].draw((50, 205, 50), 4)
                elif self.tiles[i][j].correct:
                    # highlight correct tiles in dark green
                    self.tiles[j][i].draw((34, 139, 34), 4)
                elif self.tiles[i][j].incorrect:
                    # highlight incorrect tiles in red
                    self.tiles[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0:
            for value in keys:
                # display the potential values for each tile
                self.tiles[value[0]][value[1]].display(
                    keys[value],
                    (21 + value[0] * 60, 16 + value[1] * 60),
                    (128, 128, 128),
                )

        if wrong > 0:
            # display the current wrong count as an "X" icon and a number
            font = pygame.font.SysFont("Bauhaus 93", 30)
            text = font.render("X", True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont("Bahnschrift", 40)
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        # display the current time elapsed as a number
        font = pygame.font.SysFont("Bahnschrift", 40)
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        
        # Draw the help panel on the side
        self.draw_help_panel()
        
        pygame.display.flip()  # update the game window

    def visualSolve_A(self, wrong, time):
        """ Shows the visual solve for our A* algorithm
        
        Just helps visualize the algorithm and the path it takes to solve 
        
        A lot of what was used here is recycled from the provided repo """
        
        # Needed imports for this specific function
        from astar import empty_cells_cand, update_candidates
        import heapq

        # Initialize candidates and priority queue
        cell_cand = empty_cells_cand(self.board)
        if not cell_cand:
            return True  # Board is solved

        priority_queue = [(len(candidates), (i, j), candidates) for (i, j), candidates in cell_cand.items()]
        heapq.heapify(priority_queue)

        while priority_queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            dont_use, (i, j), candidates = heapq.heappop(priority_queue)

            for num in candidates:
                if valid(self.board, (i, j), num):
                # Place the number and update the board visually
                    self.board[i][j] = num
                    self.tiles[i][j].value = num
                    self.tiles[i][j].correct = True
                    pygame.time.delay(63)
                    self.redraw({}, wrong, time)

                # Update candidates and recurse
                    update_candidates(cell_cand, self.board, (i, j), num, add=True)
                    if self.visualSolve_A(wrong, time):
                        return True

                # Backtrack
                    self.board[i][j] = 0
                    self.tiles[i][j].value = 0
                    self.tiles[i][j].incorrect = True
                    self.tiles[i][j].correct = False
                    pygame.time.delay(63)
                    self.redraw({}, wrong, time)
                    update_candidates(cell_cand, self.board, (i, j), num, add=False)

            return False

        return False

    def visualSolve(self, wrong, time):
        """
        Recursively solves the Sudoku board visually, highlighting correct and incorrect tiles as it fills them in.

        Args:
            wrong (int): The current wrong count.
            time (int): The current time elapsed.

        Returns:
            bool: True if the board is successfully solved, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()  # exit the game if the user clicks the close button

        empty = find_empty(self.board)
        if not empty:
            return True  # the board is solved if there are no empty tiles left

        for nums in range(9):
            if valid(self.board, (empty[0], empty[1]), nums + 1):

                # Count number of missing specific numbers
                # Could have Values stored for each number to get path cost
                # Find candidates for each missing cell
                # Calculate total cost to start at lowest cost

                
                # fill in the current empty tile with a valid number
                self.board[empty[0]][empty[1]] = nums + 1
                self.tiles[empty[0]][empty[1]].value = nums + 1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)  # delay to slow down the solving animation
                self.redraw(
                    {}, wrong, time
                )  # redraw the game window with the updated board

                if self.visualSolve(wrong, time):
                    return True  # recursively solve the rest of the board if the current move is valid

                # if the current move is not valid, reset the tile and highlight it as incorrect
                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)  # delay to slow down the solving animation
                self.redraw(
                    {}, wrong, time
                )  # redraw the game window with the updated board

    def hint(self, keys):
        """
        Provides a hint by filling in a random empty tile with the correct number.

        Args:
            keys (dict): A dictionary containing tuples of (x, y) coordinates as keys and potential values as values.

        Returns:
            bool: True if a hint is successfully provided, False if the board is already solved.
        """
        while True:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] == 0:
                if (j, i) in keys:
                    del keys[(j, i)]
                # fill in the selected empty tile with the correct number
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True
            elif self.board == self.solvedBoard:
                return False  # the board is already solved, so no hint can be provided.

    def draw_help_panel(self):
        """
        Draws a panel that shows available user inputs.
        """
        panel_x = 550
        panel_y = 20
        panel_width = 260
        panel_height = 300
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.window, (240, 240, 240), panel_rect)
        pygame.draw.rect(self.window, (0, 0, 0), panel_rect, 2)
        
        # Draw title
        title_font = pygame.font.SysFont("Bahnschrift", 24)
        title_text = title_font.render("Available Controls", True, (0, 0, 0))
        title_width = title_text.get_width()
        title_x = panel_x + (panel_width - title_width) // 2  # Center the title
        self.window.blit(title_text, (title_x, panel_y + 10))
        
        # Draw divider line
        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (panel_x + 10, panel_y + 40),
            (panel_x + panel_width - 10, panel_y + 40),
            2
        )
        
        # Draw controls list
        font = pygame.font.SysFont("Bahnschrift", 16)
        y_offset = panel_y + 60
        key_column_width = 96
        
        for key, description in self.user_inputs.items():
            # Draw key with background highlight
            key_bg_rect = pygame.Rect(panel_x + 15, y_offset - 2, key_column_width - 10, 22)
            pygame.draw.rect(self.window, (220, 230, 255), key_bg_rect)
            pygame.draw.rect(self.window, (180, 190, 220), key_bg_rect, 1)
            
            # Draw key text
            key_text = font.render(key, True, (0, 0, 150))
            self.window.blit(key_text, (panel_x + 20, y_offset))
            
            # Draw description
            desc_text = font.render(description, True, (0, 0, 0))
            self.window.blit(desc_text, (panel_x + key_column_width + 15, y_offset))
            
            y_offset += 30


class Tile:
    def __init__(
        self,
        value,
        window,
        x1,
        y1,
    ):
        """
        Initializes a Tile object.

        Args:
            value (int): The value to be displayed in the Tile.
            window (pygame.Surface): The surface to draw the Tile on.
            x1 (int): The x-coordinate of the top-left corner of the Tile.
            y1 (int): The y-coordinate of the top-left corner of the Tile.

        Attributes:
            value (int): The value to be displayed in the Tile.
            window (pygame.Surface): The surface to draw the Tile on.
            rect (pygame.Rect): The rectangular area of the Tile.
            selected (bool): Whether the Tile is currently selected.
            correct (bool): Whether the value in the Tile is correct.
            incorrect (bool): Whether the value in the Tile is incorrect.
        """

        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        """
        Draws the Tile on the window with a colored border.

        Args:
            color (tuple[int, int, int]): The RGB color value of the border.
            thickness (int): The thickness of the border.

        Returns:
            None.
        """

        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(
        self,
        value,
        position,
        color,
    ):
        """
        Displays the value of the Tile in the center of the Tile.

        Args:
            value (int): The value to be displayed.
            position (tuple[int, int]): The (x, y) coordinates of the center of the Tile.
            color (tuple[int, int, int]): The RGB color value of the text.

        Returns:
            None.
        """

        font = pygame.font.SysFont("lato", 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        """
        Checks if the Tile is clicked by the mouse.

        Args:
            mousePos (tuple[int, int]): The (x, y) coordinates of the mouse.

        Returns:
            bool: True if the Tile is clicked, False otherwise.
        """

        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected


def main():
    # Set up the pygame window
    screen = pygame.display.set_mode((820, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku Solver AI")
    icon = pygame.image.load("assets/thumbnail.png")
    pygame.display.set_icon(icon)

    # Display "Generating Random Grid" text while generating a random grid
    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Random Grid", True, (0, 0, 0))
    screen.blit(text, (156, 290))
    pygame.display.flip()

    # Initialize variables
    wrong = 0
    board = Board(screen)
    selected = (-1, -1)
    keyDict = {}
    startTime = time.time()

    # Loop until the user escapes
    while True:
        # Get elapsed time and format it to display in the window
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        # Handle events
        for event in pygame.event.get():
            elapsed = time.time() - startTime
            passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # Check if a Tile is clicked
                mousePos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        if board.tiles[i][j].clicked(mousePos):
                            selected = (i, j)
                            board.deselect(board.tiles[i][j])
            elif event.type == pygame.KEYDOWN:
                # Handle key presses
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1, -1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9
                    elif (
                        event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE
                    ):
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]
                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if (
                                keyDict[selected]
                                != board.solvedBoard[selected[1]][selected[0]]
                            ):
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                # break

                            board.tiles[selected[1]][selected[0]].value = keyDict[
                                selected
                            ]
                            board.board[selected[1]][selected[0]] = keyDict[selected]
                            del keyDict[selected]

                # Handle hint key
                if event.key == pygame.K_h:
                    board.hint(keyDict)

                # Handle restart key
                if event.key == pygame.K_r:
                    board = Board(screen)
                    selected = (-1, -1)
                    keyDict = {}
                    wrong = 0
                    startTime = time.time()

                # Handle escape key
                if event.key == pygame.K_ESCAPE:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return

                # Space key triggers visual solving with A* algorithm
                if event.key == pygame.K_SPACE:
                    # Deselect all tiles and clear keyDict
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    keyDict = {}

                    # Solve the sudoku visually and reset all tile correctness
                    elapsed = time.time() - startTime
                    passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                    board.visualSolve_A(wrong, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False
                    print(passedTime)

                # D key triggers visual solving with backtracking algorithm
                if event.key == pygame.K_d:
                    # Deselect all tiles and clear keyDict
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    keyDict = {}

                    # Solve the sudoku visually and reset all tile correctness
                    elapsed = time.time() - startTime
                    passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                    board.visualSolve(wrong, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False
                    print(passedTime)

        board.redraw(keyDict, wrong, passedTime)

main()
pygame.quit()