import torch
import numpy as np
import cv2
import time

def main():

    # model = torch.hub.load('ultralytics/yolov5', 'yolov5n6')
    cap = cv2.VideoCapture("http://spot:71@192.168.4.2:9999/video")
    start = time.time()
    kurcina = 0
    while cap.isOpened():
        ret, frame = cap.read()

        # Make detections
        # results = model(frame)
        kurcina += 1
        cv2.imshow('YOLO', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    end = time.time() - start
    print(end)
    print(kurcina)


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
