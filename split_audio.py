import random
import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import read

def split(audio_df):
    print(audio_df)
    fs = audio_df.loc[0]['audio samplerate']
    slice_duration = 4 #in seconds
    slice_length = fs * slice_duration

    load_audio(slice_length, audio_df)

def load_audio(slice_length, audio_df):
    #for element in audio_df.loc[0]['audio path']:
        element = audio_df.loc[0]['audio path']
        _, audio_samples = read(element)
        audio_cues(slice_length, audio_samples)

def audio_cues(slice_length, audio_samples):
    audiofile_length = int(len(audio_samples))
    last_possible_sample = int(audiofile_length - slice_length)
    start_cues = [random.randint(0, last_possible_sample) for cue in range(20)]
    slice_audio(audio_samples, start_cues, slice_length)

def slice_audio(audio_samples, start_cues, slice_length):
    new_file = audio_samples[start_cues[0]:start_cues[0]+slice_length]
    print(new_file)

    #audio_slice = audio_samples[0:44100]
    #print(len(audio_slice))