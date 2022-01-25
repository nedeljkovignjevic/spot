import cv2
import numpy as np


def save_data(data, path: str = 'data/processed.npy'):
    np.save(path, data)


def load_data(path: str):
    return np.load(path)


def get_training_data():
    data = []

    with open("data/steering/steering.csv") as file:
        for steering in file:
            if steering != '' and steering != '\n':
                id = steering.split(",")[0]

                frame = cv2.imread(f"data/images/all/frame-{str(id)}.jpg")
                data.append([frame, float(steering.split(",")[1])])

    save_data(data)
