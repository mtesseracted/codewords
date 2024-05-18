import os, sys, time
from copy import copy, deepcopy
import numpy as np
import matplotlib.pyplot as plt

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList
from puzzlePrinter import PuzzlePrinter


num_puzzles = 10
seed_start = 10

libpath = '/home/al/opt/word_dictionaries/custom/'
wordfile1 = os.path.join(libpath, 'common_scrabble_ordered.txt')
data1 = WordList(wordfile1)

puzz_list = [None,] * num_puzzles

t0 = time.time()
for ip in range(num_puzzles):
    seed = seed_start + ip
    np.random.seed(seed)
    word_list = PuzzleGrid.make_word_list(data1, min_word_count=16)

    puzz = PuzzleGrid(blank=' ', checker=None)
    puzz = GridBuilder(puzz).build_optimized_grid(word_list, min_size=20, max_size=24,
                                                  extra_words=data1, extra_count=20)
    puzz.make_code(seed)
    puzz.set_knowns(4)
    puzz_list[ip] = puzz


t1 = time.time()
print(f"Made {num_puzzles} puzzles in {t1-t0:.2f}s")

debug_var = 1

fig = plt.figure(figsize=(8, 10))
printer = PuzzlePrinter(puzz_list[0])
fig = printer.create_puzzle_fig(fig, fill_all=True)
plt.show()


debug_var = 1
