import constants
from game.casting.actor import Actor
from game.casting.robot import Robot
from game.shared.point import Point

class Bullet(Actor):
  '''
  Bullets that appear on the screen and move upwards toward the centipede.
  '''
  def __init__(self, cast):
    super().__init__()
    self.set_color(constants.WHITE)
    self.prepare_body(cast)

  def prepare_body(self, cast):
    robot = cast.get_first_actor("robot")
    robot_position = robot.get_position()
    #make the bullet originate from the robots position
    my_position = robot_position.add(Point(0, -constants.CELL_SIZE))
    text = "*"

    self.set_velocity(Point(0, -1 * constants.CELL_SIZE)) #Velocity of the bullet moving upward
    self.set_position(my_position)
    self.set_text(text)