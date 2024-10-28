class Transcript:
    def __init__(self, dict: dict, directory: str, model_used: str, timestamp: str):
        """
            dict: {filename: [{word: word, start: start, end: end}]
            
            converts this to:
            {word: [{filename: filename, start: start, end: end}]}
        """
        self.words, self.files_searched = self.get_words_and_files_searched(dict)
        self.directory = directory
        self.model = model_used
        self.timestamp = timestamp

    def get_words_and_files_searched(self, dict: dict) -> tuple[dict, list]:
        words = {}
        files_searched = []
        for file, info in dict.items():
            if not file in files_searched:
                files_searched.append(file)
            for word_info in info:
                payload = { 
                        'file': file, 
                        'start': word_info['start'], 
                        'end': word_info['end']
                    }
                if not word_info['word'] in words:
                    words[word_info['word']] = []
                
                words[word_info['word']].append(payload)

        return words, files_searched
    
    def get_headers(self):
        return {
            'directory:str': self.directory, 
            'files_searched:list': '/'.join([f for f in self.files_searched]),
            'model:str': self.model,
            'timestamp:str': self.timestamp
            }
    

    def to_string(self):
        return f"transcript {'{'} \n\
    model: {self.model}, \n\
    timestamp: {self.timestamp}, \n\
    directory: {self.directory}, \n\
    words: {[f"{word}: [{len(results)}]" for word, results in self.words.items()]} \n{'}'}"