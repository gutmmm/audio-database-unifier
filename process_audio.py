from scipy.io.wavfile import write
from scipy.io.wavfile import read
from pydub import AudioSegment
from pathlib import Path
import pandas as pd
import numpy as np
import wave
import os 

from conversion import convert_float_to_int, convert_int_to_int

directory = '/home/maks/Desktop/Dev/Datasets processing/AudioDataset/audio'

pd.set_option('display.max_colwidth', 30)

def get_audio_stats():
    audio_paths = [audio for audio in Path(directory).glob('**/*')]
    audio_names = [name for name in os.listdir(directory)]
    audio_files = [read(audio) for audio in audio_paths]
    audio_samplerate = [data[0] for data in audio_files]
    audio_samples = [data[1] for data in audio_files]
    audio_dtype = [str(datatype[1].dtype) for datatype in audio_files]
    audio_nchannels = [len(numchannels.shape) for numchannels in audio_samples]

    audio_df = pd.DataFrame({'audio name':audio_names, 
                            'audio path':audio_paths,
                            'audio samplerate':audio_samplerate,
                            'audio samples': audio_samples,
                            'audio dtype':audio_dtype,
                            'num of channels':audio_nchannels})

    print(audio_df)
    return audio_df


def file_to_int16(audio_df):
    for idx, element in enumerate(audio_df['audio dtype']):
        if 'float' in element:
            flt_to_int16 = convert_float_to_int(audio_df.loc[idx]['audio samples'])
            write_to_wav(audio_df, idx, flt_to_int16)
        elif 'int16' not in element:
            int_to_int16 = convert_int_to_int(audio_df.loc[idx]['audio samples'])
            write_to_wav(audio_df, idx, int_to_int16)
            
def write_to_wav(audio_df, idx, data):
    destination = audio_df.loc[idx]['audio path']
    write(filename=destination,
          rate=audio_df.loc[idx]['audio samplerate'],
          data=data)

def unify_samplerate(audio_df):
    default_sr = 44100
    for idx, element in enumerate(audio_df['audio samplerate']):
        if element != default_sr:
            sound = AudioSegment.from_file(audio_df['audio path'][idx], 
                                           format='wav', 
                                           frame_rate=audio_df['audio samplerate'][idx])
            sound = sound.set_frame_rate(default_sr)
            sound.export(audio_df['audio path'][idx], format='wav')

def split_channels(audio_df):
    default_num_channels = 1
    name_suffix = ['L','P']
    parent_dir = audio_df.loc[0]['audio path'].parent
    for idx, element in enumerate(audio_df['num of channels']):
        if element != default_num_channels:
            L, R = create_filenames(audio_df, parent_dir, idx)
            stereo_file = AudioSegment.from_file(audio_df.loc[idx]['audio path'])
            mono_files = stereo_file.split_to_mono()
            mono_files[0].export(L, format='wav')
            mono_files[1].export(R, format='wav')
            os.remove(Path(audio_df.loc[idx]['audio path']))

def create_filenames(audio_df, parent_dir, idx):
    filename = audio_df.loc[idx]['audio path'].stem
    mono_left = f'{parent_dir}/{filename}L.wav'
    mono_right = f'{parent_dir}/{filename}R.wav'
    return mono_left, mono_right

audio_stats = get_audio_stats()
file_to_int16(audio_stats)
unify_samplerate(audio_stats)
split_channels(audio_stats)
audio_stats = get_audio_stats()
