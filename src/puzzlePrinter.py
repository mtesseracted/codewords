import numpy as np
from matplotlib.patches import Rectangle
from puzzles import PuzzleGrid

class PuzzlePrinter():
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def grid2coordinates(self, puzz):
        grid = puzz.make_grid()
        mask = grid != puzz.blank
        x, y = np.where(mask)
        letters = grid[mask]
        return x, y, letters

    def scramble_numbers(self):
        pass

    def print_empty_grid(self, ax):
        grid = self.puzzle.make_grid()

        
