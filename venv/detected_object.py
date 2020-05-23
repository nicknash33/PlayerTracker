
class DetectedObject:
    def __init__(self, coords):
        self.coords = coords
        center_x = abs(coords['x0'] - coords['x1'])
        center_y = abs(coords['y0'] - coords['y1'])
        self.centroid = dict(x=center_x, y=center_y)
