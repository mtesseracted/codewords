import os, sys
import numpy as np

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList

np.random.seed(0)

libpath = '/mnt/c/Users/amahler.TDY/libraries/google-10000-english/'
wordfile1 = os.path.join(libpath, 'google-10000-english.txt')
wordfile2 = os.path.join(libpath, '20k.txt')
data1 = WordList(wordfile1)
data2 = WordList(wordfile1)

speller = SpellChecker(data2)
puzz = PuzzleGrid(blank=' ', checker=None) #speller.check)
builder = GridBuilder(puzz)
# builder.add_word(data[101])
# puzz.append_word(data[100], [0,0], True) # price
# puzz.append_word(data[101], [1, 2], True) # date
# puzz.append_word(data[102], [3, 1], False) # back

# r l s t n e a
word_list = [
    'slate',
    'neat',
    'nearest',
    'tan',
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
