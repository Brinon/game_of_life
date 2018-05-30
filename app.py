import datetime
import argparse
import json

import pygame
from pygame import Surface, Rect

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

  SCREEN_WIDTH = 600
  SCREEN_HEIGHT = 600

  NUM_ROWS = 100
  NUM_COLS = 100

  TITLE = "Game of Life"

  def __init__(self, initial_active_file=None, mode='game_of_life'):
    pygame.init()
    self.clock = pygame.time.Clock()
    # load and set the logo
    pygame.display.set_caption(self.TITLE)

    if initial_active_file:
      with open(args.f, 'r') as f:
        initial_active = json.load(f)
      self.game = GameOfLife.load(initial_active)
    else:
      print('Game mode is: ', mode)
      if mode == 'game_of_life':
        self.game = GameOfLife(self.NUM_ROWS, self.NUM_COLS)
      elif mode == 'high_life':
        self.game = GameOfLifeHighLife(self.NUM_ROWS, self.NUM_COLS)
      else:
        raise Exception('Unknown game mode: {}'.format(mode))

    self.ui = UI(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.NUM_COLS, self.NUM_ROWS, self.game)

  def draw(self):
    self.ui.draw()

  def update(self):
    if self.autoplay or self.step:
      self.game.step()

  def save_game(self):
    """ Saves a json containing the game state in a json file called 'game_of_life_dd_mm_yy_hh_mm_ss.json'
    """
    now = datetime.datetime.now()
    save_fpath = 'game_of_life_{day}_{month}_{year}_{hour}_{minute}_{second}.json'.format(
        day=now.day,
        month=now.month,
        year=now.year,
        hour=now.hour,
        minute=now.minute,
        second=now.second,
    )
    try:
      print('saving game as: ', save_fpath)
      self.game.save(save_fpath)
      print('saved correctly')
    except Exception as e:
      print('error saving game: {}'.format(e))

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
        row, col = self.ui.position_to_cell(mouse_position)
        self.game.toggle((row, col))

  def main_loop(self):
    self.running = True
    self.autoplay = False
    self.step = False

    while self.running:
      self.handle_input()
      self.update()
      self.draw()
      self.step = False
      self.clock.tick(20)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', nargs='?', default=None)
  parser.add_argument('-m', default='game_of_life')
  args = parser.parse_args()
  app = App(initial_active_file=args.f, mode=args.m)
  app.main_loop()
