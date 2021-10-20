import os
import pathlib
from wave import Error
from pydub import AudioSegment
from scipy.io.wavfile import read
import logging

audio_formats = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aiff']

def index_and_rename(database_directory):
    audiofiles_dir = f'{database_directory}/audio'

    check_directories(database_directory)
    move_unrecognised(audiofiles_dir)
    format_check(audiofiles_dir)
    rename_by_index(audiofiles_dir)

def format_check(path):
    for filepath in pathlib.Path(path).glob('**/*'):
                if filepath.suffix in audio_formats and filepath.suffix != '.wav':
                    audio_to_wav(filepath)

def audio_to_wav(filepath):
        audio_to_wav = AudioSegment.from_file(filepath) 
        audio_to_wav.export(f'{filepath.parent}/{filepath.stem}.wav', format="wav")
        os.remove(filepath)

def check_directories(directory):
    if not os.path.exists(f'{directory}/audio'):
        logging.error("Directory does not contain an 'audio' folder. Check provided path.")
        exit()
    elif not os.path.exists(f'{directory}/unrecognised_files'):
        logging.warning('Path for unrecognised files not found. Folder will be created')
        os.mkdir(f'{directory}/unrecognised_files')

def move_unrecognised(dir):
    for filepath in pathlib.Path(dir).glob('**/*'):
            if filepath.suffix not in audio_formats:
                destination = f'{filepath.parents[1]}/unrecognised_files/{filepath.stem}{filepath.suffix}'
                os.rename(filepath, destination)

def rename_by_index(dir):
    file_index = 0
    for filepath in pathlib.Path(dir).glob('**/*'):
        if os.path.isfile(filepath):
            
            destination = f'{dir}/{str(file_index)}.wav'
            os.rename(filepath, destination)
            file_index += 1


if __name__ == '__main__':
    path = "/home/maks/Desktop/Dev/Datasets processing/AudioDataset"
    index_and_rename(path)