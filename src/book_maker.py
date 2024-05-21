import os, sys, time
from copy import copy, deepcopy
from math import ceil
import numpy as np
import matplotlib.pyplot as plt

from gridFinder import GridBuilder, GridException
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList
from puzzlePrinter import PuzzlePrinter

# @TODO:
# save/load puzzle
# DONE ~add arg to make_word_list for starting words
# DONE ~plot for solutions, either 2x2 per page or 2x8 code solutions
# DONE ~8.5 x 11 print with margins
# bash script for pdf stitcher: stich puzz*.pdf, then soln*.pdf, then join those


num_puzzles = 4
seed_start = 10

custom_num, custom_file = 2, 'word_lists/list1.txt'

save_dir = f"book__puzzle12-{num_puzzles}__seed-{seed_start}"
os.makedirs(save_dir, exist_ok=True)

libpath = '/home/al/opt/word_dictionaries/custom/'
wordfile1 = os.path.join(libpath, 'common_scrabble_ordered.txt')
data1 = WordList(wordfile1)

puzz_list = [None,] * num_puzzles

t0 = time.time()
for ip in range(num_puzzles):
    seed = seed_start + ip
    np.random.seed(seed)
    if ip+1 == custom_num:
        ll = open(custom_file, 'r').readlines()
        ll = [l.strip().upper() for l in ll]
        word_list = PuzzleGrid.make_word_list(data1, min_word_count=16, init_list=ll)
    else:
        word_list = PuzzleGrid.make_word_list(data1, min_word_count=16)

    # try:
    puzz = PuzzleGrid(blank=' ', checker=None)
    puzz = GridBuilder(puzz).build_optimized_grid(word_list, min_size=20, max_size=24,
                                                extra_words=data1, extra_count=20)
    # except GridException as ge:
    #     ip -= 1
    #     continue

    puzz.make_code(seed)
    puzz.set_knowns(4)
    puzz_list[ip] = puzz


t1 = time.time()
print(f"Made {num_puzzles} puzzles in {t1-t0:.2f}s")


for ip, puzz in enumerate(puzz_list):

    fig = plt.figure(figsize=(8.5, 11))
    printer = PuzzlePrinter(puzz)
    printer.create_puzzle_fig(fig, fill_all=False, title=f"Grackle Puzzle {ip+1}")
    fig.tight_layout(w_pad=0, h_pad=0, pad=0) #pad=0)
    plt.savefig(os.path.join(save_dir, f"puzz{ip+1:03d}.png"), pad_inches=0)
    plt.close(fig)

    fig = plt.figure(figsize=(8.5, 11))
    printer = PuzzlePrinter(puzz)
    printer.create_puzzle_fig(fig, fill_all=True, title=f"Grackle Puzzle {ip+1}")
    fig.tight_layout(w_pad=0, h_pad=0, pad=0) #pad=0)
    plt.savefig(os.path.join(save_dir, f"solv{ip+1:03d}.png"), pad_inches=0)
    plt.close(fig)

soln_pages = ceil(len(puzz_list) / 8)
for ii in range(soln_pages):

    fig = plt.figure(figsize=(8.5, 11))
    ilo, ihi = ii * 8, min((ii+1) * 8, len(puzz_list))
    printer = PuzzlePrinter(puzz_list[ilo:ihi])
    printer.create_solution_fig(fig, labels=list(range(ilo+1, ihi+1)))
    fig.tight_layout(w_pad=0, h_pad=0)
    plt.savefig(os.path.join(save_dir, f"soln{ilo+1:03d}-{ihi+1:03d}.png"), pad_inches=0)
    plt.close(fig)


t2 = time.time()
print(f"Saved {num_puzzles} puzzles in {t2-t1:.2f}s")


debug_var = 1
