import os
import numpy as np

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from dataloader import WordList

np.random.seed(0)

wordfile = '/mnt/c/Users/amahler.TDY/libraries/google-10000-english/google-10000-english.txt'
data = WordList(wordfile)

puzz = PuzzleGrid(blank='#')
builder = GridBuilder(puzz)
# builder.add_word(data[101])
# puzz.append_word(data[100], [0,0], True) # price
# puzz.append_word(data[101], [1, 2], True) # date
# puzz.append_word(data[102], [3, 1], False) # back

# a b c d e f
word_list = [
    'cab',
    'dab',
    'baddaf',
    'eacaff',
]
for word in word_list:
    if not builder.place_word(word):
        print(f'Cannot place {word}')
    else:
        print('')
        print(puzz)
        print('')

# print(puzz)
debug_var = 1
