import os, sys
import numpy as np
import matplotlib.pyplot as plt

from gridFinder import GridBuilder
from puzzles import PuzzleGrid
from spellChecker import SpellChecker
from dataloader import WordList

np.random.seed(0)

libpath = '/home/al/opt/google-10000-english/'
# wordfile1 = os.path.join(libpath, 'google-10000-english.txt')
wordfile1 = os.path.join(libpath, 'common_scrabble.txt')
data1 = WordList(wordfile1)

# wordfile2 = os.path.join(libpath, 'scrabble2019.txt')
# data2 = WordList(wordfile2)
# speller = SpellChecker(data2)

min_word_size = 4
max_word_size = 10

num_letters = 10
min_word_count = 2
min_total_letters = 40
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

# get total number of words up to a certain count
while len(word_list) < min_word_count or len(''.join(word_list)) < min_total_letters:
    new_word = data1[np.random.randint(0, len(data1))]
    if len(new_word) < min_word_size or len(new_word) > max_word_size: continue
    if new_word in word_list: continue
    word_list.append(new_word)

# second_list = [
#     'grace',
#     'sewing',
#     'mystery',
#     'winnie',
#     'cowboy',
#     'sailor',
# ]
# second_list = [s.upper() for s in second_list]
# word_list.extend(second_list)

found = -1
for size in range(24, 25):
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

grid = puzz.make_grid()
mask = grid != puzz.blank
x, y = np.where(mask)
letters = grid[mask]

fig = plt.figure(figsize=(8, 10))
ax = fig.add_subplot(20, 1, (1, 16))
ax.axis('off')
bg_shape = np.array([8, 8]) * fig.dpi
bg_shape = [*bg_shape.astype(int), 3]
bg_img = np.zeros(bg_shape, dtype=np.uint8)
bg_col = np.array([100, 200, 100]) # lime green
bg_img[:, :, :] = bg_col[None, None, :]
ax.imshow(bg_img)

grid_max = max(x.max(), y.max(), 16)
box_size = round(bg_shape[0] / (grid_max + 3))

for xc, yc, ll in zip(x, y, letters):
    ximg = box_size * (xc + 1)
    yimg = box_size * (yc + 1)
    ilett = ord(ll.lower()) - ord('a')
    p = plt.Rectangle((ximg, yimg), box_size, box_size, fill=False, lw=1.2)
    ax.text(ximg + 1, yimg + 3, f'{ilett+1}', fontsize=8,
            horizontalalignment='left', verticalalignment='top', transform=ax.transData)
    ax.text(ximg + 0.5 * box_size, yimg + 0.6 * box_size, f'{ll.upper()}', fontsize=12,
            horizontalalignment='center', verticalalignment='center', transform=ax.transData)
    p.set_transform(ax.transData)
    ax.add_patch(p)


# cross out list subplot
ax = fig.add_subplot(20, 1, 17)
ax.axis('off')
bg_shape = np.array([10 * 1 / 20, 8]) * fig.dpi
bg_shape = [*bg_shape.astype(int), 3]
bg_img = np.zeros(bg_shape, dtype=np.uint8)
bg_col = np.array([220, 100, 120]) # light red
bg_img[:, :, :] = bg_col[None, None, :]
ax.imshow(bg_img)
spacer = round(bg_shape[1] / 27.5)
for ii in range(26):
    ximg = spacer * (ii + 1)
    yimg = round(0.5 * bg_shape[0])
    ax.text(ximg, yimg, f'{chr(ii + ord("A"))}', fontsize=8,
            horizontalalignment='center', verticalalignment='center', transform=ax.transData)


# fill in letter box codes
ax = fig.add_subplot(20, 1, (18, 20))
ax.axis('off')
bg_shape = np.array([10 * 3 / 20, 8]) * fig.dpi
bg_shape = [*bg_shape.astype(int), 3]
bg_img = np.zeros(bg_shape, dtype=np.uint8)
bg_col = np.array([240, 80, 220]) # pink
bg_img[:, :, :] = bg_col[None, None, :]
ax.imshow(bg_img)

wspacer = round(bg_shape[1] / 15)
hspacer = round(bg_shape[0] / 3)
for jj in range(2):
    for ii in range(13):
        ximg = wspacer * (ii + 1)
        yimg = hspacer * (jj + 0.5)
        ilett = ii + jj * 13 + 1
        p = plt.Rectangle((ximg, yimg), wspacer, hspacer, fill=False, lw=1.2)
        ax.text(ximg + 1, yimg + 3, f'{ilett}', fontsize=8,
                horizontalalignment='left', verticalalignment='top', transform=ax.transData)
        p.set_transform(ax.transData)
        ax.add_patch(p)

fig.tight_layout(pad=0)
plt.show()

debug_var = 1
