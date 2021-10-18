import os
import pathlib
from wave import Error
from pydub import AudioSegment
from scipy.io.wavfile import read
import logging

audio_formats = ['.mp3', '.flac', '.ogg', '.m4a', '.aiff']

def index_and_rename(directory):
    format_check(directory)
    file_index = 0
    for filepath in pathlib.Path(directory).glob('**/*'):
        if os.path.isfile:
            destination = f'{directory}/{str(file_index)}.wav'
            os.rename(filepath, destination)
            file_index += 1
        else:
            pass

def format_check(path):
    for filepath in pathlib.Path(path).glob('**/*'):
            if os.path.isfile(filepath):
                if filepath.suffix in audio_formats:
                    audio_to_wav(filepath)
                elif filepath.suffix == '.wav':
                    pass
                else:
                    os.rename(filepath, f'{filepath.parents[1]}/unrecognised_audio/{filepath.stem}{filepath.suffix}')
                    logging.warning(f'{filepath} extension is not an audio format. Moving to /unrecognised.')
            else:
                pass

def audio_to_wav(filepath):
        audio_to_wav = AudioSegment.from_file(filepath) 
        audio_to_wav.export(f'{filepath.parent}/{filepath.stem}.wav', format="wav")
        os.remove(filepath)
        


if __name__ == '__main__':
    path = "/home/maks/Desktop/Dev/Datasets processing/audio"
    index_and_rename(path)