import pytest
from snacman.maze import Maze
from snacman.snacman import SnacMan
from snacman.spicy import Spicy

@pytest.fixture
def spicy():
    spicy = Spicy()
    spicy.col, spicy.row = (1, 1)
    return spicy

@pytest.fixture
def maze():
    return Maze(SnacMan((1, 9)))

def test_spicy_attack(spicy, maze):
    for y in range(2, 10):
        spicy.attack(maze.graph, [spicy], (1, 9), None)
        assert (spicy.col, spicy.row) == (1, y)
