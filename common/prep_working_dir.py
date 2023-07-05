import os

import shutil
import logging
from pathlib import Path


class prepareDir():
    def __init__(self, audio_origin, audio_formats):
        self.audio_origin = audio_origin
        self.audio_formats = audio_formats

    def create(self):
        if "AudioExport" in os.listdir(os.getcwd()):
            shutil.rmtree('AudioExport')
            os.mkdir('AudioExport')
        else:
            os.mkdir('AudioExport')
        self.copy_audio()

    def copy_audio(self):
        for file in os.listdir(self.audio_origin):
            if Path(file).suffix in self.audio_formats:
                shutil.copy(os.path.join(self.audio_origin, file), 'AudioExport')