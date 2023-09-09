# @TODO: make a list that's the intersection of the 20k words and
# scrabble words
class WordList():
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = open(filepath).readlines()

    def __getitem__(self, item):
        return self.data[item][:-1] # remove newline

    def __len__(self):
        return len(self.data)