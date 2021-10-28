import os
import time
import shutil


source = '/home/maks/Desktop/Dev/AudioDataset'
destination = '/home/maks/Desktop/Dev/Datasets processing/AudioDataset'


try:
    shutil.rmtree('/home/maks/Desktop/Dev/Datasets processing/AudioDataset')
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))


shutil.copytree(source, destination)
