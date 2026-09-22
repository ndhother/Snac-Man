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
        moves = self.find_possible_moves(graph, enemies_pos)

        same_row_cell = (self.col, player_pos[1])
        target = (
            same_row_cell 
            if player_pos[1] != self.row and same_row_cell in graph 
            else player_pos
        )
        self.move_towards(moves, target)
