from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2 as cv
import random
import json

vid = '/Users/nick/PycharmProjects/PlayerTracker/venv/game_film/trimmed_cbj_van.mp4'

vs = cv.VideoCapture(vid)
writer = None

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
    (success, frame) = vs.read()
    #frame = frame[1]
    if frame is None:
        break
    frame_counter += 1

    if frame_counter >= rand_skip:
        frame_data = {}
        boxes = []
        frame = imutils.resize(frame, width=800)
        frame_id = create_frame_id(frame_counter)
        rand_skip = frame_counter + int(random.randrange(2000, 3000))  # Get new frame incase we skip

        # Show the frame and draw boxes
        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF
        boxes = cv.selectROIs("Frame", frame, fromCenter=False, showCrosshair=True)

        print(len(boxes))
        if len(boxes) == 0:
            # We skipped this frame so we are going to dump it.
            continue

        cv.imwrite(f'/Users/nick/PycharmProjects/PlayerTracker/venv/training_data/images/{frame_id}.jpg', frame)
        cv.destroyAllWindows()

        i = 0
        for box in boxes:
            # Draw our boxes and re-display.
            (x, y, w, h) = [int(v) for v in box]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, str(i), (x, y - 15), cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            i += 1
            cv.imshow("Frame", frame)
            key = cv.waitKey(1) & 0xFF

        box_data = {}
        i = 0
        for box in boxes:

            if len(box) <= 0:
                # Skip over empty boxes
                i += 1
                continue

            print(f'BOX {i}')
            invalid = True
            while invalid:
                b_type = input('Player type (p/g/r): ')
                if b_type == 'p':
                    object_type = 'player'
                    invalid = False
                elif b_type == 'g':
                    object_type = 'goalie'
                    invalid = False
                elif b_type == 'r':
                    object_type = 'ref'
                    invalid = False
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
            print('\n')
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

        data['frame_id'] = {
                          'boxes': box_data
                          }

        with open(f'/Users/nick/PycharmProjects/PlayerTracker/venv/training_data/image_data/{frame_id}.json', 'w') as fp:
            json.dump(data, fp, indent=4)

print(frame_counter)
