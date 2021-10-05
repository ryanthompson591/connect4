import random
from basePlayer import BasePlayer
from board import HORIZONTAL_TILES, VERTICAL_TILES, copy_board, Board, RED, BLUE, TIE
import random

MAX_DEPTH = 1

def calculate_score_for_line(line) -> int:
  total_red = sum(tile == RED for tile in line)
  total_blue = sum(tile == BLUE for tile in line)
  if total_blue != 0 and total_red != 0:
    # If red and blue pieces block each other then there can be no win.
    return 0
  if total_blue == 4:
    # blue wins
    return -200
  elif total_red == 4:
    return 200
  if total_blue == 3:
    # arbitrarily assign -8 points for having 3 in a row blue
    return -8
  if total_red == 3:
    return 8
  if total_blue == 2:
    return -1
  if total_red == 2:
    return -1
  # maybe everything is empty or there's just one piece.
  return 0

def calculate_score(p) -> float:

  total_score = 0

  # Add scores for all horizontal lines.
  for x in range(0, HORIZONTAL_TILES - 3):
    for y in range(VERTICAL_TILES):
      line = [p[x][y], p[x + 1][y], p[x + 2][y], p[x + 3][y]]
      total_score += calculate_score_for_line(line)

  # Add scores for all vertical lines.
  for x in range(HORIZONTAL_TILES):
    for y in range(0, VERTICAL_TILES - 3):
      line = [p[x][y], p[x][y + 1], p[x][y + 2], p[x][y + 3]]
      total_score += calculate_score_for_line(line)

  # Add scores for diagonals going right and down.
  for x in range(0, HORIZONTAL_TILES - 3):
    for y in range(3, VERTICAL_TILES):
      line = [p[x][y], p[x + 1][y - 1], p[x + 2][y - 2], p[x + 3][y - 3]]
      total_score += calculate_score_for_line(line)

  # Add scores for diagonal going right and up.
  for x in range(0, HORIZONTAL_TILES - 3):
    for y in range(0, VERTICAL_TILES - 3):
      line = [p[x][y], p[x + 1][y + 1], p[x + 2][y + 2], p[x + 3][y + 3]]

  if total_score >= 200:
    return 1.0
  elif total_score <= -200:
    return 0.0
  # hopefully a score won't ever be more than 200 otherwise non winning situations might look like wins.
  actual_score = 0.5
  actual_score += float(total_score) / 200.0
  return actual_score

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
    return calculate_score(board.pieces)

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


class MinMaxBotHeuristic(BasePlayer):
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

