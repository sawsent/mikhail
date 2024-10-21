from config.config import LOCAL_DIR, ASK_CONFIRMATION

import os
import shutil 

def clean(directory):

    if not os.path.exists(f"{directory}/{LOCAL_DIR}"):
        print('mikhail not started here. Aborting...')
        exit(1)

    confirmation_prompt = f"You are about to clear all files in '{directory}/{LOCAL_DIR}, including transcripts and output files. Do you wish to continue? (y/n) \n >> "
    decision = not ASK_CONFIRMATION or input(confirmation_prompt).lower() == 'y'
    
    if decision:
        shutil.rmtree(LOCAL_DIR)

    else:
        print("Aborting...")
        exit(1)