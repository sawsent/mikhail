from config.config import *
from utils.pathbuilder import build_path as bp
from audio.transcriber import VoskTranscriber

import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def start(directory, max_audio_filesize=MAX_AUDIO_FILESIZE, allowed_formats=ALLOWED_FORMATS):

    # check if mikhail dir already exists
    # if yes -> cancel op and advise refresh instead, if no keep going

    if os.path.exists(bp(directory, 'mikhail')):
        print(f"Mikhail already started in '{directory}', use refresh to reindex. ")
        exit(1)


    # 1. Find all audio files in the directory below 25MB
    conditions = [
        lambda fn: os.path.getsize(bp(directory, fn)) < max_audio_filesize, 
        lambda fn: fn.split('.')[-1] in allowed_formats
    ]
    allowed_files = get_all_allowed_files(os.listdir(directory), conditions=conditions)

    if len(allowed_files) == 0:
        print("No suitable files found. No changes were made. Quitting...")
        exit(1)
    else:
        print(f"Found {len(allowed_files)} in '{directory}' files. Indexing...")

    
    build_directories()

    create_transcripts(directory, allowed_files)

    
def build_directories():
    os.mkdir(LOCAL_DIR)
    os.mkdir(bp(LOCAL_DIR, '.transcript'))
    os.mkdir(bp(LOCAL_DIR, 'sentence'))
    os.mkdir(bp(LOCAL_DIR, 'word'))


def create_transcript(transcriber, directory, file, index, max):
    print(f"Indexing {index + 1} / {max}: {file}")
    path = bp(directory, file)
    return {file: transcriber.transcribe(path).word_list}


def create_transcripts(directory, allowed_files):

    transcriber = VoskTranscriber(MODEL_PATH)

    results = []
    with ThreadPoolExecutor() as executor:
        # Submit each transcription task
        future_to_file = {executor.submit(create_transcript, transcriber, directory, file, idx, len(allowed_files)): file for idx, file in enumerate(allowed_files)}
        
        # Collect the results as they complete
        for future in as_completed(future_to_file):
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"Error processing file {future_to_file[future]}: {exc}")
    
    transcriber.clean()

    print(results)
    




def get_all_allowed_files(file_list, conditions):
    allowed_files = [file_name for file_name in file_list if all([condition(file_name) for condition in conditions])]

    return allowed_files
            

    
