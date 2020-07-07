import os

import numpy as np
from tensorflow.keras.utils import to_categorical
import yaml


def load_training_conf(conf_path=None):
    conf_path = conf_path or os.path.join("src", "train_conf.yml")
    with open(conf_path, "r") as file:
        conf = yaml.full_load(file)
    return conf


def encode_texts(tokenizer, texts):
    return np.array(
        [
            tokenizer.encode(
                text,
                max_length=tokenizer.max_length,
                pad_to_max_length=tokenizer.pad_to_max_length,
            )
            for text in texts
        ]
    )


def encode_labels(texts_labels, unique_labels):
    unique_labels = sorted(unique_labels)
    # if labels are strings convert to ints before one-hot encoding
    if isinstance(unique_labels[0], str):
        label_int = dict((label, i) for (i, label) in enumerate(unique_labels))
        texts_labels_encoded = np.array([label_int[label] for label in texts_labels])
    else:
        texts_labels_encoded = np.array(texts_labels)
    return to_categorical(texts_labels_encoded, num_classes=max(unique_labels) + 1)


def pip_packages():
    with open("requirements.txt") as f:
        pip_packages = "".join(f.readlines()).split(os.linesep)
    # remove blank lines in requirements.txt
    return [x for x in pip_packages if x != '']