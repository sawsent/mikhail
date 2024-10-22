class Transcript:
    def __init__(self, dict: dict, model_used: str, timestamp: str):
        """
            dict: {filename: [{word: word, start: start, end: end}]
            
            converts this to:
            {word: [{filename: filename, start: start, end: end}]}
        """
        self.words = self.get_words(dict)
        self.model = model_used
        self.timestamp = timestamp

    def get_words(self, dict: dict):
        words = {}
        for file, info in dict.items():
            for word_info in info:
                payload = { 
                        'file': file, 
                        'start': word_info['start'], 
                        'end': word_info['end']
                    }
                if not word_info['word'] in words:
                    words[word_info['word']] = []
                
                words[word_info['word']].append(payload)

        return words

    def to_string(self):
        return f"transcript {'{'} \n\
    model: {self.model}, \n\
    timestamp: {self.timestamp}, \n\
    words: {[f"{word}: [{len(results)}]" for word, results in self.words.items()]} \n{'}'}"