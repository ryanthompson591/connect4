import random
from basePlayer import BasePlayer

class RandomBot(BasePlayer):

  def next_move(self, board):
    valid_moves = []
    for row in range(7):
      if board.can_add_piece(row):
        valid_moves.append(row)
    return random.choice(valid_moves)