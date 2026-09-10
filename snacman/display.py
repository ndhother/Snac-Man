"""Provides functions for drawing text and interactive buttons."""

import pygame
from snacman.constants import SCREEN_SIZE, WHITE

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 25)

def draw_text(screen, text, x=None, y=None, colour=WHITE):
    """
    Renders text at given coordinates or defaults to centre of the screen.
    """
    label = FONT.render(text, True, colour)

    if x is None:
        x = (SCREEN_SIZE[0] - label.get_width()) / 2

    if y is None:
        y = (SCREEN_SIZE[1] - label.get_height()) / 2

    screen.blit(label, (x, y))

def draw_buttons(screen, buttons, pos):
    """
    Renders a list of Button objects on the screen.
    """
    for b in buttons:
        colour = b.highlight if b.rect.collidepoint(pos) else b.colour
        pygame.draw.rect(screen, colour, b.rect)
        screen.blit(b.label, b.label.get_rect(center=b.rect.center))
