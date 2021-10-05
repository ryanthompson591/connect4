import random
from basePlayer import BasePlayer
from board import HORIZONTAL_TILES, copy_board, Board
import random

class SimpleHeuristicBot(BasePlayer):

  def __init__(self):
    self.score = 0.5

  def next_move(self, board: Board):
    pieces = board.pieces
    winning_moves = []
    player_num = board.turn
    other_moves = []
    for move in range(HORIZONTAL_TILES):
      if board.can_add_piece(move):
        new_board = copy_board(board)
        new_board.add_piece(move)
        if new_board.get_winner():
          winning_moves.append(move)
        else:
          other_moves.append(move)

    if winning_moves:
      self.score = 1.0
      return random.choice(winning_moves)
    return random.choice(other_moves)

  def get_score(self):
    return self.score