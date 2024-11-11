import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

class Player:
    player_instance = None

    @classmethod
    def get(cls):
        if cls.player_instance == None:
            cls.player_instance = Player()
        return cls.player_instance

    def __init__(self) -> None:
        mixer.init()

    def play(self, audio, volume=0.3):
        sound = mixer.Sound(audio)
        sound.set_volume(volume)
        sound.play()


