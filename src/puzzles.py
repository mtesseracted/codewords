import numpy as np

class PuzzleGrid():
    def __init__(self, blank='#', checker=None):
        """
        """
        self.grid = None
        self.words = []
        self.coordinates = []
        self.directions = []
        self.blank = blank
        self.checker = checker

    def append_word(self, word, coordinate, direction):
        """
        :param word:
        :param coordinate:
        :param direction: True for horizontal, False for vertical
        :return:
        """
        self.words.append(word)
        self.coordinates.append(coordinate)
        self.directions.append(direction)

    def delete_item(self, item):
        del self.words[item]
        del self.coordinates[item]
        del self.directions[item]

    def extend_words(self, words, coordinates, directions):
        raise NotImplementedError

    def make_grid(self):
        ''' convert to PuzzleGrid? '''
        if len(self.words) == 0: return None # base case
        co1 = np.asarray(self.coordinates)
        co2 = np.empty_like(co1)
        for ii, word in enumerate(self.words):
            if self.directions[ii]: # horizontal
                co2[ii] = co1[ii] + np.array([0, len(word)])
            else: # vertical
                co2[ii] = co1[ii] + np.array([len(word), 0])

        min_xy = co1.min(axis=0)
        co3 = np.concatenate([co1, co2])
        num_rows = co3[:, 0].max() - co3[:, 0].min() + 0
        num_cols = co3[:, 1].max() - co3[:, 1].min() + 0
        num_rows, num_cols = max(num_rows, 1), max(num_cols, 1) # min of 1
        self.grid = np.full((num_rows, num_cols), self.blank)

        co1 -= min_xy[None, :] # re-zero
        co2 -= min_xy[None, :]

        # populate the grid
        for ii, word in enumerate(self.words):
            if self.directions[ii]: # horizontal
                self.grid[co1[ii,0], co1[ii,1]:co2[ii,1]] = np.array(list(word))
            else:  # vertical
                self.grid[co1[ii,0]:co2[ii,0], co1[ii,1]] = np.array(list(word))

        return self.grid


    def validate(self):
        ''' determine if coordinates are self consistent '''
        # write them all down to grid, then make sure when you extract the word
        # that it's spelled correctly, runs in O(n) for n words
        # IDEA: on the fly validation, only check words that the added word crosses
        # bugged:
        # A) will validate when two parallel words are right next to each other
        #    and make nonsense 2 letter words
        # B) will validate when two words are laid end to end because their common
        #    letter with the perpendicular word is at the begging/end of the end to
        #    end words
        # these can be fixed by spell checking all words that can be extracted from
        # the grid. Spell checking can also be done by checking against the existing
        # database. We could also make sub databases for words all words of a certain
        # lenght to speed up lookup time instead of linear search. Also lexigraphical
        # database sort for binary search
        self.grid = self.make_grid() # assume redraw needed
        co1 = np.asarray(self.coordinates)
        co1 = co1 - co1.min(axis=0) # zero to be same as make_grid indices
        for ii, word in enumerate(self.words):
            if self.directions[ii]: # horizontal
                printed = self.grid[co1[ii,0], co1[ii,1]:co1[ii,1] + len(word)]
                if ''.join(printed) != word:
                    return False
            else: # vertical
                printed = self.grid[co1[ii,0]:co1[ii,0] + len(word), co1[ii,1]]
                if ''.join(printed) != word:
                        return False

        return True

    def shrink_grid(self, grid=None):
        ''' this is deprecated with on the fly make_grid '''
        grid = self.make_grid() #
        # take out empty rows and cols at the far right and bottom
        row_min = (self.grid == self.blank).argmin(axis=0).max()
        col_min = (self.grid == self.blank).argmin(axis=1).max()
        self.grid = self.grid[:row_min + 1, :col_min + 1]

        return self.grid

    def spell_check(self, checker=None):
        ''' spell check all words in the grid
        :param checker: spell checker function
        '''
        # iterate rows then cols, a word is anything not hashes and more than 1 char
        loc_checker = self.checker if checker is None else checker

        if loc_checker is None:
            def check(w):
                return w in self.words
        else:
            def check(w):
                return w in self.words or loc_checker(w)

        self.grid = self.make_grid()
        grid_str = self.__str__(self.grid, spacer='').split('\n')
        for row in grid_str:
            words = [w for w in row.split(self.blank) if len(w) > 1]
            for word in words:
                if not check(word):
                    return False

        grid_str = self.__str__(self.grid.T, spacer='').split('\n')
        for row in grid_str:
            words = [w for w in row.split(self.blank) if len(w) > 1]
            for word in words:
                if not check(word):
                    return False

        return True

    def __str__(self, grid=None, spacer=' '):
        if grid is None:
            grid = self.make_grid()
        row_strings = [spacer.join(row) for row in grid]
        return '\n'.join(row_strings)
