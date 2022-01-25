from model import NvidiaModel
import torch
import cv2
import numpy as np


def main():
    model = NvidiaModel()

    model.load_state_dict(torch.load('models/model-pool-64-7'))
    model.eval()

    cap = cv2.VideoCapture("http://192.168.4.3:9999/video")
    while cap.isOpened():
        ret, frame = cap.read()

        # Make detections
        input = torch.Tensor(frame).float()
        input = input[None, :]
        output = model(input)

        print(output.item())

        cv2.imshow('YOLO', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()