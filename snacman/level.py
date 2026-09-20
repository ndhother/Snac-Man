"""Provides the Level class for running an individual level of the game."""

import pygame
import sys
from snacman.button import Button
from snacman.constants import BLACK, COLOURS, HOME_SIZE
from snacman.display import draw_text, draw_buttons
from snacman.icy import Icy
from snacman.maze import Maze
from snacman.ricey import Ricey
from snacman.snacman import SnacMan
from snacman.spicy import Spicy
from snacman.tango import Tango

START_POS = (1, 1)

FRAME_RATE = 60
LV_5_TIME = 120

ENEMY_MOVE_FRAMES = 25
ENEMY_PATTERN = [8, 28, 35, 55, 60, 80, 85]

class Level:
    def __init__(self, level_num):
        self.level_num = level_num

        self.score = 0
        self.lives = 3

        self.player = SnacMan(START_POS)
        self.enemies = [Spicy()]

        if self.level_num > 1:
            self.enemies.append(Icy())

        if self.level_num > 2:
            self.enemies.append(Tango())

        if self.level_num > 3:
            self.enemies.append(Ricey())

        self.maze = Maze(self.player)
        self.sprites = pygame.sprite.Group(
            self.maze.walls, self.maze.items, self.player, self.enemies
        )
        self.clock = pygame.time.Clock()
        self.total_frames = 0
        self.frames_since_reset = 0

    def play(self, screen):
        """
        Main game loop: updates timer, character positions, lives, and score.
        Returns True if level is won, False if level is lost.
        """
        back_button = Button("BACK", None, x=850, y=35)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                        return None

            self.move_player(pygame.key.get_pressed())
            
            time_spent = self.total_frames // FRAME_RATE
            
            if self.level_num == 5:   # Timer counting down
                remaining_time = LV_5_TIME - time_spent

                if remaining_time <= 0:
                    return False
                
                timer = remaining_time // 60, remaining_time % 60
            
            else:   # Timer counting up
                timer = time_spent // 60, time_spent % 60

            self.move_enemies(time_spent)

            # Deduct 1 life for contact with enemy
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                self.lives -= 1

                if not self.lives:
                    return False

                self.player.reset()

                for e in self.enemies:
                    e.reset()

                self.frames_since_reset = 0

            # Remove item sprites when collected by player
            pygame.sprite.spritecollide(self.player, self.maze.items, True)

            if not self.maze.items:
                self.calc_score(time_spent)
                return True

            self.total_frames += 1
            self.frames_since_reset += 1
            
            screen.fill(BLACK)
            self.sprites.draw(screen)

            draw_buttons(screen, [back_button])
            draw_text(screen, f"Level {self.level_num}", x=675, y=50)

            if self.level_num == 5:
                draw_text(
                    screen, 
                    "TIMED LEVEL (2 mins)", 
                    x=670, 
                    y=180, 
                    colour=COLOURS["RED"]
                )
            draw_text(
                screen, f"Time: {timer[0]:02}:{timer[1]:02}", x=730, y=250
            )
            draw_text(screen, f"Lives: {self.lives}", x=730, y=400)
            
            pygame.display.update()
            self.clock.tick(FRAME_RATE)

    def move_player(self, keys):
        """
        Processes user input via WASD/arrow keys to move Snac-Man.
        """
        x = 0
        y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y += 1

        self.player.move(x, y, self.maze.walls)

    def move_enemies(self, time_spent):
        """
        Moves enemies out of enemy home after a reset and decides whether 
        enemies scatter or attack based on level timer.
        """
        if (
            self.frames_since_reset 
            and self.frames_since_reset % ENEMY_MOVE_FRAMES == 0
        ):
            current_frame = self.frames_since_reset // ENEMY_MOVE_FRAMES

            if current_frame < HOME_SIZE:
                for e in self.enemies:
                    e.exit_home(current_frame)

            else:
                scatter = 0
                for i, time in enumerate(ENEMY_PATTERN, 1):
                    if time_spent < time:
                        scatter = i % 2
                        break

                player_pos = self.player.get_pos()
                enemies_pos = {type(e): (e.col, e.row) for e in self.enemies}

                for e in self.enemies:
                    if scatter:
                        e.scatter(self.maze.graph, enemies_pos)
                    
                    else:
                        e.attack(
                            self.maze.graph, 
                            enemies_pos, 
                            player_pos,
                            current_frame % 2
                        )

                    enemies_pos[type(e)] = (e.col, e.row)

    def calc_score(self, time_spent):
        """
        Determines player score based on number of lives remaining and 
        speed of level completion.
        """
        self.score = 1000

        # Add 250 points if 1 life lost, 500 points if no lives lost
        self.score += (self.lives - 1) * 250

        for i, time in enumerate(range(60, 135, 15)):
            if time_spent < time:
                self.score += 500 - 100 * i
                return
