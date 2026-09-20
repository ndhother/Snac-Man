import pygame
import pytest
from snacman.constants import HOME_SIZE
from snacman.level import Level, START_POS, FRAME_RATE, LV_5_TIME
from snacman.level import ENEMY_PATTERN, ENEMY_MOVE_FRAMES

@pytest.fixture
def level():
    return Level(5)

@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    pygame.init()
    yield
    pygame.quit()

def enemy_positions(enemies):
    return {type(e): (e.col, e.row) for e in enemies}

def test_level_player_start_pos(level):
    assert level.player.get_pos() == START_POS

@pytest.mark.parametrize(
        "level_num, num_enemies", 
        [(1, 1), (2, 2), (3, 3), (4, 4), (5, 4)]
    )
def test_level_enemies(level_num, num_enemies):
    assert len(Level(level_num).enemies) == num_enemies

def test_level_5_times_out(level):
    level.total_frames = LV_5_TIME * FRAME_RATE
    assert level.play(None) is False

def test_level_won_when_no_items(level):
    level.maze.items.empty()
    assert level.play(None) is True

@pytest.mark.parametrize("frame", [0, 1, 24, 26, 49, 51])
def test_move_enemies_at_inactive_frames(level, frame):
    initial_positions = [(e.col, e.row) for e in level.enemies]
    level.frames_since_reset = frame

    level.move_enemies(None)
    assert [(e.col, e.row) for e in level.enemies] == initial_positions

def test_move_enemies_at_exit_home_frames(level):
    for move in range(1, HOME_SIZE):
        initial_positions = [(e.col, e.row) for e in level.enemies]
        level.frames_since_reset = move * ENEMY_MOVE_FRAMES

        level.move_enemies(None)
        assert [(e.col, e.row) for e in level.enemies] != initial_positions

def test_move_enemies_at_scatter_frames(level):
    level_copy = Level(5)

    for move in range(1, HOME_SIZE):
        frame = move * ENEMY_MOVE_FRAMES
        level.frames_since_reset = level_copy.frames_since_reset = frame

        level.move_enemies(None)
        level_copy.move_enemies(None)

    frame = HOME_SIZE * ENEMY_MOVE_FRAMES
    level.frames_since_reset = level_copy.frames_since_reset = frame

    for _ in range(3):
        level.move_enemies(ENEMY_PATTERN[0] - 1)
        expected_positions = [(e.col, e.row) for e in level.enemies]

        for e in level_copy.enemies:
            e.scatter(level.maze.graph, enemy_positions(level_copy.enemies))

        assert (
            [(e.col, e.row) for e in level_copy.enemies] == expected_positions
        )

def test_move_enemies_at_attack_frames(level):
    level_copy = Level(5)

    for move in range(1, HOME_SIZE):
        frame = move * ENEMY_MOVE_FRAMES
        level.frames_since_reset = level_copy.frames_since_reset = frame

        level.move_enemies(None)
        level_copy.move_enemies(None)

    # Choose an odd frame so the attack() chase argument is True (= 1)
    frame = (HOME_SIZE + HOME_SIZE % 2 + 1) * ENEMY_MOVE_FRAMES
    level.frames_since_reset = level_copy.frames_since_reset = frame

    for _ in range(3):
        level.move_enemies(ENEMY_PATTERN[0] + 1)
        expected_positions = [(e.col, e.row) for e in level.enemies]

        for e in level_copy.enemies:
            e.attack(
                level.maze.graph, 
                enemy_positions(level_copy.enemies), 
                level.player.get_pos(), 
                1
            )

        assert (
            [(e.col, e.row) for e in level_copy.enemies] == expected_positions
        )

@pytest.mark.parametrize(
        "lives, time_spent, score_bonus",
        [
            (1, 0, 500),
            (2, 0, 750),
            (3, 0, 1000),
            (3, 59, 1000),
            (1, 60, 400),
            (2, 60, 650),
            (3, 60, 900),
            (3, 74, 900),
            (1, 75, 300),
            (2, 75, 550),
            (3, 75, 800),
            (3, 89, 800),
            (1, 90, 200),
            (2, 90, 450),
            (3, 90, 700),
            (3, 104, 700),
            (1, 105, 100),
            (2, 105, 350),
            (3, 105, 600),
            (3, 119, 600),
            (1, 120, 0),
            (2, 120, 250),
            (3, 120, 500),
            (3, 135, 500),
        ]
    )
def test_calc_score(level, lives, time_spent, score_bonus):
    level.lives = lives
    level.calc_score(time_spent)

    assert level.score == 1000 + score_bonus
