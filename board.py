import pygame
import math
import copy


EMPTY = 0
RED = 1
BLUE = 2
TIE = 9000

HORIZONTAL_TILES = 7
VERTICAL_TILES = 6
OFF_WHITE = (235, 235, 235)

class Board:
  def __init__(self):
    self.pieces = []
    for y in range(HORIZONTAL_TILES):
      new_column = [0] * VERTICAL_TILES
      self.pieces.append(new_column)
    self.turn = RED

  def can_add_piece(self, row):
    return self.pieces[row][0] == EMPTY

  def add_piece(self, row):
    column = self.pieces[row]
    y = len(column) - column[::-1].index(EMPTY) - 1

    self.pieces[row][y] = self.turn
    if self.turn == RED:
      self.turn = BLUE
    else:
      self.turn = RED

  def remove_piece(self, row):
    # removes the last piece played.
    column = self.pieces[row]
    if EMPTY not in column:
      y = 0
    else:
      y = len(column) - column[::-1].index(EMPTY)

    self.pieces[row][y] = EMPTY
    if self.turn == RED:
      self.turn = BLUE
    else:
      self.turn = RED


  def is_tie(self):
    for row in range(HORIZONTAL_TILES):
      if self.can_add_piece(row):
        return False
    return True

  # returns 0 for no win or 1 or 2 for red or blue win
  def get_winner(self):
    if self.is_tie():
      return [TIE]
    # see if it's a horizontal win
    p = self.pieces
    for x in range(0, HORIZONTAL_TILES-3):
      for y in range(VERTICAL_TILES):
        if p[x][y] != EMPTY and p[x][y] == p[x+1][y] == p[x+2][y] == p[x+3][y]:
          return [p[x][y], [(x,y), (x+1,y),(x+2,y),(x+3,y)]]

    # look for a vertical win
    for x in range(HORIZONTAL_TILES):
      for y in range(0, VERTICAL_TILES-3):
        if p[x][y] != EMPTY and p[x][y] == p[x][y + 1] == p[x][y + 2] == p[x][y + 3]:
          return [p[x][y],[(x,y), (x,y + 1), (x,y + 2), (x, y + 3)]]

    # look for a diagonal win going right and down
    for x in range(0, HORIZONTAL_TILES-3):
      for y in range(3, VERTICAL_TILES):
        if p[x][y] != EMPTY and p[x][y] == p[x+1][y - 1] == p[x+2][y - 2] == p[x+3][y - 3]:
          return [p[x][y], [(x,y), (x+1,y - 1), (x+2,y - 2), (x+3,y - 3)]]

    # look for a diagonal win going right and up
    for x in range(0, HORIZONTAL_TILES-3):
      for y in range(0, VERTICAL_TILES-3):
        if p[x][y] != EMPTY and p[x][y] == p[x+1][y + 1] == p[x+2][y + 2] == p[x+3][y + 3]:
          return [p[x][y], [(x,y), (x+1,y + 1), (x+2,y + 2), (x+3,y + 3)]]

    return EMPTY

  def get_features(self) -> list:
    feature_map = {
      RED: 1,
      BLUE: 0,
      EMPTY: 0.5,
    }
    features = []
    for x in range(HORIZONTAL_TILES):
      for y in range(VERTICAL_TILES):
        features.append(feature_map[self.pieces[x][y]])
    features.append(feature_map[self.turn])
    return features

  def get_features_str(self) -> str:
    features = self.get_features()
    return ','.join([str(f) for f in features])


class DrawableBoard(Board):
  def __init__(self):
    super().__init__()
    self.tile = [None] * 3
    self.tile[EMPTY] = pygame.image.load("Assets/EmptyTile.png")
    self.tile[RED] = pygame.image.load("Assets/RedTile.png")
    self.tile[BLUE] = pygame.image.load("Assets/BlueTile.png")

    self.alpha_tile = [None] * 3
    self.alpha_tile[RED] = pygame.image.load("Assets/RedTile.png").convert()
    self.alpha_tile[RED].set_alpha(128)
    self.alpha_tile[BLUE] = pygame.image.load("Assets/BlueTile.png").convert()
    self.alpha_tile[BLUE].set_alpha(128)


  def draw(self, surface, show_tile_at = None):
    pygame.draw.rect(surface, OFF_WHITE, (40, 0, 560, 480))

    for x in range(HORIZONTAL_TILES):
      for y in range(VERTICAL_TILES):
        pixel_loc = self.pixel_loc(x, y)
        tile_type = self.pieces[x][y]
        surface.blit(self.tile[tile_type], pixel_loc)

    if show_tile_at:
      row = self.row_from_pixel(show_tile_at[0])
      if 0 <= row < HORIZONTAL_TILES and self.can_add_piece(row):
        column = self.pieces[row]
        col = len(column) - column[::-1].index(EMPTY) - 1
        pixel_loc = self.pixel_loc(row, col)
        tile_type = self.turn
        surface.blit(self.alpha_tile[tile_type], pixel_loc)


  @staticmethod
  def pixel_loc(row, col):
    return row * 80 + 40, col * 80

  @staticmethod
  def row_from_pixel(pixel_x):
    row = math.floor((pixel_x - 40) / 80)
    if row > HORIZONTAL_TILES - 1:
      return HORIZONTAL_TILES - 1
    elif row < 0:
      return 0
    return row

def copy_board(board) -> Board:
  new_board = Board()
  new_board.turn = board.turn
  new_board.pieces = copy.deepcopy(board.pieces)
  return new_board
