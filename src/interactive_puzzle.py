import os, sys
from copy import copy
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

ans = ''
exits = ['x', 'exit', 'q', 'quit']
resets = ['reset', 'r']
guess_puzz = copy(puzz)
while ans.lower() not in exits:

    # show puzzle
    printer = PuzzlePrinter(puzz)
    fig = plt.figure(figsize=(8, 10))
    fig = printer.create_puzzle_fig(fig, fill_all=False)
    fig.show()

    # ans = input("Enter (quit), (reset), or (number letter); (-num is remove guess): ")
    ans = input("Enter (quit), (reset), or (number letter): ")
    # print(ans)
    if ans.lower() not in exits + resets:
        splits = ans.split()
        num, lett = int(splits[0]), splits[1][0].lower()
        guess_puzz.add_guess(num, lett)

    elif ans.lower() in resets:
        guess_puzz = copy(puzz)

    plt.close(fig)
    # fig.clear()



ans = input("Save to file? [N/filename]:")
if ans.lower() not in ['n', 'no']:
    # show puzzle solution
    fig = plt.figure(figsize=(8, 10))
    fig = printer.create_puzzle_fig(fig, fill_all=True)
    plt.savefig(ans)




