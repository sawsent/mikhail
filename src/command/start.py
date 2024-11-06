from config.config import *
from utils.utils import build_path as bp
from audio.transcriber import VoskTranscriber
from storage.transcript import Transcript
from storage.transcript_storage_manager import TranscriptStorageManager

import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import inquirer


def start(directory, max_audio_filesize=MAX_AUDIO_FILESIZE, allowed_formats=ALLOWED_FORMATS, force=False):

    clean_confirmation = False

    if os.path.exists(bp(directory, LOCAL_DIR)):
        if force:
            clean_confirmation = input(f"You are about to delete everything in '{bp(directory, LOCAL_DIR)}'. Are you sure you want to continue? (y/n) >> ").lower() == 'y' 

        if clean_confirmation: 
            from command.clean import clean
            clean(directory)
            print('\n')

        else:
            print(f"Mikhail already started in '{directory}', use refresh to reindex. ")
            exit(1)

    model_options = [d for d in os.listdir(bp(BASE_DIR, 'models')) if os.path.isdir(bp(BASE_DIR, 'models', d))]
    if len(model_options) == 0:
        print(f"No models found. Please download a model from 'https://alphacephei.com/vosk/models' and add it to '{bp(BASE_DIR, 'models')}'")
        exit(1)

    conditions = [
        lambda fn: os.path.getsize(bp(directory, fn)) < max_audio_filesize, 
        lambda fn: fn.split('.')[-1] in allowed_formats
    ]
    allowed_files = get_all_allowed_files(os.listdir(directory), conditions=conditions)

    if len(allowed_files) == 0:
        print("No suitable files found. No changes were made. Quitting...")
        exit(1)
    else:
        print(f"Found {len(allowed_files)} suitable files in '{directory}'.")

    model = get_model(model_options)

    print(f"Transcribing files with model '{model}'")
    
    transcript = create_transcript(directory, allowed_files, model)

    build_directories()
    TranscriptStorageManager.save(transcript)

    print(f"Successfully started Mikhail in '{directory}'")

    
def build_directories():
    os.mkdir(LOCAL_DIR)
    os.mkdir(bp(LOCAL_DIR, '.transcript'))
    os.mkdir(bp(LOCAL_DIR, 'sentence'))
    os.mkdir(bp(LOCAL_DIR, 'word'))

def get_model(options):

    if len(options) == 0:
        print(f"No models found. Please download a model from 'https://alphacephei.com/vosk/models' and add it to '{bp(BASE_DIR, 'models')}'")
        exit(1)
    
    elif len(options) == 1:
        model = options[0]

    else: 
        questions = [
            inquirer.List(
                "choice",
                message="Choose the Model you want to use",
                choices=options,
            ),
        ]
        
        model = inquirer.prompt(questions)['choice']
    
    return model


def transcribe_file(transcriber, directory, file, index, max):

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
        
        for future in tqdm(as_completed(future_to_file), desc='Transcribing', unit='file', total=len(allowed_files)):
            try:
                result = future.result()
                results[result['file']] = result['words']
            except Exception as exc:
                print(f"Error processing file {future_to_file[future]}: {exc}")
                raise exc

    if CLEAR_CONVERSION_CACHE:
        transcriber.clean()

    return Transcript.from_dict(results, directory, model, datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')) 




def get_all_allowed_files(file_list, conditions):
    allowed_files = [file_name for file_name in file_list if all([condition(file_name) for condition in conditions])]

    return allowed_files
            

    
