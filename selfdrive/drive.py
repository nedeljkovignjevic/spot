import cv2
import torch
import numpy as np
from websocket import create_connection
from model import NvidiaModel


drive_url = "ws://192.168.4.1:81/drive"

ws = create_connection(drive_url)


def send_value(steer: float, speed=0.35):
    msg = "C{:.2f}|{:.2f}".format(speed, steer)
    ws.send(msg)


def drive(cam_url: str):
    model = NvidiaModel()
    model.load_state_dict(torch.load('models/model-final-13'))

    cap = cv2.VideoCapture(cam_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    selector = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if selector == 0:
            # Make detections
            # results = yolo_model(frame)

            # get steering
            input = torch.Tensor(frame).float()
            input = input[None, :]
            steering = model(input)

            value = steering.item()
            value = max(-1, value)
            value = min(1, value)
            print(value)

            send_value(steering.item())

            cv2.imshow('spot', frame)
        selector = (selector + 1) % 3

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    drive("http://192.168.4.3:9999/video")
