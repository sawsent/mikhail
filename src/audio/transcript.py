class Transcript:
    def __init__(self, dict):
        self.word_list = []

        self.populate(dict)

    def populate(self, dict):
        for word in dict:
            self.word_list.append(word)