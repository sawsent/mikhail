from config.config import *

import ffmpeg
import os

class Converter:
    def __init__(self, cache_location, loglevel='quiet'):
        self.cache_location = cache_location
        self.loglevel = loglevel

    def convert(self, input_file: str):
        output_file = f"{self.cache_location}/{''.join(input_file.split('/')[-1].split('.')[:-1])}.wav"
      
        try:
            (
                ffmpeg
                .input(input_file)
                .output(output_file, format='wav', acodec='pcm_s16le', ac=1, ar='16000', loglevel=self.loglevel)  
                .run(overwrite_output=True)  
            )
            
        except ffmpeg.Error as e:
            print(f"Error occurred during conversion: {e.stderr.decode('utf-8')}")  # Decode error message(
                
        return output_file
