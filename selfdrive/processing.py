import cv2
import numpy as np


def save_data(data, path: str = 'data/processed.npy'):
    np.save(path, data)


def load_data(path: str):
    return np.load(path)


def get_training_data():
    data = []

    # get all images
    # img_base = 'data/images/all/'
    # if not exists(img_base):
    #     os.mkdir(img_base)
    # for root, dirs, files in os.walk('data/images', topdown=True):
    #     for file in files:
    #         path = root + "/" + file
    #         if not exists(img_base + file):
    #             copyfile(path, img_base + file)
    #
    # # merge csv files
    # csv_base = 'data/steering/'
    # if not exists(csv_base):
    #     os.mkdir(csv_base)
    # with open(csv_base + 'steering.csv', mode='w+') as out:
    #
    #     for root, dirs, files in os.walk('data/steering', topdown=True):
    #         for file in files:
    #             path = root + "/" + file
    #             with open(path) as infile:
    #                 out.write(infile.read())
    #                 out.write("\n")

    with open("data/steering/steering.csv") as file:
        for steering in file:
            if steering != '' and steering != '\n':
                id = steering.split(",")[0]

                frame = cv2.imread(f"data/images/all/frame-{str(id)}.jpg")
                data.append([frame, float(steering.split(",")[1])])

    save_data(data)
