from scipy.io.wavfile import read
from pathlib import Path
import wave
import os 


directory = '/home/maks/Desktop/Dev/Datasets processing/AudioDataset/audio'

audio_paths = [audio for audio in Path(directory).glob('**/*')]
audio_files = [read(audio) for audio in audio_paths]
audio_names = [name for name in os.listdir(directory)]

print(audio_files[0][1].dtype)

def get_dtype(audio_files):
    for element in audio_files:
        print(element[1].dtype)

def get_sample_rate(audio_files):
    return [sr[0] for sr in audio_files]

def num_of_channels(audio_paths):
    for element in audio_paths:
        print(element.stem)
        obj = wave.open(str(element),'r')
        print(obj)


#sample_rates = get_sample_rate(audio_files)
#num_of_channels(audio_paths)
get_dtype(audio_files)
