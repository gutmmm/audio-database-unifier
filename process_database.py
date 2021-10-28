import os
import logging
from tqdm import tqdm
from wave import Error
from pathlib import Path
from pydub import AudioSegment
from scipy.io.wavfile import read

import unify_audio, split_audio

audio_formats = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aiff']
audio_requirement = {'sample rate':44100,
                     'audio dtype':'int16',
                     'num of chanels':1}


def check_directory(dir_parent, audio_dir):
    if not os.path.exists(audio_dir):
        logging.error("Directory does not contain an 'audio' folder. Check provided path.")
        exit()
    elif not os.path.exists(f'{dir_parent}/unrecognised_files'):
        logging.warning('Path for unrecognised files not found. Folder will be created')
        os.mkdir(f'{dir_parent}/unrecognised_files')

    move_unrecognised(audio_dir)

def move_unrecognised(audio_dir):
    for filepath in Path(audio_dir).glob('**/*'):
            if filepath.suffix not in audio_formats:
                destination = f'{filepath.parents[1]}/unrecognised_files/{filepath.stem}{filepath.suffix}'
                os.rename(filepath, destination)

def rename_by_index(audio_df, audio_dir):
    file_index = 0
    for filepath in Path(audio_dir).glob('**/*'):
        if os.path.isfile(filepath):
            destination = f'{audio_dir}/{str(file_index)}.wav'
            os.rename(filepath, destination)
            file_index += 1
    check_wavs(audio_dir)
      
def check_wavs(audio_dir):
    audio_paths = [audio for audio in Path(audio_dir).glob('**/*')]
    try:
        audio_files = [read(audio) for audio in audio_paths]
    except:
        raise Exception("Error when loading audio file")

def main():
    directory = "/home/maks/Desktop/Dev/Datasets processing/AudioDataset"
    audio_dir = f'{directory}/audio'
    check_directory(directory, audio_dir)
    unify_audio.process_audiofiles(audio_formats, audio_dir)
    check_wavs(audio_dir)
    audio_df = unify_audio.get_stats(audio_dir)
    print(audio_df)
    rename_by_index(audio_df, audio_dir)
    #split_audio.split(audio_df)

if __name__ == '__main__':
    main()