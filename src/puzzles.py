import numpy as np
import random
from typing import List

class PuzzleGrid():

    def __init__(self, blank=' ', checker=None, max_grid_size=20):
        """
        """
        self.blank = blank     # blank character for str(self)
        self.checker = checker # spell checker
        self.max_grid_size = max_grid_size # largest allowed grid length or width
        self.grid = None       # grid representation @TODO: refactor into a separate class
        self.words = []        # words in the puzzle
        self.coordinates = []  # grid coordinates of the first letter in the word
        self.directions = []   # True = horizontal, False = vertical
        self.knowns = []
        self.code = list(range(26))

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
        if self.grid is not None:
            self.grid = None

    def delete_item(self, item):
        del self.words[item]
        del self.coordinates[item]
        del self.directions[item]
        if self.grid is not None:
            self.grid = None

    # def extend_words(self, words, coordinates, directions):
    #     if self.grid is not None:
    #         self.grid = None
    #     raise NotImplementedError


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
    
    #end def make_grid()


    def validate(self, size_check=True):
        ''' determine if coordinates are self consistent
            NB: this will not check for misspelled words created from words
                placed next to each other in parallel
        '''
        if self.grid is None:
            self.grid = self.make_grid() # assume redraw needed

        if size_check:
            if any([s > self.max_grid_size for s in self.grid.shape]):
                return False

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


    def spell_check(self, checker=None):
        ''' spell check all words in the grid
        :param checker: spell checker function
        '''
        # iterate rows then cols, a word is anything not split with self.blank
        # and more than 1 char
        loc_checker = self.checker if checker is None else checker
        if loc_checker is None: # fast version
            def check(w):
                return w in self.words
        else:
            def check(w):
                return w in self.words or loc_checker(w)

        if self.grid is None:
            self.grid = self.make_grid()

        # check rows
        grid_str = self.__str__(self.grid, spacer='').split('\n')
        for row in grid_str:
            words = [w for w in row.split(self.blank) if len(w) > 1]
            for word in words:
                if not check(word):
                    return False

        # check cols with transpose
        grid_str = self.__str__(self.grid.T, spacer='').split('\n')
        for row in grid_str:
            words = [w for w in row.split(self.blank) if len(w) > 1]
            for word in words:
                if not check(word):
                    return False

        return True
    
    #end def spell_check()


    def shrink_grid(self, grid=None):
        ''' this is deprecated with on the fly make_grid '''
        # @TODO: this could be a grid optimizer
        grid = self.make_grid() #
        # take out empty rows and cols at the far right and bottom
        row_min = (self.grid == self.blank).argmin(axis=0).max()
        col_min = (self.grid == self.blank).argmin(axis=1).max()
        self.grid = self.grid[:row_min + 1, :col_min + 1]

        return self.grid


    def clear_words(self):
        self.words = []
        self.coordinates = []
        self.directions = []


    def __str__(self, grid=None, spacer=' '):
        if grid is None:
            grid = self.make_grid()
        row_strings = [spacer.join(row) for row in grid]
        return '\n'.join(row_strings)


    def make_code(self, seed=None):
        """ scramble the letters into a random ordering """
        if seed:
            np.random.seed(seed)
        self.code = np.random.permutation(list(range(26)))
        self.code_inv = np.array([np.where(self.code == ii)[0][0] for ii in range(len(self.code))])

    def set_knowns(self, knowns):
        """ set/choose which letters are the known ones """

        if isinstance(knowns, int): # choose a random number of knowns
            excludes = ['q', 'x', 'z', 'j', 'f'] # only include at most one of these letters
            self.knowns = random.sample(range(26), knowns)

        elif isinstance(knowns, (list, str)): # user decided knowns
            if len(knowns) > 0 and isinstance(knowns[0], str):
                aoff = ord('a')
                self.knowns = list(set([ord(l.lower())-aoff for l in knowns]))
            else:
                self.knowns = list(set(knowns)) # only keep uniques
        
        else:
            raise ValueError("knowns should be a list, str, or int")

    #end def set_knowns()


    @staticmethod
    def make_word_list(data, min_word_size=4, max_word_size=18, 
                       min_word_count=18, min_total_letters=200):
        
        num_letters = 26
        word_list = []
        uniqs = set(''.join(word_list))
        
        # get a set of words that have all the letters
        isafe = 0 # safety counter for looping
        while len(uniqs) < num_letters:
            new_word = data[np.random.randint(0, len(data))]
            if len(new_word) < min_word_size or \
                len(new_word) > max_word_size: continue
            new_list = word_list + [new_word,]
            new_uniqs = set(''.join(new_list))
            if len(new_uniqs) == len(uniqs):
                continue
            else:
                uniqs = new_uniqs
                word_list = new_list

            isafe += 1
            if isafe > 0.5 * len(data):
                print('!! Cannot find words that satisfy constraints !!')
                raise ValueError("Cannot find a word list")
            
        # get total number of words up to be at least min_word_count and min_letter_count
        while len(word_list) < min_word_count and len(''.join(word_list)) < min_total_letters:
            new_word = data[np.random.randint(0, len(data))]
            if len(new_word) < min_word_size or len(new_word) > max_word_size: continue
            if new_word in word_list: continue
            word_list.append(new_word)

        return word_list
            
    #end def make_word_list()
        

#end class PuzzleGrid():
