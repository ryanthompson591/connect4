import random
from basePlayer import BasePlayer
from board import HORIZONTAL_TILES, VERTICAL_TILES, copy_board, Board, RED, BLUE, TIE
import random

MAX_DEPTH = 5


def min_max_value(board, depth, max_depth = MAX_DEPTH) -> float:
  # make sure moves are possible.
  if board.is_tie():
    return 0.5

  winner = board.get_winner()
  if winner != 0:
    if winner[0] == RED:
      return 1.0
    else:
      return 0.0

  # If max depth just return the heuristic value.
  if depth >= max_depth:
    return 0.55 # the heuristic value is 0.55 because we'll give advantage to red

  heuristic_values = {}

  for row in range(HORIZONTAL_TILES):
    if board.can_add_piece(row):
      board.add_piece(row)
      heuristic_values[row] = min_max_value(board, depth + 1, max_depth = max_depth)
      board.remove_piece(row)
      # alpha beta prune
      # This means if there is a winning move to take, the bot
      # will always take that move, so no need to calculate other possibilities
      if heuristic_values[row] == 1 and board.turn == RED:
        return 1.0
      elif heuristic_values[row] == -1 and board.turn == BLUE:
        return -1.0

  if board.turn == RED:
    return max(list(heuristic_values.values()))
  else:
    return min(list(heuristic_values.values()))


class MinMaxBot(BasePlayer):
  def __init__(self, depth = MAX_DEPTH):
    self.score = 0.5
    self.max_depth = depth

  def next_move(self, board: Board):
    pieces = board.pieces

    move_scores = {}
    for move in range(HORIZONTAL_TILES):
      if board.can_add_piece(move):
        new_board = copy_board(board)
        new_board.add_piece(move)

        score = min_max_value(new_board, 0, max_depth=self.max_depth)

        if score in move_scores:
          move_scores[score].append(move)
        else:
          move_scores[score] = [move]

    if board.turn == RED:
      self.score = max(move_scores.keys())
    else:
      self.score = min(move_scores.keys())
    return random.choice(move_scores[self.score])

  def get_score(self):
    return self.score

  def reset(self):
    self.score = 0.55

  def is_known_result(self) -> bool:
    return self.score != 0.55



