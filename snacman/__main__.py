"""Runs Snac-Man and controls the game's menu navigation."""

import pygame
import sys
from snacman.button import Button
from snacman.constants import SCREEN_SIZE, BLACK, COLOURS
from snacman.display import draw_text, draw_buttons
from snacman.level import Level

GAME_NAME = "Snac-Man"
MENU_BUTTON_WIDTH = 220
ENEMIES = [COLOURS["RED"], COLOURS["PINK"], COLOURS["CYAN"], COLOURS["ORANGE"]]

def process_events(buttons, pos):
    """
    Uses pygame event queue to process clicks on Button objects or quit app.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                if b.rect.collidepoint(pos):
                    return b.choice

    return None

def main_menu():
    """
    Displays main menu with PLAY GAME, INSTRUCTIONS and QUIT buttons. 
    """
    buttons = [
        Button("PLAY GAME", play_game, y=250, width=MENU_BUTTON_WIDTH),
        Button("INSTRUCTIONS", instructions, y=350, width=MENU_BUTTON_WIDTH),
        Button("QUIT", quit_game, y=450, width=MENU_BUTTON_WIDTH)
    ]
    while True:
        pos = pygame.mouse.get_pos()
        choice = process_events(buttons, pos)

        if choice:
            return choice
        
        screen.fill(BLACK)
        draw_text(screen, GAME_NAME.upper(), y=125)
        draw_buttons(screen, buttons, pos)

        pygame.display.update()

# def level_select():
#     buttons = [
#         Button(str(x), x, x=150 * x + 25, y=300, width=50, height=50) 
#         for x in range(1, 6)
#     ]
#     while True:
#         pos = pygame.mouse.get_pos()
#         choice = process_events(buttons, pos)

#         if choice:
#             return lambda: play_game(Level(choice))
        
#         screen.fill(BLACK)
#         draw_text(screen, "Choose level:", y=150)
#         draw_buttons(screen, buttons, pos)

#         pygame.display.update()

def play_game():
    """
    Runs levels 1 through 5. Calls game_over(False) if a level is lost.
    Calls game_over(True, final score) if all levels are won.
    """
    score = 0

    for level_num in range(1, 6):
        level = Level(level_num, score)
        win = level.play(screen)
        score = level.score

        if not win:
            return game_over(False)

    return game_over(True, score)

def instructions():
    """
    Displays basic instructions page. BACK button returns user to main menu.
    """
    buttons = [Button("BACK", main_menu, x=50, y=35)]
    
    while True:
        pos = pygame.mouse.get_pos()
        choice = process_events(buttons, pos)

        if choice:
            return choice
        
        screen.fill(BLACK)
        draw_text(screen, "INSTRUCTIONS", y=50)
        draw_buttons(screen, buttons, pos)

        draw_text(
            screen, 
            "Use the arrow keys or WASD to move Snac-Man around the maze", 
            x=100, y=150
        )
        pygame.draw.rect(screen, COLOURS["YELLOW"], [860, 145, 40, 40])

        draw_text(screen, "These are your enemies:", y=225)

        for i, e in enumerate(ENEMIES):
            pygame.draw.rect(screen, e, [120 * i + 300, 300, 40, 40])

        draw_text(screen, "Avoid them or you will lose lives!", y=375)
        draw_text(screen, "You begin each level with 3 lives", y=425)

        draw_text(
            screen, "Collect all the dots to win the level", x=200, y=500
        )
        for x in range(615, 775, 20):
            pygame.draw.rect(screen, COLOURS["YELLOW"], [x, 515, 4, 4])

        pygame.display.update()

def game_over(win, score=None):
    """
    Displays lose message or win message and final score. 
    MAIN MENU button returns user to main menu.
    """
    buttons = [Button("MAIN MENU", main_menu, y=350)]

    while True:
        pos = pygame.mouse.get_pos()
        choice = process_events(buttons, pos)

        if choice:
            return choice
        
        screen.fill(BLACK)

        if win:
            draw_text(screen, "YOU WIN!", y=150)
            draw_text(screen, f"Your final score is {score}", y=250)
        else:
            draw_text(screen, "YOU LOSE", y=200)

        draw_buttons(screen, buttons, pos)

        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(GAME_NAME)

    next_page = main_menu()

    while next_page:
        next_page = next_page()
