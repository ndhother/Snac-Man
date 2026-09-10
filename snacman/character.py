"""Provides the base Character class for Snac-Man and enemies."""

import pygame
from snacman.constants import CELL_SIZE

CHARACTER_SIZE = (20, 20)
CHARACTER_MARGIN = (CELL_SIZE - CHARACTER_SIZE[0]) / 2

class Character(pygame.sprite.Sprite):
    def __init__(self, col, row, colour):
        super().__init__()

        self.start_pos = (col, row)
        self.image = pygame.Surface(CHARACTER_SIZE)
        self.image.fill(colour)
        self.reset()
    
    def reset(self):
        """
        Places character at starting position.
        """
        self.col, self.row = self.start_pos
        self.rect = self.image.get_rect(
            x=self.col * CELL_SIZE + CHARACTER_MARGIN, 
            y=self.row * CELL_SIZE + CHARACTER_MARGIN
        )
