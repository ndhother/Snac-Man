"""Provides the Item class for collectible items."""

import pygame
from snacman.constants import COLOURS, CELL_SIZE

ITEM_SIZE = (4, 4)
ITEM_MARGIN = (CELL_SIZE - ITEM_SIZE[0]) / 2

class Item(pygame.sprite.Sprite):
    def __init__(self, col, row):
        super().__init__()

        self.image = pygame.Surface(ITEM_SIZE)
        self.rect = self.image.get_rect(
            x=CELL_SIZE * col + ITEM_MARGIN, y=CELL_SIZE * row + ITEM_MARGIN
        )
        self.image.fill(COLOURS["YELLOW"])
