"""Provides the Spicy enemy subclass and its attack behaviour."""

from snacman.constants import COLOURS
from snacman.enemy import Enemy

class Spicy(Enemy):
    def __init__(self):
        super().__init__(COLOURS["RED"], "TOP_RIGHT")

    def attack(self, graph, enemies_pos, player_pos, _):
        """
        Always chases Snac-Man.
        """
        self.move_towards(
            self.find_possible_moves(graph, enemies_pos), player_pos
        )
