"""Provides the Button class for clickable menu buttons."""

import pygame
from snacman.constants import SCREEN_SIZE, BLACK, WHITE
from snacman.display import FONT

class Button:
    def __init__(
            self, text, choice, x=None, y=None, width=None, height=None, 
            colour=WHITE, highlight=None, text_colour=BLACK
        ):
        self.label = FONT.render(text, True, text_colour)
        self.choice = choice
        self.colour = colour
        self.highlight = highlight or colour

        label_width, label_height = self.label.get_size()

        width = width or label_width + label_height
        height = height or label_height * 2

        if x is None:
            x = (SCREEN_SIZE[0] - width) / 2

        if y is None:
            y = (SCREEN_SIZE[1] - height) / 2

        self.rect = pygame.Rect(x, y, width, height)
