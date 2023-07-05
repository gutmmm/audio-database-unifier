import os
import random
import numpy as np
import shutil
from pathlib import Path
from pydub import AudioSegment
from scipy.io.wavfile import read, write

def split():
    prep_dir()
    
    for file in os.listdir('AudioExport'):
        if Path(file).suffix == '.wav':
            fs, audio = read(os.path.join('AudioExport', file))
            slice_duration = 4 #in seconds
            slice_length = fs * slice_duration
            get_chunks(file, fs, audio, slice_length)

def prep_dir():
    if "chunks" in os.listdir('AudioExport'):
        shutil.rmtree('AudioExport/chunks')
        os.mkdir('AudioExport/chunks')
    else:
        os.mkdir('AudioExport/chunks')

def get_chunks(file, fs, audio, slice_length):
    audio = audio[:len(audio) - len(audio)%slice_length]
    chunks = [audio[slice_length*idx : slice_length*(idx + 1)] for idx in range(6)]
    for idx, chunk in enumerate(chunks):
        print(len(chunk))
        write(f'AudioExport/chunks/{idx}_{file}', fs, chunk)