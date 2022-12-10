import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the bullets collide
    with barriers, centipede, or top of the screen.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
        _did_player_win (boolean): Whether or not the player won.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._did_player_win = False

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over and not self._did_player_win:
            self._handle_bullet_collision(cast)
            self._handle_player_collision(cast)
        
        self._player_won(cast)
        self._handle_game_over(cast)

    def _handle_bullet_collision(self, cast):
        """Checks for collisions with the bullets.  Also removes actors and updates score accordingly.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # Grab the actors
        score = cast.get_first_actor("scores")
        barriers = cast.get_actors("barriers")
        centipede = cast.get_first_actor("centipede")
        centipede_segments = centipede.get_segments()
        bullets = cast.get_actors("bullet")  
        
        # Loop through each bullet to compare its position with each barrier and centipede segment
        for bullet in bullets:
            for segment in centipede_segments:
                if bullet.get_position().equals(segment.get_position()):
                    points = segment.get_points()
                    score.add_points(points)
                    centipede.shrink_tail()
                    cast.remove_actor("bullet", bullet)
                   
            for barrier in barriers:
                if bullet.get_position().equals(barrier.get_position()):
                    if barrier.get_color() == constants.YELLOW:
                        points = barrier.get_points()
                        score.add_points(points)
                        barrier.set_color(constants.GREEN)
                        cast.remove_actor("bullet", bullet)
                    elif barrier.get_color() == constants.GREEN:
                        points = barrier.get_points() + 25
                        score.add_points(points)
                        barrier.set_color(constants.BLUE)
                        cast.remove_actor("bullet", bullet)
                    else:
                        points = barrier.get_points() + 50
                        score.add_points(points)                       
                        cast.remove_actor("barriers", barrier)
                        cast.remove_actor("bullet", bullet)

    def _handle_player_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        centipede = cast.get_first_actor("centipede")
        if  len(centipede.get_segments()) < 1:
            self._did_player_win = True
        else:
            head = centipede.get_segments()[0]
            robot = cast.get_first_actor("robot")

        #Game will end if the centipede collides with the robot
            if head.get_position().equals(robot.get_position()):
                self._is_game_over = True

    def _player_won(self, cast):

        if self._did_player_win:

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("You conquered the Centipede!")
            message.set_position(position)
            cast.add_actor("messages", message)                      

    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the centipede white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            centipede = cast.get_first_actor("centipede")
            segments = centipede.get_segments()

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments:
                segment.set_color(constants.WHITE)         