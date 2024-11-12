from storage.transcript_storage_manager import TranscriptStorageManager
from storage.transcript import Transcript
from utils.utils import build_path as bp
from config.config import LOCAL_DIR

def list_words(directory: str, min_occurences=0):
    transcript: Transcript = TranscriptStorageManager.load(bp(directory, LOCAL_DIR, '.transcript', 'dir.transcript'))
    words = dict(sorted({word: len(occurences) for word, occurences in transcript.words.items() if len(occurences) >= min_occurences}.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))

    print(f"Found {len(words)} words {f"with at least {min_occurences} appearences " if min_occurences > 1 else ''}in current directory.")

    max_length_word = max([4] + [len(word) for word in words.keys()])

    print(f" WORD {(max_length_word - 4) * ' '} | AMOUNT ")
    print(f"--{max_length_word * '-'}-|--------")
    
    for word, amount in words.items():
        print(f" {word} {(max_length_word - len(word)) * ' '} | {amount}")


