from scipy.io.wavfile import write
from scipy.io.wavfile import read
from pydub import AudioSegment
from pathlib import Path
import pandas as pd
import numpy as np
import wave
import os 

from common.conversion import convert_float_to_int, convert_int_to_int

pd.set_option('display.max_colwidth', 20)




class audioUnify():
    """Processing class for unifying format, samplerate, splitting channels etc."""
    def __init__(self, audio_formats: list, audio_dir: str, export_sample_rate: int = 44100):
        self.audio_formats = audio_formats
        self.audio_dir = audio_dir
        self.export_sample_rate = export_sample_rate

    def format_check(self):
        """Check audio file format if .wav"""
        for filepath in Path(self.audio_dir).glob('**/*'):
            if filepath.suffix in self.audio_formats and filepath.suffix != '.wav':
                self.audio_to_wav(filepath)
                

    def audio_to_wav(self, filepath: str):
        """Converter from any audio format to .wav"""
        audio_to_wav = AudioSegment.from_file(filepath)
        audio_to_wav.export(f'{filepath.parent}/{filepath.stem}.wav', format="wav")
        os.remove(filepath)

    def get_stats(self):
        """Collect audio information"""
        audio_paths = [audio for audio in Path(self.audio_dir).glob('**/*')]
        audio_names = [name for name in os.listdir(self.audio_dir)]
        audio_files = [read(audio) for audio in audio_paths]
        audio_samplerate = [data[0] for data in audio_files]
        audio_samples = [data[1] for data in audio_files]
        audio_dtype = [str(datatype[1].dtype) for datatype in audio_files]
        audio_nchannels = [len(numchannels.shape) for numchannels in audio_samples]

        self.audio_df = pd.DataFrame({
            'audio name': audio_names, 
            'audio path': audio_paths,
            'audio samplerate': audio_samplerate,
            'audio samples': audio_samples,
            'audio dtype': audio_dtype,
            'num of channels': audio_nchannels
            })

    def file_to_int16(self):
        """Convert audio to Int16"""
        for idx, element in enumerate(self.audio_df['audio dtype']):
            if 'float' in element:
                flt_to_int16 = convert_float_to_int(self.audio_df.loc[idx]['audio samples'])
                self.write_to_wav(idx, flt_to_int16)
            elif 'int16' not in element:
                int_to_int16 = convert_int_to_int(self.audio_df.loc[idx]['audio samples'])
                self.write_to_wav(idx, int_to_int16)

    def write_to_wav(self, idx, data):
        """Export to .wav w.r.t dataframe"""
        destination = self.audio_df.loc[idx]['audio path']
        write(filename=destination, rate=self.audio_df.loc[idx]['audio samplerate'], data=data)

    def unify_samplerate(self):
        """Export audio in unified samplerate"""
        for idx, element in enumerate(self.audio_df['audio samplerate']):
            if element != self.export_sample_rate:
                sound = AudioSegment.from_file(
                    self.audio_df['audio path'][idx],
                    frame_rate=self.audio_df['audio samplerate'][idx],
                    format='wav'
                    )
                sound = sound.set_frame_rate(self.export_sample_rate)
                sound.export(self.audio_df['audio path'][idx], format='wav')

    def split_channels(self):
        """Split channels to separete audio files"""
        default_num_channels = 1
        parent_dir = self.audio_df.loc[0]['audio path'].parent
        for idx, element in enumerate(self.audio_df['num of channels']):
            if element != default_num_channels:
                L, R = self.create_mono_filenames(idx)
                stereo_file = AudioSegment.from_file(self.audio_df.loc[idx]['audio path'])
                mono_files = stereo_file.split_to_mono()
                mono_files[0].export(L, format='wav')
                mono_files[1].export(R, format='wav')
                os.remove(Path(self.audio_df.loc[idx]['audio path']))

    def create_mono_filenames(self, idx):
        filename = self.audio_df.loc[idx]['audio path'].stem
        mono_left = f'{self.audio_dir}/{filename}L.wav'
        mono_right = f'{self.audio_dir}/{filename}R.wav'
        return mono_left, mono_right