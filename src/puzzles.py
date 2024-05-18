import numpy as np
import random
from typing import List
from copy import copy, deepcopy

class PuzzleGrid():
    """ @TODO: refactor so the grid is a member of PuzzleGrid """

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
        self.solution = []

    def __copy__(self):
        ret = PuzzleGrid(blank=self.blank, checker=self.checker, 
                         max_grid_size=self.max_grid_size,)
        ret.grid = deepcopy(self.grid)
        ret.words = deepcopy(self.words)
        ret.coordinates = deepcopy(self.coordinates)
        ret.directions = deepcopy(self.directions)
        ret.knowns = deepcopy(self.knowns)
        ret.code = deepcopy(self.code)
        ret.solution = deepcopy(self.solution)

        return ret

    def copy(self):
        return self.__copy__()


    def append_word(self, word, coordinate, direction):
        """
        :param word:set_knowns
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
        self.solution = self.code.copy()

    @property
    def code_inv(self):
        return np.argsort(self.code)

    def letter_count(self, a):
        """ how many times does this letter appear """
        counts = 0
        for word in self.words:
            counts += sum([l == a for l in word])

        return counts



    def set_knowns(self, knowns):
        """ set/choose which letters are the known ones """

        if isinstance(knowns, int): # choose a random number of knowns
            uncommon = 'qxzjfkb' # only include at most one of these letters
            commons = 'aeiostln'

            self.knowns = [
                self.alph_num(commons[np.random.randint(len(commons))]),
            ]
            if knowns > 1:
                self.knowns.append(self.alph_num(uncommon[np.random.randint(len(uncommon))]))

            while len(self.knowns) < knowns:
                new_lett = np.random.randint(26)
                if new_lett not in self.knowns:
                    self.knowns.append(new_lett)

        elif isinstance(knowns, (list, str)): # user decided knowns
            if len(knowns) > 0 and isinstance(knowns[0], str):
                aoff = ord('a')
                self.knowns = list(set([ord(l.lower())-aoff for l in knowns]))
            else: # set of ints
                self.knowns = list(set(knowns)) # only keep uniques
        
        else:
            raise ValueError("knowns should be a list, str, or int")

    #end def set_knowns()

    def add_guess(self, num, lett):
        """ guess a number letter combo and add that the puzzle """
        inum = num - 1 # switch to 0-based
        anum = self.alph_num(lett)
        if anum in self.knowns:
            raise ValueError("This letter is already known")

        if inum in self.code[self.knowns]:
            raise ValueError("This number is already known")

        # corr_lett = self.num_alph(self.code[inum])
        corr_lett = self.num_alph(self.code_inv[inum])
        if corr_lett != lett: # guess is incorrect, update words with guess
            self.swap_letters(corr_lett, lett)

        self.knowns.append(self.alph_num(lett))
        return self
    #end def add_guess()


    def remove_guess(self, lett):
        try:
            anum = int(lett)
            lett = self.num_alph(anum)
        except ValueError as err:
            anum = self.alph_num(lett)

        if anum in self.knowns:
            self.knowns.remove(anum)
        else:
            raise ValueError("This letter is not known")

        curr_num = self.code[anum]
        # find correct letter
        orig_lett = self.num_alph(np.argsort(self.solution)[curr_num])
        if orig_lett != lett:
            self.swap_letters(orig_lett, lett)

        return self
    #end def remove_guess

    def code_letter(self, a):
        return self.code[self.alph_num(a)]


    def swap_letters(self, a, b):
        if a == b: return self

        # swap letters in the word list
        for iw, word in enumerate(self.words):
            tmp = word.lower().replace(a, '@')
            tmp = tmp.replace(b, a)
            tmp = tmp.replace('@', b) # swap
            self.words[iw] = tmp.upper()

        # swap letters in the code so they show up the same in printing
        na = self.alph_num(a)
        nb = self.alph_num(b)
        tmp = self.code[na]
        self.code[na] = self.code[nb]
        self.code[nb] = tmp

        return self
    #end def swap_letters


    @staticmethod
    def alph_num(lett): # alpha (a-z,A-Z) to number (0-25)
        return ord(lett.lower()) - ord('a')

    @staticmethod
    def num_alph(num): # number (0-25) to alpha (a-z)
        return chr(num + ord('a'))


    @staticmethod
    def make_word_list(data, min_word_size=4, max_word_size=18, 
                       min_word_count=12, min_total_letters=200):
        
        num_letters = 26
        word_list = []
        uniqs = set(''.join(word_list))
        
        # get a set of words that have all the letters
        isafe = 0 # safety counter for looping
        while len(uniqs) < num_letters:
            # irand = np.random.randint(0, (len(data)))
            irand = int(np.random.beta(1, 3) * len(data))
            new_word = data[irand]
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

    def check_solve(self):
        if len(set(self.knowns)) == 26:
            if np.allclose(self.code, self.solution):
                return True

        return False
        

#end class PuzzleGrid():
