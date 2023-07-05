# Audio Dataset Unifier

Convienient scipt for processing large audio dataset for a time series forecasting experiments.

Features of `process_database.py`
* Unify sampling rate across whole audio dataset
* Unify data format to `int16`
* Unify audio format to `.wav`
* Split stereo audio files to single channels (kind of data augmentation)
* Rename whole dataset to index based namespace

Additionally `split_audio.py` can help in splitting every file in dataset for specified time duration audio chunks.
That should help in feeding such dataset in some neural networks.

