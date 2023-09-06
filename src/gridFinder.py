import numpy as np
from copy import copy

class GridBuilder():
    def __init__(self, puzzle):
        self.puzzle = puzzle # type PuzzleGrid

    def place_word(self, word):
        ''' place a word in the puzzle so that it shares a letter with an existing word '''
        # @TODO: could make it optimial by choosing the smallest footprint choice
        # of all combos, will be horribly expensive as it grows
        # a better heuristic will be once it's a certain size, then reject moves
        # that grow the area of the grid by too much
        # if area(grid) > 100, reject moves that grow the area by more than
        # a monotically decreasing function
        if len(self.puzzle.words) == 0: # no words yet
            self.puzzle.append_word(word, [0,0], True)
            return True

        for ii, old in enumerate(self.puzzle.words):
            common = set(old).intersection(word)
            if len(common) == 0: continue # no common letters

            new_orient = not self.puzzle.directions[ii]
            old_xy = self.puzzle.coordinates[ii] # old coordinates
            for comm in common:
                ios = [io for io, ch in enumerate(old) if ch == comm]
                iws = [io for io, ch in enumerate(word) if ch == comm]

                for iw in iws:
                    for io in ios:
                        if self.puzzle.directions[ii]: # horizontal old, vertical new
                            new_xy = [old_xy[0] - iw, old_xy[1] + io]
                        else: # vetical old, horizontal new
                            new_xy = [old_xy[0] + io, old_xy[1] - iw]

                        self.puzzle.append_word(word, new_xy, new_orient)
                        if self.puzzle.validate() and self.puzzle.spell_check():
                            return True
                        else:
                            self.puzzle.delete_item(-1)

        return False # tried all combos, none valid
    #end def add_word(self, word):


