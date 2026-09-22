"""Provides the Tango enemy subclass and its attack behaviour."""

from snacman.constants import COLOURS
from snacman.enemy import Enemy

class Tango(Enemy):
    def __init__(self):
        super().__init__(COLOURS["ORANGE"], "BOTTOM_LEFT")

    def attack(self, graph, enemies_pos, player_pos, chase):
        """
        Constantly switches between chasing Snac-Man and random movement.
        """
        moves = self.find_possible_moves(graph, enemies_pos)

        if chase:
            self.move_towards(moves, player_pos)
        else:
            self.move_randomly(moves)
