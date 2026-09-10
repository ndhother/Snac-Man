"""Provides the Snac-Man player character and its movement."""

import pygame
from snacman.character import Character
from snacman.constants import COLOURS, CELL_SIZE

MOVE_SPEED = 3

class SnacMan(Character):
    def __init__(self, pos):
        super().__init__(*pos, COLOURS["YELLOW"])

    def get_pos(self):
        """
        Derives current grid location using centre of sprite image.
        """
        return self.rect.centerx // CELL_SIZE, self.rect.centery // CELL_SIZE

    def move(self, x, y, walls):
        """
        Updates player position and prevents them from moving through walls.
        """
        if x:
            self.rect.x += x * MOVE_SPEED

            for wall in pygame.sprite.spritecollide(self, walls, False):
                if x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right

        if y:
            self.rect.y += y * MOVE_SPEED

            for wall in pygame.sprite.spritecollide(self, walls, False):
                if y > 0:
                    self.rect.bottom = wall.rect.top
                else:
                    self.rect.top = wall.rect.bottom
