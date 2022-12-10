import constants
from game.casting.actor import Actor
from game.shared.point import Point

class Robot(Actor):
  '''
  Our blaster thing that is limited to left and right movements at the bottom the the screen
  '''
  def __init__(self):
    super().__init__()
    self.set_color(constants.GREEN)
    self.prepare_body()

  def prepare_body(self):
    x = int(constants.MAX_X /2)
    y = int(constants.MAX_Y -15)
    position = Point(x,y)
    text = "#"

    self.set_position(position)
    self.set_text(text)
    
    

  

  