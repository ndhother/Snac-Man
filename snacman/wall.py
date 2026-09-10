"""Provides the Wall class for maze walls."""

import pygame
from snacman.constants import WHITE, CELL_SIZE

class Wall(pygame.sprite.Sprite):
    def __init__(self, col, row, width, height, visible=True):
        super().__init__()

        self.col = col
        self.row = row
        self.width = width
        self.height = height

        self.image = pygame.Surface((width * CELL_SIZE, height * CELL_SIZE))
        self.rect = self.image.get_rect(x=col * CELL_SIZE, y=row * CELL_SIZE)

        if visible:
            self.image.fill(WHITE)
