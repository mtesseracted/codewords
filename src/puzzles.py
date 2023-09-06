import numpy as np

class PuzzleGrid():
    def __init__(self, blank='#'):
        """
        """
        self.words = []
        self.coordinates = []
        self.directions = []
        self.blank = blank
        self.grid = None

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
        self.grid = self.make_grid() # assume redraw needed
        co1 = np.asarray(self.coordinates)
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

    def __str__(self):
        self.grid = self.make_grid()
        spacer = ' '
        row_strings = [spacer.join(row) for row in self.grid]
        return '\n'.join(row_strings)
