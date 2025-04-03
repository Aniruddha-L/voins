from Sender import main
from Access import Access
from Reciever import Reciever
from gtts import gTTS
import os
from Recorder import record
import whisper as ws

whisper = ws.load_model('small')
def stt():
    # if record():
        file_path = 'input.wav'
        result = whisper.transcribe(file_path)
        text = result['text'].strip()
        return text


def tts(text):
    s = gTTS(text, lang='en')
    s.save('output.wav')
    print('saved')
    # os.system(f'ffmpeg output.wav')

voice = stt()
sen = main(voice)

Reciever(sen)
tts(sen['task'])