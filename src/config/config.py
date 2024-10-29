from utils.utils import build_path as bp

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
LOCAL_DIR = 'mikhail'
VENV_DIR_NAME = '.venv'
VENV = bp(BASE_DIR, VENV_DIR_NAME)

ALLOWED_FORMATS = ['mp3', 'm4a']
MAX_AUDIO_FILESIZE = 20 * 1024 * 1024

# clean
ASK_CONFIRMATION = False

# model
MODELS_DIR = bp(BASE_DIR, 'models')

# audio converter
CONVERSION_CACHE_LOCATION = bp(BASE_DIR, 'temp', 'conversion')
CLEAR_CONVERSION_CACHE = True
