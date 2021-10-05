import random
from basePlayer import BasePlayer
from board import HORIZONTAL_TILES, VERTICAL_TILES, copy_board, Board, RED, BLUE, TIE
import random

def calculate_score_for_line(line) -> int:
  total_red = sum(tile == RED for tile in line)
  total_blue = sum(tile == BLUE for tile in line)
  if total_blue != 0 and total_red != 0:
    # If red and blue pieces block each other then there can be no win.
    return 0
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

  actual_score = 0.5
  # hopefully a score won't ever be more than 200 otherwise non winning situations might look like wins.
  actual_score += float(total_score) / 200.0
  return actual_score

class HeuristicBot(BasePlayer):
  def __init__(self):
    self.score = 0.5

  def next_move(self, board: Board):
    pieces = board.pieces

    move_scores = {}
    for move in range(HORIZONTAL_TILES):
      if board.can_add_piece(move):
        new_board = copy_board(board)
        new_board.add_piece(move)

        # first see if the move completes the game
        winner = new_board.get_winner()
        score = 0.5
        if winner:
          if winner[0] == RED:
            score = 1
          elif winner[0] == BLUE:
            score = 0
          elif winner[0] == TIE:
            score = 0.5
        else:
          score = calculate_score(new_board.pieces)

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