from storage.transcript_storage_manager import TranscriptStorageManager, Transcript
from utils.utils import build_path as bp
from config.config import LOCAL_DIR

def find(directory: str, word: str):

    print(f"finding word '{word}' in directory '{directory}'") 

    # load transcript
    transcript = TranscriptStorageManager.load(bp(directory, LOCAL_DIR, '.transcript', 'dir.transcript'))

    print(transcript.to_string())

