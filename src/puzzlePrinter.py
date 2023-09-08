
from matplotlib.patches import Rectangle
from puzzles import PuzzleGrid

class PuzzlePrinter():
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def print_empty_grid(self, ax):
        grid = self.puzzle.make_grid()

        
