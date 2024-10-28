from storage.transcript import Transcript
from utils.pathbuilder import build_path as bp
from config.config import LOCAL_DIR

class TranscriptStorageManager:
    WORD_SEPARATOR = ','

    @classmethod
    def save(cls, transcript: Transcript):
        dir_to_save_in = bp(transcript.directory, LOCAL_DIR, '.transcript')
        
        with open(bp(dir_to_save_in, 'dir.transcript'), 'w') as file:
            cls.write_headers(file, transcript.get_headers())
            cls.write_words(file, transcript.words)
            file.write('#end')

    @classmethod
    def write_headers(cls, file, headers):
        for identifier, header in headers.items():
            file.write(cls.build_line('#', identifier, '=', header, sep=''))

    @classmethod
    def write_words(cls, file, words):
        for word, appearences in words.items():
            for appearence in appearences:
                file.write(cls.build_line(word, appearence['start'], appearence['end'], appearence['file'], sep=cls.WORD_SEPARATOR))


    @classmethod
    def build_line(cls, *args, sep=WORD_SEPARATOR):
        return sep.join([str(arg) for arg in args]) + '\n' 

