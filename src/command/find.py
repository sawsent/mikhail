from storage.transcript_storage_manager import TranscriptStorageManager, Transcript
from utils.utils import build_path as bp
from config.config import LOCAL_DIR
from audio.simple_play import play_test_sound
from utils.prompter import Prompter, Action, Option

import threading

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
    options = [
        Option('hello 2', '2'),
        Option('hello 3', '3')
    ]

    options = [Option(occurence['file'], occurence) for occurence in occurences]

    actions = [
        Action(' ', 'Space to play', lambda _: threading.Thread(target=play_test_sound).start()),
        Action('a', 'troll', lambda data: print('i trolled ya' + str(data), end=''))
    ]
    

    prompter = Prompter(options, actions)
    prompter.prompt()

    print(occurences)


def handle_word_not_found(word):
    print(f"Word '{word}' not found in current directory.")
    exit(0)
