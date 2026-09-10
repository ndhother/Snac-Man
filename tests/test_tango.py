import pytest
from snacman.maze import Maze
from snacman.snacman import SnacMan
from snacman.tango import Tango

@pytest.fixture
def tango():
    tango = Tango()
    tango.col, tango.row = (1, 1)
    return tango

@pytest.fixture
def maze():
    return Maze(SnacMan((4, 5)))

def test_tango_chase_on(tango, maze):
    tango.attack(maze.graph, [tango], (5, 1), True)
    assert (tango.col, tango.row) == (2, 1)
