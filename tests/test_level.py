import pygame
import pytest
from snacman.constants import HOME_SIZE
from snacman.level import Level, START_POS, FRAME_RATE, LV_5_TIME
from snacman.level import ENEMY_PATTERN, ENEMY_MOVE_FRAMES

@pytest.fixture
def level():
    return Level(5, 100)

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
    pygame.init()
    try:
        level.total_frames = LV_5_TIME * FRAME_RATE
        assert level.play(None) is False
    finally:
        pygame.quit()

def test_level_won_when_no_items(level):
    pygame.init()
    try:
        level.maze.items.empty()
        assert level.play(None) is True
    finally:
        pygame.quit()

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
        "time_spent, bonus",
        [
            (0, 5000),
            (59, 5000),
            (60, 4000),
            (74, 4000),
            (75, 3000),
            (89, 3000),
            (90, 2000),
            (104, 2000),
            (105, 1000),
            (119, 1000),
            (120, 0),
        ]
    )
def test_add_bonus_points(level, time_spent, bonus):
    level.add_bonus_points(time_spent)
    assert level.score == 100 + bonus
