import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.layers import LayerNormalization
from tensorflow.keras.models import load_model


def get_anomaly_model():
    MODEL_PATH = "weights/anomaly_model.hdf5"
    return load_model(MODEL_PATH, custom_objects={'LayerNormalization': LayerNormalization})


def get_single_test(images_path):
    sz = 200
    test = np.zeros(shape=(sz, 256, 256, 1))
    cnt = 0
    for f in sorted(os.listdir(images_path)):
        if str(os.path.join(images_path, f))[-3:] == "jpg":
            img = Image.open(os.path.join(images_path, f)).convert('L').resize((256, 256))
            img = np.array(img, dtype=np.float32) / 256.0
            test[cnt, :, :, 0] = img
            cnt = cnt + 1
    return test


def evaluate(model, images_path):
    test = get_single_test(images_path)
    sz = test.shape[0] - 10 + 1
    sequences = np.zeros((sz, 10, 256, 256, 1))

    for i in range(0, sz):
        clip = np.zeros((10, 256, 256, 1))
        for j in range(0, 10):
            clip[j] = test[i + j, :, :, :]
        sequences[i] = clip

    reconstructed_sequences = model.predict(sequences, batch_size=4)
    sequences_reconstruction_cost = np.array([np.linalg.norm(np.subtract(sequences[i],
                                                                         reconstructed_sequences[i])) for i in range(0, sz)])
    sa = (sequences_reconstruction_cost - np.min(sequences_reconstruction_cost)) / np.max(sequences_reconstruction_cost)
    sr = 1.0 - sa

    plt.plot(sr)
    plt.ylabel('regularity score Sr(t)')
    plt.xlabel('frame t')
    #plt.savefig('source/saved_figure.png')
