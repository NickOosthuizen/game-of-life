import random
import os
import time

def initialize_cells(grid_size):
    grid = [[random.randint(0, 1) for i in range(grid_size)] for j in range(grid_size)]
    return grid 

def play_round(cell_list):
    list_size = len(cell_list)
    result_grid = cell_list
    for i in range(list_size):
        for j in range(list_size):
            num_neighbors = 0

            if i > 0:
                if j > 0:
                    num_neighbors += cell_list[i-1][j-1]
                num_neighbors += cell_list[i-1][j]
                if j < (list_size-1):
                    num_neighbors += cell_list[i-1][j+1]
            if j > 0:
                num_neighbors += cell_list[i][j-1]
            if j < (list_size-1):
                num_neighbors += cell_list[i][j+1]
            if i < (list_size-1):
                if j > 0:
                    num_neighbors += cell_list[i+1][j-1]
                num_neighbors += cell_list[i+1][j]
                if j < (list_size-1):
                    num_neighbors += cell_list[i+1][j+1]
            if cell_list[i][j] == 1:
                if num_neighbors < 2:
                    result_grid[i][j] = 0
                elif num_neighbors > 3:
                    result_grid[i][j] = 0
            elif num_neighbors == 3:
                result_grid[i][j] = 1
    return result_grid


def cells_not_dead(cell_list):
    for row in cell_list:
        for cell in row:
            if cell == 1:
                return True
    return False


def display_cells(cell_list):
    os.system('clear')
    for row in cell_list:
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
    while True:
        size = input("How big do you want your square: ")
        try:
            size = int(size)
            break
        except ValueError:
            print("You have to pass in an integer!")
    cell_grid = initialize_cells(size)
    display_cells(cell_grid)
    while cells_not_dead(cell_grid):
        cell_grid = play_round(cell_grid)
        display_cells(cell_grid)


if __name__ == "__main__":
    play_game()