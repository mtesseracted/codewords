Plan: 
Automate making codewords puzzles. 
Tasks:
- Load the dataset and manipulate it, e.g. only allow words between certain lengths.
- Plot the puzzle as empty boxes, and with certain letters filled in (up to completely filled in)
- Make the puzzle config!
- All algos are sampling methods for placement, need to make infrastructure to
  try these algos: place next word at desired spot, see if it breaks the
boundaries, etc. 

Ideas for how to generate a puzzle:
- Get a certain number of words that in aggregate have all letters.
If we assume we want something that is less than XxX size of squares, then
trim it if it has too many words?

- Start with a word, add another word that has at least one letter not covered by the previous word(s), maybe not a good way for layout because you also need the next word to have a letter in common with the previous word

- probably going to need to generate the next word on the fly, unlike a
  crossword there is the additional constraint of the next word has to have
certain letters. 
