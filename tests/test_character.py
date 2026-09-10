import pytest
from snacman.character import Character
from snacman.constants import CELL_SIZE

@pytest.fixture
def character():
    return Character(3, 8, (0, 0, 0))

def test_character_start_pos(character):
    assert (character.col, character.row) == character.start_pos == (3, 8)

    assert character.rect.x // CELL_SIZE == character.col
    assert character.rect.y // CELL_SIZE == character.row

def test_character_reset(character):
    character.col = 10
    character.row = 4
    character.rect.x = 100
    character.rect.y = 200

    character.reset()

    assert (character.col, character.row) == character.start_pos == (3, 8)

    assert character.rect.x // CELL_SIZE == character.col
    assert character.rect.y // CELL_SIZE == character.row
