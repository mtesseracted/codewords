import numpy as np
from copy import copy
from puzzles import PuzzleGrid

class GridBuilder():
    def __init__(self, puzzle:PuzzleGrid):
        self.puzzle = puzzle # type PuzzleGrid

    
    def build_optimized_grid(self, word_list, min_size:int=20, max_size:int=26):

        for size in range(min_size, max_size+1):
            self.puzzle.max_grid_size = size
            if self.build_grid(word_list):
                return self.puzzle
        
        raise ValueError(f"Unable to find a size {max_size} grid for that word list")


    def place_word(self, word):
        ''' place a word in the puzzle so that it shares a letter with an existing word '''
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
    #end def place_word(self, word):


    def build_grid(self, word_list):

        # try different permuations
        for itry in range(len(word_list)):
            self.puzzle.clear_words()

            # try this permutation
            permuted = self.get_good_order(word_list, itry)
            for word in permuted:
                if not self.place_word(word): break

            if len(self.puzzle.words) == len(word_list):
                return True

        return False


    def get_good_order(self, word_list, idx0):
        pop_list = copy(word_list)
        ret = [word_list[idx0],]
        pop_list.remove(ret[0])
        isafe = 0
        while len(pop_list) > 0 and isafe < len(word_list):
            for w in pop_list:
                if len(set(''.join(ret)).intersection(w)) > 0:
                    pop_list.remove(w)
                    ret.append(w)
                    break

            isafe += 1

        if len(pop_list) > 0:
            raise ValueError('Cannot satisfy common letter ordering')
        return ret


