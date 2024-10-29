from utils.utils import build_path as bp

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
LOCAL_DIR = 'mikhail'

ALLOWED_FORMATS = ['mp3', 'm4a']
MAX_AUDIO_FILESIZE = 20 * 1024 * 1024

# clean
ASK_CONFIRMATION = True

# model
MODELS_DIR = bp(BASE_DIR, 'models')
MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_PATH = bp(MODELS_DIR, MODEL_NAME)

# audio converter
CONVERSION_CACHE_LOCATION = f"{BASE_DIR}/temp/conversion"
CLEAR_CONVERSION_CACHE = True
