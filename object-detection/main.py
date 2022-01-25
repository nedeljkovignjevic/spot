import numpy as np
import torch
import cv2
import time
from model import NvidiaModel


def main():
    # model = torch.hub.load('ultralytics/yolov5', 'custom', classes=2,
    #                        path='yolov5/runs/train/exp15/weights/last.pt',
    #                        force_reload=True)

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.classes = [9, 11]
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        print(frame.shape)

        # Make detections
        results = model(frame)

        cv2.imshow('YOLO', np.squeeze(results.render()))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # model = NvidiaModel(show_first_activation=True)
    # model.load_state_dict(torch.load('models/model-pool-4'))
    #
    # data = get_data()
    # data = data[:64]
    # train_loader = torch.utils.data.DataLoader(data, batch_size=32, shuffle=True)
    #
    # valid_loss = 0
    # n_valid_losses = 0
    # model.eval()
    # with torch.no_grad():
    #     for (x, y) in train_loader:
    #         input, target = x.float(), y.float()
    #
    #         output = model(input)
    #         return
    #         print(output)


if __name__ == '__main__':
    main()
