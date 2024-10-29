from config.config import LOCAL_DIR, ASK_CONFIRMATION
from utils.utils import build_path as bp

import os
import shutil
from tqdm import tqdm

def clean(directory):

    if not os.path.exists(f"{directory}/{LOCAL_DIR}"):
        print('mikhail not started here. Aborting...')
        exit(1)

    confirmation_prompt = f"You are about to clear all files in '{directory}/{LOCAL_DIR}, including transcripts and output files. Do you wish to continue? (y/n) \n >> "
    decision = not ASK_CONFIRMATION or input(confirmation_prompt).lower() == 'y'
    
    directories = {
        'transcripts': bp(directory, LOCAL_DIR, '.transcript'),
        'words': bp(directory, LOCAL_DIR, 'word'),
        'sentences': bp(directory, LOCAL_DIR, 'sentence')
    }

    if decision:
        for desc, dir_path in directories.items():
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                with tqdm(total=len(files), desc=f"Deleting {desc}", unit="file") as pbar:
                    for file in files:
                        file_path = os.path.join(dir_path, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                        pbar.update(1)

                os.rmdir(dir_path)

        os.rmdir(bp(directory, LOCAL_DIR))

        print(f"Successfully cleaned up mikhail from '{directory}'.")

    else:
        print("Aborting...")
        exit(1)