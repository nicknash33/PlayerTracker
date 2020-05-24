from imutils.video import FPS
import numpy as np
import argparse
import imutils
import dlib
import cv2
from trackedplayers import TrackedPlayer
import time
from CurrentTrackedObjects import CurrentTrackedObjects
from detected_object import DetectedObject


class ObjectTracker:

    def __init__(self, args):
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog",
                   "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
                   "train", "tvmonitor"]
        self.args = args
        self.trackers = []
        self.labels = []
        self.cto = args['currentTrackedObjects']

        # Frame variables
        self.net = None
        self.vs = None
        self.frame = ''  # Current frame being analyzed.
        self.rgb = None  # Current RGB frame being analyzed.
        self.current_label = ''

        self.detections = None
        self.fps = ''
        self.current_detection_object = ''
        self.last_num_detections = 0

        # Coordinate variables.
        self.h = 0
        self.w = 0
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.centroid = []

    def resize_and_recolor_frame(self):
        self.frame = imutils.resize(self.frame, width=600)
        self.rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def get_object_detections(self):
        (self.h, self.w) = self.frame.shape[:2]
        blob = cv2.dnn.blobFromImage(self.frame, 0.007843, (self.w, self.h), 127.5)
        self.net.setInput(blob)
        self.detections = self.net.forward()

    def get_detection_box_dims(self, detection_object):
        h = self.h
        w = self.w
        box = detection_object * np.array([w, h, w, h])
        (self.x0, self.y0, self.x1, self.y1) = box.astype("int")
        self.calc_center()

    def calc_center(self):
        mid_x = abs(self.x0 - self.x1)
        mid_y = abs(self.y0 - self.y1)
        self.centroid = dict(x=mid_x, y=mid_y)

    def create_tracker(self):
        p = None  # Clear any reference to player before assignment.
        t = dlib.correlation_tracker()
        rect = dlib.rectangle(self.x0, self.y0, self.x1, self.y1)
        t.start_track(self.rgb, rect)
        self.calc_center()
        p = TrackedPlayer(self.centroid, t, self.current_label)
        #self.labels.append(self.current_label)
        return p

    def update_boxes(self, player):
        t = player.tracker
        t.update(self.rgb)
        pos = t.get_position()

        self.x0 = int(pos.left())
        self.y0 = int(pos.top())
        self.x1 = int(pos.right())
        self.y1 = int(pos.bottom())
        self.calc_center()
        self.current_label = player.name
        player.centroid = self.centroid
        self.draw_box()

    def draw_box(self):
        cv2.rectangle(self.frame, (self.x0, self.y0), (self.x1, self.y1),
                      (0, 255, 0), 2)
        cv2.putText(self.frame, self.current_label, (self.x0, self.y0 - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    def clean_up_to_close(self):
        # stop the timer and display FPS information
        self.fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.vs.release()

    @staticmethod
    def is_same_object(center_1, center_2):
        x1 = center_1['x']
        y1 = center_1['y']
        x2 = center_2['x']
        y2 = center_2['y']

        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        if delta_x <= 5 and delta_y <= 5:
            return True

        return False

    def handle_new_objects(self, new_objects):
        to_delete = []
        for new_object in new_objects:
            for obj in self.cto:
                if is_same_object(new_object.centroid, obj.current_position):
                    to_delete.append(index(new_object))
                    break

        for i in to_delete:
            del new_objects[i]  # This is now actual new objects need to do stuff with it


    def start(self):
        # load our serialized model from disk
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(self.args['prototxt'], self.args['model'])

        # initialize the video stream and output video writer
        print("[INFO] starting video stream...")
        self.vs = cv2.VideoCapture(self.args['vid'])

        # start the frames per second throughput estimator
        self.fps = FPS().start()

        frame_counter = 0

        while True:

            frame_tuple = self.vs.read()
            self.frame = frame_tuple[1]
            frame_counter += 1

            if self.frame is None:
                break

            self.resize_and_recolor_frame()

            if len(self.trackers) == 0 or frame_counter >= 10:
                frame_counter = 0
                self.get_object_detections()

                current_detected_object_centers = []
                for i in np.arange(0, self.detections.shape[2]):
                    confidence = self.detections[0, 0, i, 2]

                    if confidence > self.args["confidence"]:
                        class_label_index = int(self.detections[0, 0, i, 1])
                        detection_label = self.CLASSES[class_label_index]
                        self.current_label = str(detection_label + str(len(self.trackers)))

                        # if the class label is not a person, ignore it
                        if self.current_label[0:6] != "person":
                            continue

                        self.current_detection_object = self.detections[0, 0, i, 3:7]
                        self.get_detection_box_dims(self.current_detection_object)
                        new_obj = DetectedObject({'x0': self.x0, 'x1': self.x1, 'y0': self.y0, 'y1': self.y1})
                        new_detected_objects.append(new_obj)

                        self.create_tracker()
                        self.draw_box()

            else:
                centers = {}
                for tracked_player in self.trackers:
                    self.update_boxes(tracked_player)
                    centers[tracked_player.name] = tracked_player.centroid

                if frame_counter >= 9:

                    print(centers)


            cv2.imshow("Frame", self.frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            self.fps.update()

        self.clean_up_to_close()


vid = '/Users/nick/PycharmProjects/PlayerTracker/venv/game_film/trimmed_cbj_van.mp4'
prototxt = 'mobilenet_ssd/MobileNetSSD_deploy.prototxt'
model = 'mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
confidence = 0.10
cto = CurrentTrackedObjects()

args_ = {'vid': vid, 'prototxt': prototxt, 'model': model, 'confidence': confidence, 'currentTrackedObjects': cto}

ot = ObjectTracker(args_)
ot.start()