import time
import threading
import simulator

import os
import cv2
import csv

from websocket import create_connection

info_url = "ws://192.168.4.1:80/info"

ws = create_connection(info_url)

session_id = 'straight-in'
no = 20

if not os.path.exists(f"data/images/{session_id}"):
    os.makedirs(f"data/images/{session_id}")

if not os.path.exists(f"data/steering/{session_id}"):
    os.makedirs(f"data/steering/{session_id}")

os.mkdir(f"data/images/{session_id}/{session_id}-{no}")


def save_data(frame, steering, counter):
    # timestamp = round(time.time())

    cv2.imwrite(f"data/images/{session_id}/{session_id}-{no}/frame-{session_id}-{no}-{str(counter)}.jpg", frame)

    with open(f"data/steering/{session_id}/{session_id}-{no}.csv", "a", newline="") as file:
        fieldnames = ['id', 'steering']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'id': str(f"{session_id}-{no}") + "-" + str(counter), 'steering': steering})


def get_current_steering_value():
    ws.send("info")
    steering = ws.recv()
    return steering


def collect():
    cap = cv2.VideoCapture("http://192.168.4.3:9999/video")
    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    start = time.time()

    frame_counter = 0
    request_data = 0
    request_counter = 0

    while cap.isOpened():
        ret, frame = cap.read()

        frame_counter += 1

        # get SPOT's steer value
        if request_data == 1:
            steering = get_current_steering_value()
            # steering = round(random.randrange(-200, 200, 1) / 10000, 2)
            print(f"Steer: {steering}")
            request_counter += 1

            # save data to files
            threading.Thread(target=save_data, args=(frame, steering, frame_counter,), daemon=True).start()

        request_data = (request_data + 1) % 3

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    total_time = time.time() - start
    print("total time: {}".format(total_time))
    print("number of frames: {}".format(frame_counter))
    print("fps: {}".format(frame_counter / total_time))
    print("rqs: {}".format(request_counter / total_time))

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    threading.Thread(target=collect, daemon=True).start()
    time.sleep(0.5)
    threading.Thread(target=simulator.drive).start()

