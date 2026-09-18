"""Provides the Ricey enemy subclass and its attack behaviour."""

from snacman.constants import COLOURS
from snacman.enemy import Enemy

class Ricey(Enemy):
    def __init__(self):
        super().__init__(COLOURS["PINK"], "TOP_LEFT")

    def attack(self, graph, enemies_pos, player_pos, _):
        """
        Always chases Snac-Man but prioritises getting to the same row.
        """
        if player_pos[1] != self.row and (self.col, player_pos[1]) in graph:
            target = (self.col, player_pos[1])
        else:
            target = player_pos

        self.move_towards(graph, enemies_pos, target)
