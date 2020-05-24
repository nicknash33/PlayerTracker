from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2 as cv
import random
import json

vid = '/Users/nick/PycharmProjects/PlayerTracker/venv/game_film/trimmed_cbj_van.mp4'

vs = cv.VideoCapture(vid)

frame_counter = 0
rand_skip = int(random.randrange(0, 500))
frame = 0
data = {}


def create_frame_id(frame_number):
    # ids in form 00000
    frame_number = str(frame_number)
    zeros_needed = 5 - len(frame_number)
    while len(frame_number) <= 5:
        frame_number = str('0' + frame_number)

    return frame_number


while True:
    frame = vs.read()
    frame = frame[1]
    if frame is None:
        break
    frame_counter += 1

    if frame_counter >= rand_skip:
        frame_data = {}
        boxes = []
        frame = imutils.resize(frame, width=800)

        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF

        boxes = cv.selectROIs("Frame", frame, fromCenter=False, showCrosshair=True)

        rand_skip = frame_counter + int(random.randrange(2000, 3000))
        print(boxes)
        i = 0
        for box in boxes:
            (x, y, w, h) = [int(v) for v in box]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, str(i), (x, y - 15), cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            cv.imshow("Frame", frame)
            key = cv.waitKey(1) & 0xFF
            i += 1

        box_data = {}
        i = 0
        for box in boxes:
            print(f'BOX {i}')
            b_type = input('Plyer type (p/g/r): ')
            if b_type == 'p':
                object_type = 'player'
            elif b_type == 'g':
                object_type = 'goalie'
            elif b_type == 'r':
                object_type = 'ref'
            else:
                object_type = 'Error'

            player_obscured = True if input('player obscured? ') == 'y' else False
            if player_obscured:
                obscured_by_boards = True if input('player obscured by boards? ') == 'y' else False
                obscured_by_player = True if input('player obscured by player? ') == 'y' else False
                obscured_by_net = True if input('player obscured by net? ') == 'y' else False
            else:
                obscured_by_boards = False
                obscured_by_player = False
                obscured_by_net = False

            difficult = True if input('difficult? ') == 'y' else False
            print('/n')
            (x, y, w, h) = [int(v) for v in box]

            box_data[i] = {
                'loc': {
                    'x': x,
                    'y': y,
                    'w': w,
                    'h': h
                },
                'type': object_type,
                'obscured': [player_obscured, {'boards': obscured_by_boards,
                                               'player': obscured_by_player,
                                               'net': obscured_by_net}
                             ]
            }
            i += 1

        frame_id = create_frame_id(frame_counter)
        data[frame_id] = {'frame': frame.tolist(),
                          'boxes': box_data
                          }

with open('data.json', 'w') as fp:
    json.dump(data, fp)

print(frame_counter)
