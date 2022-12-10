import constants

from game.scripting.action import Action
from game.shared.point import Point
from game.casting.bullet import Bullet

class ControlActorsAction(Action):
    """
    An input action that controls the snake.
    
    The responsibility of ControlActorsAction is to get the direction and move the snake's head.

    Attributes:
        _keyboard_service (KeyboardService): An instance of KeyboardService.
    """

    def __init__(self, keyboard_service):
        """Constructs a new ControlActorsAction using the specified KeyboardService.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            direction (Point): used to save the current velocity of the centipede.
            move_down (Point): set the velocity to move down.
            previous_direction (Point): saves the current direction of the centipede.
            rotate (int):
        """
        self._keyboard_service = keyboard_service
        self._direction = Point(constants.CELL_SIZE, 0)
        self._move_down = Point(0, constants.CELL_SIZE)
        self._previous_direction = Point(0,0)
        self._rotate = 0

    def execute(self, cast, script):
        """Executes the control actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """    
        self._centipede_movement(cast)
        self._robot_movement(cast)
        self._bullet_movement(cast)

    def _centipede_movement(self, cast):
        """Controls the movement of the centipede.

        Args:
            cast (Cast): The cast of Actors in the game.
        """  
        centipede = cast.get_first_actor("centipede")
        barriers = cast.get_actors("barriers")

        if len(centipede.get_segments()) > 0:
            my_head = centipede.get_segments()[0]
            my_position = my_head.get_position()
            move_right = my_position.add(Point(constants.CELL_SIZE, 0))
            move_left = my_position.add(Point(-constants.CELL_SIZE, 0))
            my_velocity = my_head.get_velocity()
            dodge_barrier = False

            # Finds barriers to the left or right of the centipede
            for barrier in barriers:
                if (move_right.equals(barrier.get_position())) or (move_left.equals(barrier.get_position())):
                    dodge_barrier = True
                    break

            # If there is a barrier to the left or right, this checks below the head
            if dodge_barrier:
                for barrier in barriers:
                    if (my_position.add(Point(0, constants.CELL_SIZE)).equals(barrier.get_position())):
                        self._previous_direction = my_velocity.get_x()
                        self._rotate = 1
                        break

            # Checks for the edge of the screen or if a barrier is next to the centipede and moves it down
            if self._rotate == 0:
                if ((my_position.get_x() <= 0) or (my_position.get_x() + constants.CELL_SIZE >= constants.MAX_X)) or dodge_barrier:
                    self._previous_direction = my_velocity.get_x()
                    centipede.turn_head(self._move_down)
                    self._rotate = 1
            else: # If the centipede is moving down, turn it left or right
                centipede.turn_head(Point(self._previous_direction * -1, 0))
                self._rotate = 0

    def _robot_movement(self, cast):
        """Controls the movement of the Robot.

        Args:
            cast (Cast): The cast of Actors in the game.
        """  
        robot = cast.get_first_actor("robot")
        robotDirection = Point(0,0)
        # left
        if self._keyboard_service.is_key_down('a'):
            robotDirection = Point(-constants.CELL_SIZE, 0)
        
        # right
        if self._keyboard_service.is_key_down('d'):
            robotDirection = Point(constants.CELL_SIZE, 0)

        robot.set_velocity(robotDirection)

    def _bullet_movement(self, cast):
        """Controls the creation of the bullet with spacebar or removal from hitting the top of the screen.

        Args:
            cast (Cast): The cast of Actors in the game.
        """  
        bullets = cast.get_actors("bullet")

        for bullet in bullets:
            my_position = bullet.get_position()
            if my_position.get_y() <= 0:
                cast.remove_actor("bullet", bullet)
        
        # shoot
        if self._keyboard_service.is_key_down('space'):
            cast.add_actor("bullet", Bullet(cast))