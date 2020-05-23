import numpy as np
import imutils
import dlib
import cv2
from trackedplayers import TrackedPlayer
import time


class CurrentTrackedObjects:
    #  Array like object of items currently being tracked.
    def __init__(self):
        self.objects = []

    def __getitem__(self, item):
        return self.objects[item]

    def __iter__(self):
        return iter(self.objects)

    def __len__(self):
        return len(self.objects)

    def append(self, object_to_add):
        if self.length_ok():
            self.objects.append(object_to_add)
        else:
            # This is crap. Need to make this based on movement ie if player is actually in use.
            self.objects.pop(0)

    @staticmethod
    def length_ok(self):
        if len(self.objects) > 14:
            return False
        return True


