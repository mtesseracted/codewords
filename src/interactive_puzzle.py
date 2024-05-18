import os, sys
from copy import copy, deepcopy
import numpy as np
import matplotlib.pyplot as plt

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList
from puzzlePrinter import PuzzlePrinter

seed = 2
np.random.seed(seed)

libpath = '/home/al/opt/word_dictionaries/custom/'
# wordfile1 = os.path.join(libpath, 'google-10000-english.txt')
wordfile1 = os.path.join(libpath, 'common_scrabble_ordered.txt')
data1 = WordList(wordfile1)
word_list = PuzzleGrid.make_word_list(data1, min_word_count=16)

# make the puzzle
puzz = PuzzleGrid(blank=' ', checker=None)
puzz = GridBuilder(puzz).build_optimized_grid(word_list, min_size=20, max_size=24, 
                                              extra_words=data1, extra_count=20)
puzz.make_code(seed)
# puzz.set_knowns('aoxz')
puzz.set_knowns(4)

ans = ''
exits = ['x', 'exit', 'q', 'quit']
resets = ['reset', 'r']
guess_puzz = puzz.copy()
fig = plt.figure(figsize=(8, 10))
fig.show()
while ans.lower() not in exits:

    # show puzzle
    printer = PuzzlePrinter(guess_puzz)
    fig.clear()
    fig = printer.create_puzzle_fig(fig, fill_all=False)
    plt.draw()

    # ans = input("Enter (quit), (reset), or (number letter); (-num is remove guess): ")
    ans = input("Enter (quit), (reset), or (number letter): ")
    # print(ans)
    if ans == '':
        continue 

    elif ans.lower() not in exits + resets:
        try:
            if ans.startswith('-'):
                guess_puzz.remove_guess(ans[1])
            else:
                splits = ans.split()
                num, lett = int(splits[0]), splits[1][0].lower()
                guess_puzz.add_guess(num, lett)
        except ValueError as err:
            print(err)

    elif ans.lower() in resets:
        guess_puzz = puzz.copy()

    if puzz.check_solve():
        print("** SOLVED! **")
        break


# show puzzle solution
fig = plt.figure(figsize=(8, 10))
fig = printer.create_puzzle_fig(fig, fill_all=True)
ans = input("Save solution to file? [N/filename]:")
if ans.lower() not in ['n', 'no']:
    plt.savefig(ans)
else:
    plt.show()




