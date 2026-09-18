"""Provides the base Enemy class and shared enemy behaviour."""

import random
from snacman.character import Character
from snacman.constants import CELL_SIZE, MAZE_CORNERS, HOME_CORNERS

SCATTER_DIST = 5 ** 2

class Enemy(Character):
    def __init__(self, colour, corner):
        super().__init__(*HOME_CORNERS[corner], colour)
        self.corner = corner

    def move_x(self, steps):
        """
        Updates position in x direction (column) by number of steps.
        Positive: right, negative: left.
        """
        self.rect.x += steps * CELL_SIZE
        self.col += steps

    def move_y(self, steps):
        """
        Updates position in y direction (row) by number of steps.
        Positive: down, negative: up.
        """
        self.rect.y += steps * CELL_SIZE
        self.row += steps
    
    def exit_home(self, frame):
        """
        Moves enemy upwards and out of enemy home. 
        On frame 3, enemies in the upper corners move to the left or the right.
        """
        if frame == 3:
            if self.corner == "TOP_LEFT":
                return self.move_x(-1)

            elif self.corner == "TOP_RIGHT":
                return self.move_x(1)

        if frame < 3 or self.corner.startswith("BOTTOM"):
            self.move_y(-1)

    def scatter(self, graph, enemies_pos):
        """
        Moves enemy towards assigned maze corner or randomly when close enough.
        """
        corner_pos = MAZE_CORNERS[self.corner]

        if self.calc_dist(corner_pos, (self.col, self.row)) < SCATTER_DIST:
            self.move_randomly(graph, enemies_pos)
        else:
            self.move_towards(graph, enemies_pos, corner_pos)

    def calc_dist(self, node_a, node_b):
        """
        Returns the squared Euclidean distance between two grid cells.
        """
        return (node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2

    def move_randomly(self, graph, enemies_pos):
        """
        Chooses a random neighbouring node to move to.
        """
        self.adjacent_move(
            random.choice(graph[(self.col, self.row)]), enemies_pos
        )

    def move_towards(self, graph, enemies_pos, target):
        """
        Moves towards the neighbouring node closest to the target.
        """
        new_pos = min(
            graph[(self.col, self.row)], 
            key=lambda pos: self.calc_dist(target, pos)
        )
        self.adjacent_move(new_pos, enemies_pos)

    def adjacent_move(self, new_pos, enemies_pos):
        """
        Moves to an adjacent node if it is not occupied by another enemy.
        """
        if any(new_pos == pos for pos in enemies_pos.values()):
            return

        if new_pos[0] < self.col:
            self.move_x(-1)

        elif new_pos[0] > self.col:
            self.move_x(1)

        elif new_pos[1] < self.row:
            self.move_y(-1)

        elif new_pos[1] > self.row:
            self.move_y(1)
