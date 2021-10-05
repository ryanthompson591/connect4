import random
from basePlayer import BasePlayer
from board import HORIZONTAL_TILES, VERTICAL_TILES, copy_board, Board, RED, BLUE, TIE
import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

def most_recent_model() -> str:
  i = 0
  while os.path.exists("models/win_estimate_%s.model" % i):
    i += 1
  return "models/win_estimate_%s.model" % (i-1)


MAX_DEPTH = 1
FEATURES = 43


class NeuralMinMaxBot(BasePlayer):
  def __init__(self):
    self.score = 0.5
    self.model = keras.models.load_model(most_recent_model())

  def next_move(self, board: Board):
    pieces = board.pieces

    move_scores = {}
    for move in range(HORIZONTAL_TILES):
      if board.can_add_piece(move):
        new_board = copy_board(board)
        new_board.add_piece(move)

        score = self.min_max_value(new_board, 0)

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

  def calculate_score(self, board) -> float:
    features = board.get_features()
    features = np.array(features)
    features = np.reshape(features, (1, FEATURES))
    score_array = self.model.predict(features)
    score = score_array[0][0]
    if score > 1:
      score = 0.99
    elif score < 0.0:
      score = 0.01
    return score

  def min_max_value(self, board, depth) -> float:
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
    if depth >= MAX_DEPTH:
      return self.calculate_score(board)

    values = {}

    for row in range(HORIZONTAL_TILES):
      if board.can_add_piece(row):
        board.add_piece(row)
        values[row] = self.min_max_value(board, depth + 1)
        board.remove_piece(row)
        # alpha beta prune
        # This means if there is a winning move to take, the bot
        # will always take that move, so no need to calculate other possibilities
        if values[row] == 1 and board.turn == RED:
          return 1.0
        elif values[row] == -1 and board.turn == BLUE:
          return 0.0

    if board.turn == RED:
      return max(list(values.values()))
    else:
      return min(list(values.values()))
