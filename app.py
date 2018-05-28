import argparse
import json

import pygame
from pygame import Surface, Rect

from game_of_life import GameOfLife

# Aliases for keyboard keys
Q = pygame.K_q
ESC = pygame.K_ESCAPE
SP = pygame.K_SPACE
W = pygame.K_w
A = pygame.K_a
S = pygame.K_s
D = pygame.K_d


class App:
  """ Game of life pygame app """

  SCREEN_WIDTH = 600
  SCREEN_HEIGHT = 600

  NUM_ROWS = 100
  NUM_COLS = 100

  TITLE = "Game of Life"

  def __init__(self, initial_active_file=None):
    pygame.init()
    self.clock = pygame.time.Clock()
    # load and set the logo
    pygame.display.set_caption(self.TITLE)

    # create a surface on screen that has the size of 240 x 180
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    self.cell_width = self.SCREEN_WIDTH / self.NUM_COLS
    self.cell_height = self.SCREEN_HEIGHT / self.NUM_ROWS

    active_rect = Surface((self.cell_width, self.cell_height))
    active_rect.fill((255, 0, 0))
    inactive_rect = Surface((self.cell_width, self.cell_height))
    inactive_rect.fill((128, 128, 128))
    self.surface_by_class = {0: inactive_rect, 1: active_rect}

    if initial_active_file:
      with open(args.f, 'r') as f:
        initial_active = json.load(f)
    else:
      initial_active = None
    self.game = GameOfLife(self.NUM_ROWS, self.NUM_COLS, initial_active=initial_active)

  def current_cell_surface(self, position):
    return self.surface_by_class[self.game.mat[position]]

  def draw(self):
    self.screen.fill((255, 255, 255))
    for i in range(self.NUM_ROWS):
      for j in range(self.NUM_COLS):
        current_cell_rect = Rect((i * self.cell_width, j * self.cell_height),
                                 (self.cell_width, self.cell_height))
        self.screen.blit(self.current_cell_surface((i, j)), current_cell_rect)

    pygame.display.flip()

  def update(self):
    if self.autoplay or self.step:
      self.game.step()

  def handle_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.KEYDOWN:
        if event.key == Q or event.key == ESC:
          self.running = False
        if event.key == SP:
          self.self = True
        if event.key == A:
          self.autoplay = not self.autoplay

      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        row = int(mouse_position[0] / self.cell_width)
        col = int(mouse_position[1] / self.cell_height)
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
  args = parser.parse_args()
  app = App(initial_active_file=args.f)
  app.main_loop()
