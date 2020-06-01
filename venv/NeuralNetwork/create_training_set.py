from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2 as cv
import random
import json

vid = '/Users/nick/PycharmProjects/PlayerTracker/venv/game_film/chi_stl_trimmed.mp4'

vs = cv.VideoCapture(vid)


frame_counter = 0
rand_skip = int(random.randrange(0, 500))
frame = 0
data = {}
box_counter = 0


def create_frame_id(frame_number):
    # ids in form 00000
    frame_number = str(frame_number)
    zeros_needed = 5 - len(frame_number)
    while len(frame_number) <= 5:
        frame_number = str('0' + frame_number)

    return frame_number


def num_frames_to_skip():
    # Has 5 % chance of next frame being close (20-90 frames) if not go far (10-15k) frames away
    # returns number of frames to skip.
    close = True if random.randrange(0, 100) < 8 else False  # 5% chance of the next frame being close
    if close:
        return int(random.randrange(20, 90))
    else:
        return int(random.randrange(5000, 10000))


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
        rand_skip = frame_counter + num_frames_to_skip()  # Get new frame incase we skip

        # Show the frame and draw boxes
        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF
        boxes = cv.selectROIs("Frame", frame, fromCenter=False, showCrosshair=True)
        print(boxes)

        if len(boxes) == 0:
            # We skipped this frame so we are going to dump it.
            print('No boxes detected. Moving on.')
            continue

        cv.imwrite(f'/Users/nick/PycharmProjects/PlayerTracker/venv/NeuralNetwork/training_data/images/{frame_id}.jpg', frame)
        cv.destroyAllWindows()
        print('Got boxes moving on to identification. ')

        i = 0
        for box in boxes:
            # Draw our boxes and re-display.
            (x, y, w, h) = [int(v) for v in box]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, str(i), (x, y - 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            i += 1
            cv.imshow(frame_id, frame)
            key = cv.waitKey(1) & 0xFF

        box_data = {}
        i = 0
        for i in range(0, len(boxes)-1):

            if len(box) <= 0:
                # Skip over empty boxes
                i += 1
                continue

            print(f'BOX {i}')
            invalid = True
            skip = False
            undo = False
            while invalid:
                b_type = input('Player type (p/g/r/e/u): ')
                if b_type == 'p':
                    object_type = 'player'
                    invalid = False
                elif b_type == 'g':
                    object_type = 'goalie'
                    invalid = False
                elif b_type == 'r':
                    object_type = 'ref'
                    invalid = False
                elif b_type == 'e':
                    skip = True
                    invalid = False
                elif b_type == 'u':
                    undo = True
                    invalid = False
                else:
                    object_type = 'Error'

            if skip:
                continue
            if undo:
                i -= 2
                try:
                    del box_data[i]
                    print(f'Deleted box_data[{i}]')
                except KeyError:
                    print('No data found for this. Skipping back one')
                continue

            player_obscured = True if input('player obscured? ') == 'y' else False
            if player_obscured:
                obscured_by = input('Obscured by p/n/b ')
                if obscured_by == 'p':
                    obscured_by_player = True
                    obscured_by_boards = False
                    obscured_by_net = False
                elif obscured_by == 'n':
                    obscured_by_player = False
                    obscured_by_boards = False
                    obscured_by_net = True
                elif obscured_by == 'b':
                    obscured_by_player = False
                    obscured_by_boards = True
                    obscured_by_net = False
                else:
                    obscured_by_player = False
                    obscured_by_boards = False
                    obscured_by_net = False
            else:
                obscured_by_boards = False
                obscured_by_player = False
                obscured_by_net = False

            difficult = True if input('difficult? ') == 'y' else False
            print('\n')
            (x, y, w, h) = [int(v) for v in boxes[i]]

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

        data['boxes'] = box_data

        with open(f'/Users/nick/PycharmProjects/PlayerTracker/venv/NeuralNetwork/training_data/image_data/{frame_id}.json', 'w') as fp:
            json.dump(data, fp, indent=4)

        print(f'Saved {frame_id}.json. Moving on.')
        box_counter += len(boxes)
        cv.destroyAllWindows()


print(frame_counter)
print(f'Found {box_counter}.')
