import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Centipede(Actor):
    """
    A long limbless reptile.
    
    The responsibility of Centipede is to move itself.

    Attributes:
        _points (int): The number of points the centipede segments are worth.
        _centipede_color (tuple): The color of the centipede.
        _segments (list): A list of all the segment pieces that make up the centipede
    """
    def __init__(self):
        super().__init__()
        self._centipede_color = constants.RED
        self._segments = []
        self._points = 75
        self._prepare_body()

    def get_segments(self):
        return self._segments

    def move_next(self):
        # move all segments
        for segment in self._segments:
            segment.move_next()
        # update velocities
        for i in range(len(self._segments) - 1, 0, -1):
            trailing = self._segments[i]
            previous = self._segments[i - 1]
            velocity = previous.get_velocity()
            trailing.set_velocity(velocity)

    def get_head(self):
        return self._segments[0]

    def shrink_tail(self):
            self._segments.pop(-1)
            
    def turn_head(self, velocity):
        self._segments[0].set_velocity(velocity)
    
    def _prepare_body(self):

        x = int(20 * constants.CELL_SIZE)
        y = int(1 * constants.CELL_SIZE)

        # Generates each segment with its required attributes
        for i in range(constants.SNAKE_LENGTH):
            position = Point(x - i * constants.CELL_SIZE, y)
            velocity = Point(1 * constants.CELL_SIZE, 0)
            text = "8" if i == 0 else "#"
            
            segment = Actor()
            segment.set_position(position)
            segment.set_velocity(velocity)
            segment.set_text(text)
            segment.set_points(self._points)
            segment.set_color(self._centipede_color)
            self._segments.append(segment)