import pytest
from snacman.constants import HOME_START, MAZE_CORNERS, HOME_CORNERS
from snacman.constants import EMPTY_CELL
from snacman.enemy import Enemy, SCATTER_DIST
from snacman.maze import Maze
from snacman.snacman import SnacMan

@pytest.fixture
def enemy():
    return Enemy((0, 0, 0), "TOP_LEFT")

@pytest.fixture
def enemy_2():
    return Enemy((0, 0, 0), "BOTTOM_RIGHT")

@pytest.fixture
def maze():
    return Maze(SnacMan((7, 7)))

def enemy_positions(enemies):
    return {i: (enemy.col, enemy.row) for i, enemy in enumerate(enemies, 1)}

def test_enemy_start_pos(enemy):
    assert (enemy.col, enemy.row) == HOME_CORNERS["TOP_LEFT"]

def test_enemy_exit_home(enemy, enemy_2):
    for frame in range(1, 6):
        enemy.exit_home(frame)
        enemy_2.exit_home(frame)

    assert enemy.col == HOME_CORNERS["TOP_LEFT"][0] - 1
    assert enemy.row == HOME_CORNERS["TOP_LEFT"][1] - 2

    assert enemy_2.col == HOME_CORNERS["BOTTOM_RIGHT"][0]
    assert enemy_2.row == HOME_CORNERS["BOTTOM_RIGHT"][1] - 5

@pytest.mark.parametrize(
        "node_a, node_b, dist", 
        [
            ((11, 7), (1, 7), 10 ** 2), 
            ((8, 4), (8, 6), 2 ** 2), 
            ((5, 5), (2, 9), 5 ** 2), 
            ((3, 3), (3, 3), 0)
        ]
    )
def test_enemy_calc_dist(enemy, node_a, node_b, dist):
    assert enemy.calc_dist(node_a, node_b) == dist

def test_enemy_scatter(enemy, maze):
    corner_pos = MAZE_CORNERS[enemy.corner]
    enemy.col, enemy.row = MAZE_CORNERS["BOTTOM_RIGHT"]

    dist = enemy.calc_dist(corner_pos, (enemy.col, enemy.row))
    assert dist > SCATTER_DIST

    enemy.scatter(maze.graph, enemy_positions([enemy]))
    assert enemy.calc_dist(corner_pos, (enemy.col, enemy.row)) < dist

def test_enemy_possible_moves(enemy, maze):
    enemy.col, enemy.row = (4, 1)
    moves = enemy.find_possible_moves(maze.graph, enemy_positions([enemy]))
    
    assert (3, 1) in moves and (5, 1) in moves

    if maze.grid[2][4] == EMPTY_CELL:
        assert (4, 2) in moves

def test_enemy_does_not_move_onto_enemy(enemy, enemy_2, maze):
    enemy.col, enemy.row = (1, 1)
    enemy_2.col, enemy_2.row = (1, 2)

    assert (1, 2) not in enemy.find_possible_moves(
        maze.graph, enemy_positions([enemy, enemy_2])
    )

def test_enemy_move_randomly(enemy, maze):
    enemy.col, enemy.row = (1, 1)

    for _ in range(10):
        pos = (enemy.col, enemy.row)
        enemy.move_randomly(
            enemy.find_possible_moves(maze.graph, enemy_positions([enemy]))
        )
        assert maze.grid[enemy.row][enemy.col] == EMPTY_CELL
        assert enemy.calc_dist(pos, (enemy.col, enemy.row)) == 1

def test_enemy_move_randomly_no_moves(enemy):
    enemy.col, enemy.row = (1, 1)
    enemy.move_randomly([])
    
    assert (enemy.col, enemy.row) == (1, 1)

def test_enemy_move_towards_horizontal(enemy, maze):
    enemy.col, enemy.row = (2, 1)
    enemy.move_towards(
        enemy.find_possible_moves(maze.graph, enemy_positions([enemy])), (8, 1)
    )
    assert (enemy.col, enemy.row) == (3, 1)

def test_enemy_move_towards_vertical(enemy, maze):
    enemy.col, enemy.row = (1, 6)
    enemy.move_towards(
        enemy.find_possible_moves(maze.graph, enemy_positions([enemy])), (1, 2)
    )
    assert (enemy.col, enemy.row) == (1, 5)

def test_enemy_move_towards_no_moves(enemy):
    enemy.col, enemy.row = (1, 1)
    enemy.move_towards([], None)

    assert (enemy.col, enemy.row) == (1, 1)

def test_enemy_stays_within_graph(enemy, maze):
    enemy.col, enemy.row = (HOME_START - 1, HOME_START)
    enemy.move_towards(
        enemy.find_possible_moves(maze.graph, enemy_positions([enemy])), 
        (HOME_START + 1, HOME_START)
    )
    assert (enemy.col, enemy.row) != (HOME_START, HOME_START)

def test_enemy_adjacent_move(enemy):
    enemy.col, enemy.row = (1, 1)
    enemy.adjacent_move((1, 2))

    assert (enemy.col, enemy.row) == (1, 2)
