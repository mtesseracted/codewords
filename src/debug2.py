import os, sys
import numpy as np

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList

np.random.seed(0)

libpath = '/mnt/c/Users/amahler.TDY/libraries/google-10000-english/'
# wordfile1 = os.path.join(libpath, 'google-10000-english.txt')
wordfile1 = os.path.join(libpath, 'common_scrabble.txt')
data1 = WordList(wordfile1)

# wordfile2 = os.path.join(libpath, 'scrabble2019.txt')
# data2 = WordList(wordfile2)
# speller = SpellChecker(data2)

min_word_size = 4
max_word_size = 12

num_letters = 26
word_list = []
uniqs = set(''.join(word_list))
isafe = 0
while len(uniqs) < num_letters:
    new_word = data1[np.random.randint(0, len(data1))]
    if len(new_word) < min_word_size or len(new_word) > max_word_size: continue
    new_list = word_list + [new_word,]
    new_uniqs = set(''.join(new_list))
    if len(new_uniqs) == len(uniqs):
        continue
    else:
        uniqs = new_uniqs
        word_list = new_list

    isafe += 1
    if isafe > 0.5 * len(data1):
        print('!! Cannot find words that satisfy constraints !!')
        break

second_list = [
    'grace',
    'sewing',
    'mystery',
    'winnie',
    'cowboy',
    'sailor',
]
second_list = [s.upper() for s in second_list]
word_list.extend(second_list)

found = -1
for size in range(14, 24):
    puzz = PuzzleGrid(max_grid_size=size, blank=' ', checker=None) #speller.check)
    builder = GridBuilder(puzz)
    if builder.build_grid(word_list):
        print(puzz)
        print(f'\nFound solution of size {puzz.grid.shape}')
        found = size
        break

if found == -1:
    print(f'\n!! Unable to find a grid for that word list !!')

# @TODO: once found, add some small to medium-ish random words without
# making it larger to make the puzzle easier and also look better

# @TODO: need to be able to condense the grid
debug_var = 1
