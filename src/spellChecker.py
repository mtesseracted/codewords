
class SpellChecker():
    def __init__(self, word_list):
        self.word_list = word_list

    def check(self, word):
        ''' dumb as a box of rocks '''
        return word in self.word_list
