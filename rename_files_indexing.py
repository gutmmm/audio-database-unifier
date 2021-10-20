import os
import pathlib
from wave import Error
from pydub import AudioSegment
from scipy.io.wavfile import read
import logging

audio_formats = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aiff']


def process(dir):
    audio_dir = f'{dir}/audio'
    if not os.path.exists(audio_dir):
        logging.error("Directory does not contain an 'audio' folder. Check provided path.")
        exit()
    elif not os.path.exists(f'{dir}/unrecognised_files'):
        logging.warning('Path for unrecognised files not found. Folder will be created')
        os.mkdir(f'{dir}/unrecognised_files')
    move_unrecognised(audio_dir)

def move_unrecognised(audio_dir):
    for filepath in pathlib.Path(audio_dir).glob('**/*'):
            if filepath.suffix not in audio_formats:
                destination = f'{filepath.parents[1]}/unrecognised_files/{filepath.stem}{filepath.suffix}'
                os.rename(filepath, destination)
    format_check(audio_dir)

def format_check(audio_dir):
    for filepath in pathlib.Path(audio_dir).glob('**/*'):
                if filepath.suffix in audio_formats and filepath.suffix != '.wav':
                    audio_to_wav(filepath)
    rename_by_index(audio_dir)

def rename_by_index(audio_dir):
    file_index = 0
    for filepath in pathlib.Path(audio_dir).glob('**/*'):
        if os.path.isfile(filepath):
            destination = f'{audio_dir}/{str(file_index)}.wav'
            os.rename(filepath, destination)
            file_index += 1

def audio_to_wav(filepath):
        audio_to_wav = AudioSegment.from_file(filepath) 
        audio_to_wav.export(f'{filepath.parent}/{filepath.stem}.wav', format="wav")
        os.remove(filepath)


if __name__ == '__main__':
    path = "/home/maks/Desktop/Dev/Datasets processing/AudioDataset"
    process(path)