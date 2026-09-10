"""Provides the Tango enemy subclass and its attack behaviour."""

from snacman.constants import COLOURS
from snacman.enemy import Enemy

class Tango(Enemy):
    def __init__(self):
        super().__init__(COLOURS["ORANGE"], "BOTTOM_LEFT")

    def attack(self, graph, enemies, player_pos, chase):
        """
        Constantly switches between chasing Snac-Man and random movement.
        """
        if chase:
            self.move_towards(graph, enemies, player_pos)
        else:
            self.move_randomly(graph, enemies)
