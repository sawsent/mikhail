from storage.transcript import Transcript
from utils.utils import build_path as bp
from config.config import LOCAL_DIR

class TranscriptStorageManager:
    WORD_SEPARATOR = ','

    @classmethod
    def save(cls, transcript: Transcript):
        dir_to_save_in = bp(transcript.directory, LOCAL_DIR, '.transcript')
        
        with open(bp(dir_to_save_in, 'dir.transcript'), 'w') as file:
            cls.__write_headers(file, transcript.get_headers())
            cls.__write_words(file, transcript.words)
            file.write('#end')
    
    @classmethod
    def load(cls, file_path: str) -> Transcript:
        headers = {}
        words = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if line.startswith('#end'):
                    return Transcript(words, headers)

                if line.startswith('#'):
                    key, header = cls.parse_header(line)
                    headers[key] = header
                
                else: 
                    word, start, end, file = line.split(cls.WORD_SEPARATOR)
                    if not word in words:
                        words[word] = []
                    words[word].append(Transcript.to_word_payload(file, float(start), float(end)))
                
    
    @classmethod
    def parse_header(cls, line: str) -> tuple[str, any]:
        split = line.split('=')

        typ = split[0].split(':')[1]
        key = split[0].split(':')[0].removeprefix('#')

        raw_header = split[1]

        if typ == 'str':
            return (key, raw_header)
        
        elif typ == 'list':
            return (key, raw_header.split(Transcript.LIST_DELIMITER))
        
        else: 
            raise Exception('Unknown header type.')

    @classmethod
    def parse_word(cls, line):
        # word, start, end, file
        pass

        

    @classmethod
    def __write_headers(cls, file, headers):
        for identifier, header in headers.items():
            file.write(cls.__build_line('#', identifier, '=', header, sep=''))

    @classmethod
    def __write_words(cls, file, words):
        for word, appearences in words.items():
            for appearence in appearences:
                file.write(cls.__build_line(word, appearence['start'], appearence['end'], appearence['file'], sep=cls.WORD_SEPARATOR))


    @classmethod
    def __build_line(cls, *args, sep=WORD_SEPARATOR):
        return sep.join([str(arg) for arg in args]) + '\n' 

