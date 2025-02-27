import os
import pathlib

import keras.src.utils.audio_dataset_utils
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf

seed = 42

tf.random.set_seed(seed)
np.random.seed(seed)

# keras API
from keras import layers, models

"""just a small change"""

def speech_to_text():
    DATASET_PATH = 'data/mini_speech_command'
    data_dir = pathlib.Path(DATASET_PATH)
    if not data_dir.exists():
        keras.utils.get_file(
            'mini_speech_commands.zip',
            origin="http://storage.googleapis.com/download.tensorflow.org/data/mini_speech_commands.zip",
            extract=True,
            cache_dir='.', cache_subdir='data')

    return


def text_summarizer():
    return


def speech_to_text_model(train_spectrogram_ds=None, num_labels=None):
    norm_layer = layers.Normalization()
    norm_layer.adapt(data=train_spectrogram_ds.map(map_func=lambda spec, label: spec))
    model = models.Sequential([
        layers.Input(shape=[124, 129, 1]),
        # Downsample the input.
        layers.Resizing(32, 32),
        # Normalize.
        norm_layer,
        layers.Conv2D(32, 3, activation='relu'),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_labels),
    ])

    model.summary()
    return


speech_to_text_model()
