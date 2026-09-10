import pytest
from snacman.constants import GRID_SIZE
from snacman.icy import Icy
from snacman.maze import Maze
from snacman.snacman import SnacMan
from snacman.spicy import Spicy

@pytest.fixture
def icy():
    icy = Icy()
    icy.col, icy.row = (1, 1)
    return icy

@pytest.fixture
def maze():
    return Maze(SnacMan((1, 6)))

@pytest.fixture
def spicy():
    return Spicy()

@pytest.mark.parametrize(
        "spicy_pos, player_pos", 
        [
            ((1, 2), (3, 1)),   # Both near
            ((1, 2), (GRID_SIZE - 2, 1)),   # Spicy near, player far
            ((GRID_SIZE - 2, GRID_SIZE - 2), (3, 1)),  # Spicy far, player near
            ((GRID_SIZE - 2, GRID_SIZE - 2), (GRID_SIZE - 2, 1))    # Both far
        ]
    )
def test_icy_chase_on_with_spicy(icy, maze, spicy, spicy_pos, player_pos):
    spicy.col, spicy.row = spicy_pos
    icy.attack(maze.graph, [icy, spicy], player_pos, True)
    assert (icy.col, icy.row) == (2, 1)

def test_icy_chase_on_without_spicy(icy, maze):
    icy.attack(maze.graph, [icy], (1, 6), True)
    assert (icy.col, icy.row) == (1, 2)

def test_icy_chase_off(icy, maze, spicy):
    spicy.col, spicy.row = (1, 2)
    icy.attack(maze.graph, [icy, spicy], (GRID_SIZE - 2, 1), False)
    assert (icy.col, icy.row) == (2, 1)
