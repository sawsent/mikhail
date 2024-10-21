from audio.transcript import Transcript
from audio.converter import Converter
from config.config import *

import os
import shutil
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel



class VoskTranscriber:
    def __init__(self, model_path, cache_location=CONVERSION_CACHE_LOCATION):
        SetLogLevel(-1)
        if not os.path.exists(model_path):
            raise Exception('Model not found.')
        
        self.model_path = model_path
        self.model = Model(model_path)
        self.cache_location = cache_location
        self.converter = Converter(cache_location)

        if not os.path.exists(cache_location):
            os.makedirs(cache_location)

    def transcribe(self, audio: str) -> Transcript:

        converted = self.converter.convert(audio)

        with wave.open(converted, "rb") as wf:

            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [16000, 8000]:
                print("Audio file must be WAV format with mono channel and 16kHz or 8kHz sample rate.")
                exit(1)

            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetWords(True)

            results = []
            while True:
                data = wf.readframes(4000)
                if not data:
                    break

                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    results.append(json.loads(res)) 


            results.append(json.loads(rec.FinalResult()))
        
        
        word_timestamps = []
        for result in results:
            if 'result' in result:
                for word_info in result['result']:
                    word = word_info['word']
                    start_time = word_info['start']
                    end_time = word_info['end']
                    word_timestamps.append({
                        'word': word,
                        'start': start_time,
                        'end': end_time
                    })
            
        transcript = Transcript(word_timestamps)

        return transcript

    def clean(self):

        for item in os.listdir(self.cache_location):
            item_path = os.path.join(self.cache_location, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path) 
    



    