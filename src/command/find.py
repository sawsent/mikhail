from storage.transcript_storage_manager import TranscriptStorageManager, Transcript
from utils.utils import build_path as bp
from config.config import LOCAL_DIR

def find(directory: str, word: str):
    # load transcript
    transcript: Transcript = TranscriptStorageManager.load(bp(directory, LOCAL_DIR, '.transcript', 'dir.transcript'))

    words = transcript.words

    if not word in words:
        handle_word_not_found(word)

    else: 
        handle_word_found(words[word], word)
    


def handle_word_found(occurences, word):
    print(f"Found these occurences of '{word}':")
    print(occurences)


def handle_word_not_found(word):
    print(f"Word '{word}' not found in current directory.")
    exit(0)
