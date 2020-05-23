# Space for imports
#
#
#


class TrackedPlayer:

    def __init__(self, rect_coords, tracker, label):
        self.coords = rect_coords  # {startx: , starty: , endx: , endy: }
        self.centroid = []
        self.calc_centroid()
        self.t = tracker
        self.name = label
        self.on_ice = False
        # todo: There is a lot to add here.

    def calc_centroid(self):
        mid_x = abs(self.coords['startx'] - self.coords['endx'])
        mid_y = abs(self.coords['starty'] - self.coords['endy'])
        assert mid_x > 0
        assert mid_y > 0
        self.centroid = [mid_x, mid_y]
