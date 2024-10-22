from storage.transcript import Transcript

class FileManager:
    def __init__(self):
        pass 

    def save(self, directory, transcript: Transcript):
        print(f"saving transcript from directory '{directory}' with {len(transcript.words)} words, transcribed by model {transcript.model} on {transcript.timestamp} ")
        print(transcript.to_string())