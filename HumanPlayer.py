from basePlayer import BasePlayer


class HumanPlayer(BasePlayer):
  def __init__(self):
    pass

  def next_move(self, board):
    pass

  @property
  def is_human(self):
    return True