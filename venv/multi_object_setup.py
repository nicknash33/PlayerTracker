from imutils.video import FPS
import numpy as np
import argparse
import imutils
import dlib
import cv2


def resize_and_recolor_frame(frame):
    frame = imutils.resize(frame, width=600)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, rgb


def get_object_detections(frame, net):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)
    net.setInput(blob)
    detections = net.forward()
    return detections, h, w


def get_detection_box_dims(detection_object, h, w):
    box = detection_object * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    return startX, startY, endX, endY


def calc_center(detection_object):
    (startX, startY, endX, endY) = get_detection_box_dims(detection_object)
    mid_x = abs(startX - endX)
    mid_y = abs(startY - endY)
    return mid_x, mid_y


def create_tracker(startX, startY, endX, endY, rgb):
    t = dlib.correlation_tracker()
    rect = dlib.rectangle(startX, startY, endX, endY)
    t.start_track(rgb, rect)
    return t


def main(args):
    # initialize the list of class labels MobileNet SSD was trained to detect.
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog",
               "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
               "train", "tvmonitor"]

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args['prototxt'], args['model'])

    # initialize the video stream and output video writer
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(vid)
    writer = None

    # initialize the list of object trackers and corresponding class
    # labels
    trackers = []
    labels = []

    # start the frames per second throughput estimator
    fps = FPS().start()

    frame_counter = 0

    while True:

        (grabbed, frame) = vs.read()
        frame_counter += 1

        if frame is None:
            break

        (frame, rgb) = resize_and_recolor_frame(frame)

        ##
        # Place holder for writing to file
        ##

        if len(trackers) == 0 or frame_counter >= 10:
            frame_counter = 0
            (detections, h, w) = get_object_detections(frame, net)

            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    class_label_index = int(detections[0, 0, i, 1])
                    detection_label = CLASSES[class_label_index]

                    # if the class label is not a person, ignore it
                    if CLASSES[class_label_index] != "person":
                        continue

                    # TODO: Change this up and make it a dict
                    (startX, startY, endX, endY) = get_detection_box_dims(detections[0, 0, i, 3:7], h, w)
                    t = create_tracker(startX, startY, endX, endY, rgb)

                    label = str(detection_label + str(len(labels)))
                    labels.append(label)
                    trackers.append(t)

                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  (0, 255, 0), 2)
                    cv2.putText(frame, label, (startX, startY - 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        else:
            for (t, l) in zip(trackers, labels):

                t.update(rgb)
                pos = t.get_position()

                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)
                cv2.putText(frame, l, (startX, startY - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

     # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.release()


vid = '/Users/nick/PycharmProjects/PlayerTracker/venv/game_film/trimmed_cbj_van.mp4'
prototxt = 'mobilenet_ssd/MobileNetSSD_deploy.prototxt'
model = 'mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
confidence = 0.2

args_ = {'vid': vid, 'prototxt': prototxt, 'model': model, 'confidence': confidence}

main(args_)