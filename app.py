import sys
import datetime
import argparse
import json

import pygame
from pygame import Rect

from game_of_life import GameOfLife, GameOfLifeHighLife
from ui import UI

# Aliases for keyboard keys
Q = pygame.K_q
ESC = pygame.K_ESCAPE
SP = pygame.K_SPACE
W = pygame.K_w
A = pygame.K_a
S = pygame.K_s
D = pygame.K_d
R = pygame.K_r


class App:
  """ Game of life pygame app """

  DEFAULT_WINDOW_WIDTH = 600
  DEFAULT_WINDOW_HEIGHT = 600

  DEFAULT_NUM_ROWS = 100
  DEFAULT_NUM_COLS = 100

  TITLE = "Game of Life"

  def __init__(self, size=None, window_size=None, initial_active_file=None, mode="game_of_life"):
    """
    args:
      size: number of rows and columns in the matrix
      initial_active_file: json file to load the state of the matrix from
      mode: str, 'game_of_life' or 'high_life', game mode
    """
    num_cols, num_rows = size or [self.DEFAULT_NUM_ROWS, self.DEFAULT_NUM_COLS]
    window_width, window_heigth = window_size or [
        self.DEFAULT_WINDOW_WIDTH,
        self.DEFAULT_WINDOW_HEIGHT,
    ]

    pygame.init()
    self.clock = pygame.time.Clock()
    # load and set the logo
    pygame.display.set_caption(self.TITLE)

    if initial_active_file:
      with open(args.f, "r") as f:
        save_obj = json.load(f)
      self.game = GameOfLife.load(save_obj)
      num_cols, num_rows = self.game.size
    else:
      print("Game mode is: ", mode)
      if mode == "game_of_life":
        self.game = GameOfLife(num_rows, num_cols)
      elif mode == "high_life":
        self.game = GameOfLifeHighLife(num_rows, num_cols)
      else:
        raise Exception("Unknown game mode: {}".format(mode))

    self.ui = UI(window_width, window_heigth, num_cols, num_rows, self.game)

  def draw(self, draw_all=False):
    if draw_all:
      self.ui.draw(None)
    else:
      # self.ui.draw(None)
      self.ui.draw(self.changed_cells)

  def update(self):
    """ Update the cell matrix 
    """
    if self.autoplay or self.step:
      self.changed_cells += self.game.step()

  def save_game(self):
    """ Saves a json containing the game state in a json file called 'game_of_life_dd_mm_yy_hh_mm_ss.json'
    """
    now = datetime.datetime.now()
    save_fpath = "game_of_life_{day}_{month}_{year}_{hour}_{minute}_{second}.json".format(
        day=now.day,
        month=now.month,
        year=now.year,
        hour=now.hour,
        minute=now.minute,
        second=now.second,
    )
    try:
      print("saving game as: ", save_fpath)
      self.game.save(save_fpath)
      print("saved correctly")
    except Exception as e:
      print("error saving game: {}".format(e))

  def handle_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.KEYDOWN:
        if event.key == Q or event.key == ESC:
          self.running = False
        if event.key == SP:
          self.step = True
        if event.key == A:
          self.autoplay = not self.autoplay
        if event.key == S:
          self.save_game()
        if event.key == R:
          self.game.restart()

      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        window_surf = self.ui.position_to_surf(mouse_position)
        print('clicked on: {} -> {} '.format(mouse_position, window_surf))
        if window_surf == "game":
          row, col = self.ui.position_to_cell(mouse_position)
          self.game.toggle((row, col))
          self.changed_cells.append((row, col))
        elif window_surf == "score":
          pass

  def main_loop(self):
    self.running = True
    self.autoplay = False
    self.step = False

    self.draw(True)
    while self.running:
      self.changed_cells = []
      self.handle_input()

      self.update()

      self.draw()
      self.step = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", nargs="?", default=None)
  parser.add_argument("-m", default="game_of_life")
  parser.add_argument("-s", nargs=2, type=int)
  parser.add_argument("-ws", nargs=2, type=int)
  args = parser.parse_args()
  app = App(initial_active_file=args.f, mode=args.m, size=args.s, window_size=args.ws)
  app.main_loop()
