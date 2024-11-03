from config.config import *
from utils.utils import build_path as bp

import os
import shutil
import subprocess

def setup(is_mac_os=False):
    print(f"Found mikhail installation in '{BASE_DIR}'. Setting up...")

    if os.path.exists(VENV): 
        print(f"Found virtual environment already setup in '{VENV}'. Reinstalling...")
        shutil.rmtree(VENV)

    create_venv(is_mac_os)
    
    print(f"Installing dependencies in {VENV}...")
    install_requirements(is_mac_os)

    no_model = len([d for d in os.listdir(bp(BASE_DIR, 'models')) if os.path.isdir(bp(BASE_DIR, 'models', d))]) == 0

    print(f"\n[WARNING] No models found. Please download a model from 'https://alphacephei.com/vosk/models' and unzip it into '{bp(BASE_DIR, 'models')}'" if no_model else '\n')

    print(f"Successful setup in '{BASE_DIR}'. {'Make sure you download a model before transcribing!' if no_model else ''} Mikhail is ready for use! Thanks for using mikhail!")

def create_venv(is_mac_os: bool):
    if is_mac_os:
        command = f'python3 -m venv "{VENV}"'

    else:
        command = f'python -m venv "{VENV}"'
        

    subprocess.call(command, shell=True)

def install_requirements(is_mac_os: bool):
    if is_mac_os:
        command = f"""
source "{VENV}/bin/activate" && \
pip install -r "{BASE_DIR}/requirements.txt" 2>/dev/null && \
deactivate
""" 

    else:
        command = (
            f'call "{VENV}\\Scripts\\activate.bat" && '
            f'pip install -r "{BASE_DIR}\\requirements.txt" 2>nul && '
            f'deactivate'
        )

    subprocess.call(command, shell=True)
