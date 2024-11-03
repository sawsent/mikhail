class Transcript:
    LIST_DELIMITER = '/'

    def __init__(self, words, headers: dict):
        """
            dict: {filename: [{word: word, start: start, end: end}]
            
            converts this to:
            {word: [{filename: filename, start: start, end: end}]}
        """
        self.words = words
        self.files_searched = headers['files_searched'] 
        self.directory = headers['directory']
        self.model = headers['model']
        self.timestamp = headers['timestamp']
    
    @classmethod
    def from_dict(cls, dict: dict, directory, model_used, timestamp):
        words, files_searched = cls.get_words_and_files_searched(dict)
        headers = {
            'files_searched': files_searched,
            'directory': directory,
            'model': model_used,
            'timestamp': timestamp
        }
        return Transcript(words, headers)


    @classmethod
    def get_words_and_files_searched(cls, dict: dict) -> tuple[dict, list]:
        words = {}
        files_searched = []
        for file, info in dict.items():
            if not file in files_searched:
                files_searched.append(file)
            for word_info in info:
                payload = cls.to_word_payload(file, word_info['start'], word_info['end'])
                if not word_info['word'] in words:
                    words[word_info['word']] = []
                
                words[word_info['word']].append(payload)

        return words, files_searched
    
    @classmethod
    def to_word_payload(cls, file, start, end):
        return {
            'file': file, 
            'start': start, 
            'end': end
        }
    
    def get_headers(self):
        return {
            'directory:str': self.directory, 
            'files_searched:list': self.LIST_DELIMITER.join([f for f in self.files_searched]),
            'model:str': self.model,
            'timestamp:str': self.timestamp
            }
    

    def to_string(self):
        return f"transcript {'{'} \n\
    model: {self.model}, \n\
    timestamp: {self.timestamp}, \n\
    directory: {self.directory}, \n\
    words: {[f"{word}: [{len(results)}]" for word, results in self.words.items()]} \n{'}'}"