"""Provides the Icy enemy subclass and its attack behaviour."""

from snacman.constants import COLOURS
from snacman.enemy import Enemy
from snacman.spicy import Spicy

CHASE_DIST = 6 ** 2

class Icy(Enemy):
    def __init__(self):
        super().__init__(COLOURS["CYAN"], "BOTTOM_RIGHT")

    def attack(self, graph, enemies_pos, player_pos, chase):
        """
        Chases Snac-Man when close to Spicy and far from Snac-Man.
        Otherwise, constantly switches between chasing and random movement.
        """
        my_pos = (self.col, self.row)
        spicy_pos = enemies_pos.get(Spicy)

        if (
            chase
            or spicy_pos 
            and self.calc_dist(my_pos, spicy_pos) < CHASE_DIST 
            and self.calc_dist(my_pos, player_pos) > CHASE_DIST
        ):
            self.move_towards(graph, enemies_pos, player_pos)
        else:
            self.move_randomly(graph, enemies_pos)
