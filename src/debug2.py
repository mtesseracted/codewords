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
# data2 = WordList(wordfile2)
# speller = SpellChecker(data2)
puzz = PuzzleGrid(blank='#', checker=None) #speller.check)
builder = GridBuilder(puzz)

num_letters = 26
word_list = []
uniqs = set(''.join(word_list))
isafe = 0
while len(uniqs) < num_letters:
    new_word = data1[np.random.randint(0, len(data1))]
    if len(new_word) < 4: continue
    new_list = word_list + [new_word,]
    new_uniqs = set(''.join(new_list))
    if len(new_uniqs) == len(uniqs):
        continue
    else:
        uniqs = new_uniqs
        word_list = new_list

    isafe += 1
    if isafe > 0.5 * len(data1):
        break


for word in word_list:
    if not builder.place_word(word):
        print(f'!! Cannot place "{word}" !!')

# @TODO: need to be able to condense the grid
print(puzz)
debug_var = 1
