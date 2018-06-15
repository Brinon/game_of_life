import uuid

import pygame
from pygame import Rect, Surface
"""
Layout of the UI
 ____________
|  ________  |
| |        | |
| |  Game  | |
| |________| |
|  ________  |
| | Score  | |
| |________| |
|____________|

"""


class UIError(Exception):
  pass


class UI:
  """ UI of the game of life
  85 of height is the game viewer
  15 of height (bottom) is scoreboard
  """
  OFFSET_LEFT = 10
  OFFSET_RIGHT = 10
  OFFSET_TOP = 10
  OFFSET_CENTER = 10  # between game and scores
  OFFSET_BOTTOM = 10

  SCORES_HEIGHT = 70

  def __init__(self, width: int, height: int, num_cols: int, num_rows, game):
    self.width = width
    self.height = height
    self.num_cols = num_cols
    self.num_rows = num_rows
    self.game = game

    self.screen_width = self.width + self.OFFSET_LEFT + self.OFFSET_RIGHT
    self.screen_height = (
        self.OFFSET_TOP + self.height + self.OFFSET_CENTER + self.SCORES_HEIGHT +
        self.OFFSET_BOTTOM)
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    self.components = []
    game_screen = Surface((self.width, self.height))
    scores = Surface((self.width, self.SCORES_HEIGHT))
    self.components.append(game_screen, scores)

    self.cell_width = self.width / self.num_cols
    self.cell_height = self.height / self.num_rows

    active_rect = Surface((self.cell_width, self.cell_height))
    active_rect.fill((255, 0, 0))
    inactive_rect = Surface((self.cell_width, self.cell_height))
    inactive_rect.fill((128, 128, 128))
    self.surface_by_class = {0: inactive_rect, 1: active_rect}

  def current_cell_surface(self, position):
    return self.surface_by_class[self.game.mat[position]]

  def position_to_surf(self, position):
    """
    Return:
    str "game", "score", ""
    """
    if position[0] < self.OFFSET_LEFT or position[0] > self.OFFSET_LEFT + self.width:
      return ""

    if self.OFFSET_TOP <= position[1] <= self.OFFSET_TOP + self.height:
      return "game"

    elif (self.OFFSET_TOP + self.height + self.OFFSET_CENTER) <= position[1] <= (
        self.OFFSET_TOP + self.height + self.OFFSET_CENTER + self.SCORES_HEIGHT):
      return "score"

  def position_to_cell(self, position):
    """ return the coordinates of the current cell inside the matrix given a mouse
    pixel position """
    if self.position_to_surf(position) != 'game':
      raise UIError("Position {} is not inside the game Surface!".format(position))
    #compute relative position
    position_i = position[0] - self.OFFSET_LEFT
    position_j = position[1] - self.OFFSET_TOP
    row = int(position_i / self.cell_width)
    col = int(position_j / self.cell_height)

    # inside the game
    return row, col

  def draw(self, **kwargs):
    """
    if changed_cells is None then paint all cells
    """
    for component in self.components:
      component.draw(**kwargs)
      self.screen.blit(component, component.ui_rect)

    # self.screen.fill((255, 255, 255))
    self.scores.fill((255, 0, 0))
    if changed_cells is None:
      changed_cells = [(i, j) for i in range(self.num_cols) for j in range(self.num_rows)]

    for (i, j) in changed_cells:
      current_cell_rect = Rect(
          (i * self.cell_width, j * self.cell_height),
          (self.cell_width, self.cell_height),
      )
      self.game_screen.blit(self.current_cell_surface((i, j)), current_cell_rect)

    # draw game and scores into main screen
    self.screen.blit(self.game_screen,
                     Rect((self.OFFSET_LEFT, self.OFFSET_TOP), (self.width, self.height)))
    self.screen.blit(self.scores,
                     Rect((self.OFFSET_LEFT, self.OFFSET_TOP + self.width + self.OFFSET_CENTER),
                          (self.width, self.SCORES_HEIGHT)))
    pygame.display.flip()


class UIComponent(Surface):
  """ Component in the UI 
  """

  def __init__(self, ui_rect, *args, name=None, **kwargs):
    """
    Args:
      ui_rect: Rect indicating where in the ui window this component is placed
    """
    super().__init__(ui_rect.size, *args, **kwargs)
    self.ui_rect = ui_rect
    self.name = name or 'component_{}'.format(uuid.uuid4())

  def draw(self, **kwargs):
    raise NotImplementedError


class GameUIComponent(UIComponent):

  def __init__(self, num_cols, num_rows, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.num_cols = num_cols
    self.num_rows = num_rows

    self.cell_width = self.width // num_cols
    self.cell_height = self.height // num_rows

    active_rect = Surface((self.cell_width, self.cell_height))
    active_rect.fill((255, 0, 0))
    inactive_rect = Surface((self.cell_width, self.cell_height))
    inactive_rect.fill((128, 128, 128))
    self.surface_by_class = {0: inactive_rect, 1: active_rect}

  def draw(self, changed_cells=None, **kwargs):
    """ changed cells is a list of pairs [[position, class]]"""
    if changed_cells is None:
      changed_cells = [((i, j), 0) for i in range(self.num_cols) for j in range(self.num_rows)]

    for (i, j) in changed_cells:
      current_cell_rect = Rect(
          (i * self.cell_width, j * self.cell_height),
          (self.cell_width, self.cell_height),
      )
      self.blit(self.current_cell_surface((i, j)), current_cell_rect)
