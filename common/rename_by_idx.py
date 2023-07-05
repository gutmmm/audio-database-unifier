import os
from pathlib import Path

from scipy.io.wavfile import read



def rename():
    """Rename audio files by index"""
    file_index = 0
    for filepath in Path('AudioExport').glob('**/*'):
        if os.path.isfile(filepath):
            destination = f'AudioExport/{str(file_index)}.wav'
            os.rename(filepath, destination)
            file_index += 1
    check_wavs()
      
def check_wavs():
    """Check if audio files loads properly"""
    audio_paths = [audio for audio in Path('AudioExport/audio').glob('**/*')]
    try:
        [read(audio) for audio in audio_paths]
    except:
        raise Exception("Error when loading audio file")