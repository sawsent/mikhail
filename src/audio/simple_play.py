from pydub import AudioSegment
from pydub.playback import play

def play_test_sound():
    song = AudioSegment.from_wav("C:\\Users\\vicente\\Desktop\\mikhail\\test\\test.wav")
    play(song)
