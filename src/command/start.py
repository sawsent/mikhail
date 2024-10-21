import os
from config.config import *

def start(directory, max_audio_filesize=MAX_AUDIO_FILESIZE, allowed_formats=ALLOWED_FORMATS):

    print(f"Indexing all files in '{directory}'")

    # 1. Find all audio files in the directory below 25MB
    allowed_files = get_all_allowed_files(os.listdir(directory), 
                                          conditions=[
                                              lambda fn: os.path.getsize(directory + '/' + fn) < max_audio_filesize, 
                                              lambda fn: fn.split('.')[-1] in allowed_formats
                                          ])

    if len(allowed_files) == 0:
        print("No suitable files found. No changes were made. Quitting...")
    else:
        print(f"Found {len(allowed_files)} files. Indexing...")

    # create mikhail directory and its subdirectories


    # create all transcript files
    


def get_all_allowed_files(file_list, conditions):
    allowed_files = [file_name for file_name in file_list if all([condition(file_name) for condition in conditions])]

    return allowed_files
            
    