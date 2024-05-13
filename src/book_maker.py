import os, sys
import numpy as np
import matplotlib.pyplot as plt

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList
from puzzlePrinter import PuzzlePrinter

seed = 0
np.random.seed(seed)

libpath = '/home/al/opt/word_dictionaries/custom/'
# wordfile1 = os.path.join(libpath, 'google-10000-english.txt')
wordfile1 = os.path.join(libpath, 'common_scrabble_ordered.txt')
data1 = WordList(wordfile1)
word_list = PuzzleGrid.make_word_list(data1)

# make the puzzle
puzz = PuzzleGrid(blank=' ', checker=None)
puzz = GridBuilder(puzz).build_optimized_grid(word_list, min_size=20, max_size=24)
puzz.make_code(seed)
puzz.set_knowns('aoxz')

# show puzzle
printer = PuzzlePrinter(puzz)
fig = plt.figure(figsize=(8, 10))
fig = printer.create_puzzle_fig(fig, fill_all=False)
plt.show()

# show puzzle solution
fig = plt.figure(figsize=(8, 10))
fig = printer.create_puzzle_fig(fig, fill_all=True)
plt.show()

