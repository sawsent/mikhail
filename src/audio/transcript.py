class Transcript:
    def __init__(self, dict):
        """
            dict: {filename: [{word: word, start: start, end: end}]
            
            converts this to:
            {word: [{filename: filename, start: start, end: end}]}
        """
        self.word_list = []

        self.populate(dict)

    def populate(self, dict):
        for word in dict:
            self.word_list.append(word)
