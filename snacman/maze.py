"""Provides the Maze class for generating and managing game mazes."""

import pygame
import random
from snacman.constants import GRID_SIZE, CELL_SIZE
from snacman.constants import HOME_SIZE, HOME_START, HOME_END
from snacman.constants import EMPTY_CELL, WALL, ENEMY_TERRITORY
from snacman.item import Item
from snacman.wall import Wall

MAX_WALL_SIZE = 6

class Maze:
    def __init__(self, player):
        self.grid = [[EMPTY_CELL] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.player = player

        self.walls = self.create_walls()
        self.graph = self.build_graph()
        self.items = self.place_items()

    # grid[row][col] --> Matrix access
    # (x, y) --> Game coordinate
    # (col, row) --> Converting between them

    def create_walls(self):
        """
        Places walls to create a maze, starting with borders and enemy home.
        Fills remaining space with randomly generated walls.
        """
        wall_sprites = pygame.sprite.Group()

        borders = [
            Wall(0, 0, GRID_SIZE, 1),               # top
            Wall(0, GRID_SIZE - 1, GRID_SIZE, 1),   # bottom
            Wall(0, 0, 1, GRID_SIZE),               # left
            Wall(GRID_SIZE - 1, 0, 1, GRID_SIZE),   # right
        ]

        enemy_home = [
            Wall(HOME_START, HOME_START, 1, HOME_SIZE),     # left
            Wall(HOME_END, HOME_START, 1, HOME_SIZE),       # right
            Wall(HOME_START, HOME_END, HOME_SIZE, 1)        # bottom  
        ]

        for wall in borders + enemy_home:
            self.add_wall(wall, wall_sprites)

        for row in range(HOME_START, HOME_END):
            for col in range(HOME_START + 1, HOME_END):
                self.grid[row][col] = ENEMY_TERRITORY

        # Invisible wall to block player entry to enemy home (top)
        wall_sprites.add(
            Wall(HOME_START + 1, HOME_START, HOME_SIZE - 2, 1, visible=False)
        )

        spaces = {
            (col, row) 
            for row in range(2, GRID_SIZE - 2) 
            for col in range(2, GRID_SIZE - 2) 
            if self.grid[row][col] == EMPTY_CELL
        }
        spaces.discard(self.player.get_pos())

        while spaces:
            # Choose random position + orientation for new wall
            col, row = random.choice(tuple(spaces))
            vertical = random.choice([True, False])

            wall_size = MAX_WALL_SIZE

            while wall_size:
                width = wall_size if vertical else 1
                height = 1 if vertical else wall_size

                wall = Wall(col, row, width, height)

                if self.can_place_wall(wall, wall_sprites):
                    self.add_wall(wall, wall_sprites, spaces)
                    break

                # Decrease size until it reaches 0 or wall is added
                wall_size -= 1

            spaces.discard((col, row))

        return wall_sprites

    def can_place_wall(self, new_wall, wall_sprites):
        """
        Returns True if new wall does not touch Snac-Man or any existing walls.
        """
        if new_wall.rect.colliderect(self.player.rect):
            return False

        # Add 1 cell of padding to each edge
        padded = new_wall.rect.inflate(CELL_SIZE * 2, CELL_SIZE * 2)

        return not any(padded.colliderect(w.rect) for w in wall_sprites)

    def add_wall(self, wall, wall_sprites, spaces=None):
        """
        Adds a wall to the sprite group and marks its cells as occupied.
        Optionally removes occupied cells from the candidate spaces.
        """
        wall_sprites.add(wall)

        for row in range(wall.row, wall.row + wall.height):
            for col in range(wall.col, wall.col + wall.width):
                self.grid[row][col] = WALL

                if spaces is not None:
                    spaces.discard((col, row))

    def build_graph(self):
        """
        Creates graph node for every empty grid cell.
        Returns dictionary mapping each node to a list of neighbouring nodes.
        """
        graph = {
            (col, row): []
            for row in range(GRID_SIZE) 
            for col in range(GRID_SIZE) 
            if self.grid[row][col] == EMPTY_CELL
        }
        for node in graph:
            for neighbour in [
                (node[0], node[1] - 1),   # top
                (node[0] - 1, node[1]),   # left
                (node[0] + 1, node[1]),   # right
                (node[0], node[1] + 1)    # bottom
            ]:
                if neighbour in graph:
                    graph[node].append(neighbour)

        return graph

    def place_items(self):
        """
        Places an item in every empty cell except player's starting position.
        """
        return pygame.sprite.Group(
            Item(*pos) for pos in self.graph if pos != self.player.get_pos()
        )
