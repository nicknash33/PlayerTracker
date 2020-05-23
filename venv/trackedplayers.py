# Space for imports
#
#
#


class TrackedPlayer:

    def __init__(self, center, tracker, label):
        self.centroid = center
        self.tracker = tracker
        self.name = label
        self.on_ice = False
        self.past_positions = [[], []]  # [[xs], [ys]]
        self.current_position = {'x': 0, 'y': 0}
        # todo: There is a lot to add here.

    def update_position(self, centroid):
        self.current_position = centroid
        self.past_positions[0].append(self.current_position['x'])
        self.past_positions[1].append(self.current_position['y'])

    def validate_past_positions(self):
        assert len(self.past_positions) == 2  # If this fails we somehow added a 3rd dimension
        assert len(self.past_positions[0] == self.past_positions[1])  # x and y need to be equal in length
