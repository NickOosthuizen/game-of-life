import random
import os
import time
# import tkinter

"""
class Game_App(tkinter.Frame):
    def __init__(self, master=None, initial_grid):
        super().__init__(master)
        self.master = master
        self.grid_width = 50
        self.grid_height = 38
        self.pack()
        self.add_grid(initial_grid)

    def add_grid(self, grid):
        self.grid_canvas = tkinter.Canvas(self.master, width = self.grid_width, height = seld.grid_height, bg= 'snow')
        self.grid_canvas.pack()
        img = tkinter.PhotoImage(width = self.grid_width, height = self.grid_height)
"""

# game of life object to manage the grid of the program
# follows the classic rules of Conway's Game of Life
class game_of_life_grid():
    def __init__(self, dimension):
        # initialize a 2D array of 1s and 0s to serve as the starting point of the game
        self.grid = [[random.randint(0, 1) for i in range(dimension)] for j in range(dimension)]
        self.grid_dim = dimension
        self.previous_grid = None
    
    def play_round(self):
        list_size = self.grid_dim
        # create a temporary array filled with 0s to record the state of the grid after
        # a new round without changing the previous grid during the round
        result_grid = [[0 for i in range(list_size)] for j in range(list_size)]
        for i in range(list_size):
            for j in range(list_size):
                # each cell starts with 0 neighbors assumed
                num_neighbors = 0

                # if statements check to ensure that the array reads will not
                # trigger an array index error
                # As the grid holds either a 1 or 0, can just add the cell's neighbors
                # to get its number of neighbors
                if i > 0:
                    if j > 0:
                        num_neighbors += self.grid[i-1][j-1]
                    num_neighbors += self.grid[i-1][j]
                    if j < (list_size-1):
                        num_neighbors += self.grid[i-1][j+1]
                if j > 0:
                    num_neighbors += self.grid[i][j-1]
                if j < (list_size-1):
                    num_neighbors += self.grid[i][j+1]
                if i < (list_size-1):
                    if j > 0:
                        num_neighbors += self.grid[i+1][j-1]
                    num_neighbors += self.grid[i+1][j]
                    if j < (list_size-1):
                        num_neighbors += self.grid[i+1][j+1]

                # If a cell is alive with either < 2 or > 3 neighbors, it dies, otherwise survives
                if self.grid[i][j] == 1:
                    if num_neighbors < 2:
                        result_grid[i][j] = 0
                    elif num_neighbors > 3:
                        result_grid[i][j] = 0
                    else:
                        result_grid[i][j] = 1
                # If a dead cell has 3 neighbors, a new cell is born
                elif num_neighbors == 3:
                    result_grid[i][j] = 1
                # Otherwise the cell stays dead
                else:
                    result_grid[i][j] = 0
        # record the old grid as previous_grid and replace grid with the result grid
        # the previous_grid allows us to check if the game has reached a static state
        self.previous_grid = self.grid
        self.grid = result_grid
    
    # If the current grid is the same as the previous grid, no new change can occur
    def grid_active(self):
        if self.previous_grid is not None:
            if self.grid == self.previous_grid:
                return False
        return True

    # clears screen and prints current grid
    def display_cells(self):
        os.system('clear')
        for row in self.grid:
            display_row = ""
            for cell in row:
                if cell == 1:
                    display_row += "@"
                else:
                    display_row += " "
            print(display_row)
        time.sleep(.5)


def play_game():
    size = str()
    # prompt user for a desired grid size until user gives one
    while True:
        size = input("How big do you want your square: ")
        try:
            size = int(size)
            break
        except ValueError:
            print("You have to pass in an integer!")
    cell_grid = game_of_life_grid(size)
    cell_grid.display_cells()
    # run game until the grid reaches a static state
    while cell_grid.grid_active():
        cell_grid.play_round()
        cell_grid.display_cells()


if __name__ == "__main__":
    play_game()