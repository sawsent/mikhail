from config.config import *
from utils.pathbuilder import build_path as bp
from audio.transcriber import VoskTranscriber
from storage.transcript import Transcript
from storage.transcript_storage_manager import TranscriptStorageManager

import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def start(directory, max_audio_filesize=MAX_AUDIO_FILESIZE, allowed_formats=ALLOWED_FORMATS, model=MODEL_NAME):

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
        print(f"Found {len(allowed_files)} suitable files in '{directory}'. Indexing...")

    
    build_directories()

    transcript = create_transcript(directory, allowed_files, model)

    TranscriptStorageManager.save(transcript)

    print(f"Successfully started Mikhail in '{directory}'")

    
def build_directories():
    os.mkdir(LOCAL_DIR)
    os.mkdir(bp(LOCAL_DIR, '.transcript'))
    os.mkdir(bp(LOCAL_DIR, 'sentence'))
    os.mkdir(bp(LOCAL_DIR, 'word'))


def transcribe_file(transcriber, directory, file, index, max):
    #print(f"Indexing {index + 1} / {max}: {file}")

    path = bp(directory, file)
    return {
        'file': file,
        'words': transcriber.transcribe(path)
        }


def create_transcript(directory, allowed_files, model):

    transcriber = VoskTranscriber(bp(MODELS_DIR, model))

    results = {}
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(transcribe_file, transcriber, directory, file, idx, len(allowed_files)): file for idx, file in enumerate(allowed_files)}
        
        for future in tqdm(as_completed(future_to_file), desc='', unit='file', total=len(allowed_files)):
            try:
                result = future.result()
                results[result['file']] = result['words']
            except Exception as exc:
                print(f"Error processing file {future_to_file[future]}: {exc}")
    
    transcriber.clean()

    return Transcript(results, directory, model, datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')) 




def get_all_allowed_files(file_list, conditions):
    allowed_files = [file_name for file_name in file_list if all([condition(file_name) for condition in conditions])]

    return allowed_files
            

    
