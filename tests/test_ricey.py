import pytest
from snacman.constants import GRID_SIZE, HOME_START
from snacman.maze import Maze
from snacman.ricey import Ricey
from snacman.snacman import SnacMan

@pytest.fixture
def ricey():
    ricey = Ricey()
    ricey.col, ricey.row = (1, 1)
    return ricey

@pytest.fixture
def maze():
    return Maze(SnacMan((6, 3)))

def test_ricey_when_player_in_same_row(ricey, maze):
    ricey.attack(maze.graph, [ricey], (8, 1), None)
    assert (ricey.col, ricey.row) == (2, 1)

def test_ricey_when_player_row_reachable(ricey, maze):
    ricey.attack(maze.graph, [ricey], (3, GRID_SIZE - 2), None)
    assert (ricey.col, ricey.row) == (1, 2)

def test_ricey_when_player_row_unreachable(ricey, maze):
    ricey.col, ricey.row = (HOME_START, 1)
    ricey.attack(maze.graph, [ricey], (GRID_SIZE - 2, HOME_START), None)

    # Player is far enough right that moving right is closer than moving down
    assert (ricey.col, ricey.row) != (HOME_START, 2)
