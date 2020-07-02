import random
import os
import time
import tkinter


class Game_App(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.display_canvas = None 
        self.create_welcome_screen()

    def create_welcome_screen(self):
        # welcome screen is made up of a title label, a direction label, a entry to get size of grid, and a submit button
        self.welcome_label = tkinter.Label(master = self.master, text = "Welcome to Conway's Game of Life", fg = "black", bg = "white")
        self.enter_size_label = tkinter.Label(master = self.master, text = "Please enter desired grid size:", fg = "black", bg = "white")
        self.get_size_entry = tkinter.Entry(master = self.master, fg = "black", bg = "white")
        # button will attempt to create grid if input is valid
        self.submit_button = tkinter.Button(master = self.master, text="Submit", command = self.attempt_game_construction)
        self.welcome_label.pack()
        self.enter_size_label.pack()
        self.get_size_entry.pack()
        self.submit_button.pack()

    def attempt_game_construction(self):
        size = self.get_size_entry.get()
        # entered value must be an integer
        try:
            size = int(size)
        except ValueError:
            self.enter_size_label.config(text = "You must enter an integer > 0!")
            return 

        # entered value must be greater than 0
        if size <= 0:
            self.enter_size_label.config(text = "You must enter an integer > 0!")
            return
        
        self.grid_dim = size
        self.add_grid()
        self.update_grid()

    # clear the welcome screen
    def remove_entry_widgets(self):
        self.welcome_label.pack_forget()
        self.enter_size_label.pack_forget()
        self.get_size_entry.pack_forget()
        self.submit_button.pack_forget()

    def add_grid(self):
        size = self.grid_dim
        self.remove_entry_widgets()

        # app creates its own game grid
        self.game_grid = game_of_life_grid(size)

        # display is a canvas
        self.display_canvas = tkinter.Canvas(self.master, width = 5 * size + 5, height = 5 * size + 5, bd = 0, bg = "white")
        self.display_canvas.pack()
        
        # fill canvas with rectangles corresponding to dead and alive cells in the game grid
        for i in range(size):
            for j in range(size):
                if self.game_grid.grid[i][j] == 1:
                    self.display_canvas.create_rectangle(5 * i, 5 * j, 5 * i + 5, 5 * j + 5, width = 0, fill='black')
                else:
                    self.display_canvas.create_rectangle(5 * i, 5 * j, 5 * i + 5, 5 * j + 5, width = 0, fill='white')
        
    def update_grid(self):
        self.game_grid.play_round()

        size = self.grid_dim
        for i in range(size):
            for j in range(size):
                # update the colors of cells that have changed
                if self.game_grid.grid[i][j] != self.game_grid.previous_grid[i][j]:
                    cell_color = "white"
                    if self.game_grid.grid[i][j] == 1:
                        cell_color = "black"
                    self.display_canvas.create_rectangle(5 * i, 5 * j, 5 * i + 5, 5 * j + 5, width = 0, fill=cell_color)
        
        # function calls itself after a delay so that it can run inside the tkinter mainloop
        self.master.after(250, self.update_grid)


                
# game of life object to manage the grid of the program
# follows the classic rules of Conway's Game of Life
class game_of_life_grid():
    def __init__(self, dimension):
        # initialize a 2D array of 1s and 0s to serve as the starting point of the game
        self.grid = [[random.randint(0, 1) for i in range(dimension)] for j in range(dimension)]
        self.grid_dim = dimension
        self.previous_grid = None
        self.change_choords = []
    
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
                        # self.change_choords.append(((i, j), 0))
                    elif num_neighbors > 3:
                        result_grid[i][j] = 0
                         # self.change_choords.append(((i, j), 0))
                    else:
                        result_grid[i][j] = 1
                # If a dead cell has 3 neighbors, a new cell is born
                elif num_neighbors == 3:
                    result_grid[i][j] = 1
                    # self.change_choords.append(((i, j), 1))
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
    root = tkinter.Tk()
    root.title("Conway's Game of Life")
    app = Game_App(root)
    root.mainloop()
        

if __name__ == "__main__":
    play_game()