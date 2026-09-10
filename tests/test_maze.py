import pytest
from snacman.constants import BLACK, GRID_SIZE, CELL_SIZE, HOME_SIZE
from snacman.constants import HOME_START, HOME_END, EMPTY_CELL, WALL
from snacman.maze import Maze, MAX_WALL_SIZE
from snacman.snacman import SnacMan
from snacman.wall import Wall

@pytest.fixture
def maze():
    return Maze(SnacMan((2, 4)))

@pytest.fixture
def empty_cells(maze):
    return {
        (col, row) 
        for row in range(len(maze.grid))
        for col in range(len(maze.grid[row]))
        if maze.grid[row][col] == EMPTY_CELL
    }

def test_grid_size(maze):
    assert len(maze.grid) == GRID_SIZE

    for row in maze.grid:
        assert len(row) == GRID_SIZE

def test_maze_top_border(maze):
    for cell in maze.grid[0]:
        assert cell == WALL

def test_maze_bottom_border(maze):
    for cell in maze.grid[-1]:
        assert cell == WALL

def test_maze_left_border(maze):
    for row in maze.grid:
        assert row[0] == WALL

def test_maze_right_border(maze):
    for row in maze.grid:
        assert row[-1] == WALL

def test_maze_outer_corridors(maze):
    for i in range(1, GRID_SIZE - 1):
        assert maze.grid[1][i] == EMPTY_CELL
        assert maze.grid[-2][i] == EMPTY_CELL
        assert maze.grid[i][1] == EMPTY_CELL
        assert maze.grid[i][-2] == EMPTY_CELL

def test_enemy_home_side_walls(maze):
    for row in range(HOME_START, HOME_END):
        assert maze.grid[row][HOME_START] == WALL
        assert maze.grid[row][HOME_END] == WALL

def test_enemy_home_bottom_wall(maze):
    for col in range(HOME_START, HOME_END):
        assert maze.grid[HOME_END][col] == WALL

def test_enemy_home_is_blocked(maze):
    for col in range(HOME_START, HOME_END):
        assert maze.grid[HOME_START][col] != EMPTY_CELL

def test_player_start_pos_is_empty(maze):
    assert maze.grid[4][2] == EMPTY_CELL

def test_wall_cannot_be_placed_on_player(maze):
    col, row = maze.player.get_pos()
    assert maze.can_place_wall(Wall(col, row, 1, 1), maze.walls) is False

def test_maze_add_wall(maze):
    num_walls = len(maze.walls)
    col, row = maze.player.get_pos()
    maze.add_wall(Wall(col, row, 1, 1), maze.walls)

    assert maze.grid[row][col] == WALL
    assert len(maze.walls) == num_walls + 1

def test_maze_wall_size(maze):
    for wall in maze.walls:
        if (
            wall.width != GRID_SIZE 
            and wall.width != HOME_SIZE 
            and wall.image.get_at((0, 0))[:3] != BLACK
        ):
            assert 1 <= wall.width <= MAX_WALL_SIZE

        if wall.height != GRID_SIZE and wall.height != HOME_SIZE:
            assert 1 <= wall.height <= MAX_WALL_SIZE

def test_graph_contains_only_empty_cells(maze, empty_cells):
    assert set(maze.graph) == empty_cells

def test_graph_neighbours_are_adjacent(maze):
    for node, neighbours in maze.graph.items():
        for neighbour in neighbours:
            dist = abs(node[0] - neighbour[0]) + abs(node[1] - neighbour[1])
            assert dist == 1

def test_graph_edges_are_bidirectional(maze):
    for node, neighbours in maze.graph.items():
        for neighbour in neighbours:
            assert node in maze.graph[neighbour]

def test_maze_is_fully_traversable(maze, empty_cells):
    reachable_cells = {maze.player.get_pos()}
    visited = set()

    while reachable_cells:
        pos = reachable_cells.pop()

        if pos not in visited:
            visited.add(pos)

            for neighbour in maze.graph[pos]:
                reachable_cells.add(neighbour)

    assert visited == empty_cells

def test_items_are_only_in_empty_cells(maze, empty_cells):
    item_cells = {
        (item.rect.x // CELL_SIZE, item.rect.y // CELL_SIZE) 
        for item in maze.items
    }
    empty_cells.discard(maze.player.get_pos())

    assert item_cells == empty_cells
