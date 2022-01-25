import time

from websocket import create_connection

drive_url = "ws://192.168.4.1:81/drive"

ws = create_connection(drive_url)


def send_value(steer: float, speed=0.52):
    msg = "C{:.2f}|{:.2f}".format(speed, steer)
    print(msg)
    ws.send(msg)


def _line(delay):
    send_value(0)
    time.sleep(delay)
    send_value(0, 0)


def long_line():
    _line(2.3)


def short_line():
    _line(1.2)


def ultra_short_line():
    _line(0.3)


def back_on_track():
    for i in range(11):
        send_value(0.8 + i * 0.02)
        time.sleep(0.04)
    for i in range(11):
        send_value(1.0 - i * 0.02)
        time.sleep(0.02)
    # for i in range(11):
    #     send_value(-0.5 - i * 0.02)
    #     time.sleep(0.02)
    send_value(0, 0)


def back_on_track_left():
    for i in range(11):
        send_value(-0.8 - i * 0.02)
        time.sleep(0.04)
    for i in range(11):
        send_value(-1.0 + i * 0.02)
        time.sleep(0.02)
    # for i in range(11):
    #     send_value(0.5 + i * 0.02)
    #     time.sleep(0.02)
    send_value(0, 0)


def turn_left_start():
    for i in range(11):
        send_value(-0.5 - i * 0.05)
        time.sleep(i * 0.032)
    time.sleep(1.0)
    for i in range(11):
        send_value(-1.0 + i * 0.05)
        time.sleep(0.025)
    send_value(0, 0)


def turn_left_ds():
    for i in range(11):
        send_value(-0.5 - i * 0.05)
        time.sleep(i * 0.015)
    time.sleep(0.8)
    for i in range(11):
        send_value(-1.0 + i * 0.05)
        time.sleep(0.20)
    send_value(0, 0)


def turn_left2():
    for i in range(6):
        send_value(-0.5 - i * 0.1)
        time.sleep(i * 0.15)
    time.sleep(0.8)
    for i in range(6):
        send_value(-1.0 + i * 0.1)
        time.sleep(i * 0.15)
    send_value(0, 0)


def drive():
    # back_on_track()
    # back_on_track_left()
    # long_line()
    # turn_left_ds()
    short_line()
    # turn_left_ds()
    # long_line()
    # turn_left()
    # ultra_short_line()
    # long_line()


if __name__ == '__main__':
    drive()
