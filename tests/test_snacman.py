import pygame
import pytest
from snacman.constants import CELL_SIZE
from snacman.snacman import SnacMan, MOVE_SPEED
from snacman.wall import Wall

FRAMES_PER_CELL = CELL_SIZE / MOVE_SPEED

@pytest.fixture
def snacman():
    return SnacMan((5, 12))

def test_snacman_get_pos(snacman):
    assert snacman.get_pos() == (5, 12)

def test_snacman_horizontal_movement(snacman):
    snacman.move(4 * FRAMES_PER_CELL, 0, pygame.sprite.Group())
    assert snacman.get_pos() == (9, 12)

    snacman.move(-2 * FRAMES_PER_CELL, 0, pygame.sprite.Group())
    assert snacman.get_pos() == (7, 12)

def test_snacman_vertical_movement(snacman):
    snacman.move(0, FRAMES_PER_CELL, pygame.sprite.Group())
    assert snacman.get_pos() == (5, 13)

    snacman.move(0, -3 * FRAMES_PER_CELL, pygame.sprite.Group())
    assert snacman.get_pos() == (5, 10)

def test_snacman_diagonal_movement(snacman):
    snacman.move(-FRAMES_PER_CELL, 2 * FRAMES_PER_CELL, pygame.sprite.Group())
    assert snacman.get_pos() == (4, 14)

def test_snacman_no_movement(snacman):
    snacman.move(0, 0, pygame.sprite.Group())
    assert snacman.get_pos() == (5, 12)

def test_snacman_horizontal_collision(snacman):
    snacman.move(
        4 * FRAMES_PER_CELL, 0, 
        pygame.sprite.Group(Wall(9, 12, 2, 3))
    )
    assert snacman.get_pos() == (8, 12)

def test_snacman_vertical_collision(snacman):
    snacman.move(
        0, FRAMES_PER_CELL, 
        pygame.sprite.Group(Wall(5, 13, 1, 1))
    )
    assert snacman.get_pos() == (5, 12)

def test_snacman_diagonal_collision(snacman):
    snacman.move(
        -FRAMES_PER_CELL, 2 * FRAMES_PER_CELL, 
        pygame.sprite.Group(Wall(4, 14, 1, 2))
    )
    assert snacman.get_pos() == (4, 13)
