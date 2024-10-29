from config.config import *
from utils.utils import delete_directory_with_tqdm, build_path as bp

import os
import shutil
import subprocess

def setup(is_mac_os=False):
    print(f"Found mikhail installation in '{BASE_DIR}'. Setting up...")

    if os.path.exists(VENV): 
        print(f"Found virtual environment already setup in '{VENV}'. Reinstalling...")
        shutil.rmtree(VENV)

    create_venv(is_mac_os)

    print(f"\nSuccessfully setup in '{BASE_DIR}'. Mikhail is ready for use! Thanks for using mikhail!")

def create_venv(is_mac_os: bool):
    if is_mac_os:
        command = ()
    else:
        command = (
            f'python -m venv "{VENV}" && '
            f'call "{VENV}\\Scripts\\activate.bat" && '
            f'pip install -r "{BASE_DIR}\\requirements.txt" && '
            f'deactivate'
        )
    subprocess.call(command, shell=True)

