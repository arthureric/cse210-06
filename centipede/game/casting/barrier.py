import random
import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Barrier(Actor):
    """
    A barrier that will block centipede movement.
    
    The responsibility of Barrier is to select a random position and points that it's worth.

    Attributes:
        _points (int): The number of points the barrier is worth.
    """

    def __init__(self, cast):
        """Constructs Barriers."""

        super().__init__()
        self._points = 50
        self.spawn_barrier(cast)
        
    def spawn_barrier(self, cast):
        """Selects a random number of barriers and positions.  Also sets needed attributes."""
        
        barrier_count =random.randint(20, 30)

        for n in range(barrier_count):
            x = random.randint(2, constants.COLUMNS - 3)
            y = random.randint(1, constants.ROWS)
            position = Point(x, y)
            position = position.scale(constants.CELL_SIZE)
            
            barrier = Actor()
            barrier.set_text("@")
            barrier.set_color(constants.YELLOW)
            barrier.set_position(position)
            barrier.set_points(self._points)
            cast.add_actor("barriers", barrier)

    def get_points(self):
        """
        Gets the points the barrier is worth.
        
        Returns:
            points (int): The points the barrier is worth.
        """
        return self._points