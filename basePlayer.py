import abc
from abc import ABC


# The base class for all bots.
class BasePlayer(ABC):

  @abc.abstractmethod
  def next_move(self, board):
    pass

  @property
  def is_human(self):
    return False

  def get_score(self):
    return 0.5

  def reset(self):
    pass

  def is_known_result(self) -> bool:
    return self.get_score() == 0  or self.get_score() == 1