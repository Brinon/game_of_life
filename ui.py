import pygame
from pygame import Rect, Surface


class UI:
  """ UI of the game of life
  85 of height is the game viewer
  15 of height (bottom) is scoreboard
  """

  def __init__(self, width: int, height: int, num_cols: int, num_rows, game):
    self.width = width
    self.height = height
    self.num_cols = num_cols
    self.num_rows = num_rows
    self.game = game

    self.screen = pygame.display.set_mode((self.width, self.height))

    board_height = int(0.85 * self.height)
    scores_height = self.height - board_height

    self.cell_width = self.width / self.num_cols
    self.cell_height = self.height / self.num_rows

    active_rect = Surface((self.cell_width, self.cell_height))
    active_rect.fill((255, 0, 0))
    inactive_rect = Surface((self.cell_width, self.cell_height))
    inactive_rect.fill((128, 128, 128))
    self.surface_by_class = {0: inactive_rect, 1: active_rect}

    board_height = int(0.85 * self.height)
    scores_height = self.height - board_height
    # game_surf = Surface()
    # scores_surt = Surface()

  def current_cell_surface(self, position):
    return self.surface_by_class[self.game.mat[position]]

  def position_to_cell(self, position):
    """ return the coordinates of the current cell inside the matrix given a mouse
    pixel position """
    row = int(position[0] / self.cell_width)
    col = int(position[1] / self.cell_height)
    return row, col

  def draw(self, changed_cells=None):
    """
    if changed_cells is None then paint all cells
    """
    # self.screen.fill((255, 255, 255))
    if changed_cells is None:
      changed_cells = [(i, j) for i in range(self.num_cols) for j in range(self.num_rows)]

    for (i, j) in changed_cells:
      current_cell_rect = Rect(
          (i * self.cell_width, j * self.cell_height),
          (self.cell_width, self.cell_height),
      )
      self.screen.blit(self.current_cell_surface((i, j)), current_cell_rect)
    pygame.display.flip()
