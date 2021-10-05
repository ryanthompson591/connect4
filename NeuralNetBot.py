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
  model_file_name = "models/win_estimate_%s.model" % (i-1)

  return keras.models.load_model(model_file_name)


class NeuralNetBot(BasePlayer):
  def __init__(self):
    self.score = 0.5
    self.model = most_recent_model()

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
          score = self.calculate_score(new_board)

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
    features = np.reshape(features, (1, 43))
    score_array = self.model.predict(features)
    score = score_array[0][0]
    if score > 1:
      score = 0.99
    elif score < 0.0:
      score = 0.01
    return score
