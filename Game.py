import basePlayer
import pygame
from pygame import QUIT
from board import RED, BLUE, TIE
from board import DrawableBoard
import sys
import os

HEIGHT = 480
WIDTH = 640
FPS = 30  # frames per second setting
MILLIS_BETWEEN_GAMES = 500


BLUE_COLOR = (0, 0, 255)
RED_COLOR = (255, 0, 0)

ENABLE_FILE_SAVE = False
CACHE_ONLY_KNOWN_RESULTS = True


class Game:
  def __init__(self, player1: basePlayer, player2: basePlayer, display_surface, save_to_file_name=None):
    self.red_player = player1
    self.blue_player = player2
    self.display_surface = display_surface

    self.fpsClock = pygame.time.Clock()

    self.is_game_over = False
    self.board = DrawableBoard()
    self.winner = 0

    self.cached_results = {}
    self.save_to_file_name = save_to_file_name

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
          self.on_mouse_button_down()

      if not self.get_current_player().is_human and not self.winner:
        # Let the robot choose a move.
        row = self.get_current_player().next_move(self.board)
        self.add_piece(row)

      self.draw_board()
      pygame.display.flip()
      self.fpsClock.tick(FPS)
      if self.winner:
        # once the game ends wait
        pygame.time.wait(MILLIS_BETWEEN_GAMES)
        break

  def draw_board(self):
    self.display_surface.fill((0, 0, 0))
    if self.winner:
      self.draw_winner()
    elif self.get_current_player().is_human:
      self.board.draw(self.display_surface, pygame.mouse.get_pos())
    else:
      self.board.draw(self.display_surface)
    self.draw_score()

  def draw_score(self):
    # This is where blue and red think their score is.
    blue_score = self.blue_player.get_score()
    red_score = self.red_player.get_score()

    if 0.0 <= blue_score < 0.4999:
      line_height = (0.5 - blue_score) * HEIGHT * 2
      pygame.draw.line(self.display_surface, BLUE_COLOR, (620, HEIGHT) , (620, HEIGHT - line_height), 10)
    elif 0.5001 < blue_score <= 1.0:
      line_height = (blue_score - 0.5) * HEIGHT * 2
      pygame.draw.line(self.display_surface, RED_COLOR, (620, HEIGHT) , (620, HEIGHT - line_height), 10)

    if 0.0 <= red_score < 0.49999:
      line_height = (0.5 - red_score) * HEIGHT * 2
      pygame.draw.line(self.display_surface, BLUE_COLOR, (20, HEIGHT) , (20, HEIGHT - line_height), 10)
    elif 0.5001 < red_score <= 1.0:
      line_height = (red_score - 0.5) * HEIGHT * 2
      pygame.draw.line(self.display_surface, RED_COLOR, (20, HEIGHT) , (20, HEIGHT - line_height), 10)


  def get_current_player(self):
    if self.board.turn == RED:
      return self.red_player
    else:
      return self.blue_player

  def on_mouse_button_down(self):
    if not self.winner and self.get_current_player().is_human:
      row = self.board.row_from_pixel(pygame.mouse.get_pos()[0])
      if self.board.can_add_piece(row):
        self.add_piece(row)

  def add_piece(self, row: int):
    self.board.add_piece(row)
    self.winner = self.board.get_winner()
    if ENABLE_FILE_SAVE:
      self.cache_move()
      if self.winner != 0:
        self.dump_results()

  def draw_winner(self):
    self.board.draw(self.display_surface)
    if self.winner[0] == TIE:
      return
    first_win_row_col = self.winner[1][0]
    line_start = self.board.pixel_loc(first_win_row_col[0], first_win_row_col[1])
    line_start = (line_start[0] + 40, line_start[1] + 40)
    last_win_row_col = self.winner[1][3]
    line_end = self.board.pixel_loc(last_win_row_col[0], last_win_row_col[1])
    line_end = (line_end[0] + 40, line_end[1] + 40)

    pygame.draw.line(self.display_surface, (100, 100, 100), line_start, line_end, 10)

  def get_result(self):
    return self.winner

  def cache_move(self):
    features = self.board.get_features_str()
    red_score = self.red_player.get_score()
    blue_score = self.blue_player.get_score()

    saved_score = 0.5
    # If a bot is certain about win/loss, save that score.
    if blue_score == 1 or red_score == 1:
      saved_score = 1
    if blue_score == 0 or red_score == 0:
      saved_score = 0
    if not CACHE_ONLY_KNOWN_RESULTS:
      self.cached_results[features] = saved_score
    elif self.red_player.is_known_result():
      self.cached_results[features] = red_score
    elif self.blue_player.is_known_result():
      self.cached_results[features] = blue_score


  def dump_results(self):
    winner = self.winner[0]
    label_map = {
      RED: 0.9,
      BLUE: 0.1,
      TIE: 0.5
    }
    with open(self.save_to_file_name, 'a') as out_file:
      for result_key, result_value in self.cached_results.items():
        if result_value != 1 and result_value != 0:
          result_value = label_map[winner]
        out_file.write(','.join([str(result_value), str(result_key)]))
        out_file.write('\n')
