import random
import os
import time
import tkinter


class Game_App(tkinter.Frame):
    def __init__(self, master, initial_grid):
        super().__init__(master)
        self.master = master
        self.grid_dim = initial_grid.grid_dim
        # save a game_of_life object
        self.game_grid = initial_grid
        # array tracks canvas widgets
        self.grid_widgets = []
        self.add_grid()

    def add_grid(self):
        size = self.grid_dim
        for i in range(size):
            grid_row = []
            for j in range(size):
                cell_color = 'white'
                # seed widgets corresponding to living cells as black cells
                if self.game_grid.grid[i][j] == 1:
                    cell_color = 'black'
                # each cell is a canvas widget 
                square_canvas = tkinter.Canvas(self.master, width = 20, height = 20, bg = cell_color)
                # widgets aligned in a square grid
                square_canvas.grid(row = i, column = j)
                grid_row.append(square_canvas)
            self.grid_widgets.append(grid_row)
    
    def update_grid(self):
        size = self.grid_dim
        for i in range(size):
            for j in range(size):
                # update the colors of cells that have changed
                if self.game_grid.grid[i][j] != self.game_grid.previous_grid[i][j]:
                    cell_color = 'white'
                    if self.game_grid.grid[i][j] == 1:
                        cell_color = 'black'
                    self.grid_widgets[i][j].config(bg = cell_color)


                
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
    root = tkinter.Tk()
    app = Game_App(root, cell_grid)
    # run game until the grid reaches a static state
    root.update()
    while True:
        app.game_grid.play_round()
        app.update_grid()
        root.update()
        

if __name__ == "__main__":
    play_game()