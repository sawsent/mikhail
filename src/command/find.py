from storage.transcript_storage_manager import TranscriptStorageManager, Transcript
from utils.utils import build_path as bp
from config.config import LOCAL_DIR
from audio.cropper import crop_into
from utils.prompter import Prompter, Action, Option
from audio.player import Player

import os

def find(directory: str, word: str):
    transcript: Transcript = TranscriptStorageManager.load(bp(directory, LOCAL_DIR, '.transcript', 'dir.transcript'))

    words = transcript.words

    if not word in words:
        handle_word_not_found(word, words)

    else: 
        handle_word_found(words[word], word, directory)
    
def handle_word_found(occurences, word, directory):
    print(f"Found {len(occurences)} occurences of '{word}':")

    occurences = enrich_with_spacing(occurences)

    options = [Option(f"'{word}' @ {occurence['file']} {occurence['space']}|| from {occurence['start']} to {occurence['end']}", occurence) for occurence in occurences]

    player = Player.get()
    actions = [
        Action(' ', 'Space to play', lambda option: play_or_crop_and_then_play(player, directory, option, word)),
        Action('e', 'Extract to file', lambda option: extract_to_file(directory, option.data, word)),
        Prompter.QUIT(help="Done"),
    ]
    
    prompter = Prompter(options, actions)
    prompter.prompt()

def play_or_crop_and_then_play(player, directory, option: Option, word):
    temp_file = temp_file_path(directory, option.data, word)
    occurence: dict = option.data

    ensure_exists(occurence, temp_file, directory)
    
    player.play(temp_file)

def extract_to_file(directory, occurence, word):
    temp_file = temp_file_path(directory, occurence, word)

    ensure_exists(occurence, temp_file, directory)
    
    output_file = occurence['temp-file'].replace('.temp', 'word')
    if not os.path.exists(output_file):
        os.rename(temp_file, output_file)

def ensure_exists(occurence, temp_file, directory):
    if not os.path.exists(temp_file):
        create_temp_file(directory, occurence, temp_file)
    if not 'temp-file' in occurence:
        occurence['temp-file'] = temp_file

def enrich_with_spacing(occurences):
    max_size = max([ len(oc['file']) for oc in occurences ])
    for oc in occurences:
        oc['space'] = ' ' * (max_size - len(oc['file']))

    return occurences

def temp_file_path(directory, occurence, word):
    return bp(directory, LOCAL_DIR, '.temp', occurence_to_temp_file_name(word, occurence))

def create_temp_file(directory, occurence, output_path):
    input_path = bp(directory, occurence['file'])
    occurence['temp-file'] = output_path 
    crop_into(input_path, output_path, occurence['start'], occurence['end'])

def occurence_to_temp_file_name(word, occurence):
    file, start, end = (occurence['file'], occurence['start'], occurence['end'])
    processed_file = ''.join(file.split('.')[:-1])
    file_extension = file.split('.')[-1]
    processed_start = str(start).replace('.', '_')
    processed_end = str(end).replace('.', '_')
    return f"{word}-{processed_file}-{processed_start}-{processed_end}.{file_extension}"


def handle_word_not_found(word, words):
    print(f"Word '{word}' not found in current directory.")
    exit(0)

