#========================================
# There are better ways to write this code
# Most of the design choices here were inherited
# from porting from .lua to .py
#========================================

import pygame
pygame.init()

from math import floor
from typing import Dict, List
from enemy import *
from button import *
from states import *
from globals import *

game = Game()

MEDIUM = "medium"
LARGE = "large"
MASSIVE = "massive"
fonts = {
    MEDIUM: pygame.font.SysFont("Lucida Sans", 16),
    LARGE: pygame.font.SysFont("Lucida Sans", 24),
    MASSIVE: pygame.font.SysFont("Lucida Sans", 60),
}

player = Player()

MENU_STATE = "menu_state"
ENDED_STATE = "ended_state"
PLAY_GAME = "play_game"
SETTINGS = "settings"
EXIT_GAME = "exit_game"
REPLAY_GAME = "replay_game"
MENU = "menu"
buttons: Dict[str, Dict[str, Button]] = {
    MENU_STATE: {
        PLAY_GAME: None,
        SETTINGS: None,
        EXIT_GAME: None,
    },
    ENDED_STATE: {
        REPLAY_GAME: None,
        MENU: None,
        EXIT_GAME: None,
    },
}

enemies:List[Enemy] = []

#========================================
# Translated functions
#========================================
def change_game_state(state):
    game.state = state

    #pygame.event.set_grab(state == Game.State.RUNNING)

    if state == Game.State.PAUSED:
        player.paused_x, player.paused_y = player.x, player.y

def set_config():
    pygame.display.set_caption("Save the Ball")
    pygame.mouse.set_visible(False)

def load_enemies():
    global enemies
    enemies = [ Chaser(1) ]

def start_new_game():
    change_game_state(Game.State.RUNNING)

    game.score = 0
    game.curr_level = 0

    load_enemies()

def load_buttons():
    quit_event = pygame.event.Event(pygame.QUIT, {})

    buttons[MENU_STATE][PLAY_GAME] = Button("Play Game", start_new_game, None, 150, 45)
    buttons[MENU_STATE][SETTINGS] = Button("Settings", None, None, 150, 45)
    buttons[MENU_STATE][EXIT_GAME] = Button("Exit Game", pygame.event.post, quit_event, 150, 45)

    buttons[ENDED_STATE][REPLAY_GAME] = Button("Replay", start_new_game, None, 100, 45)
    buttons[ENDED_STATE][MENU] = Button("Menu", change_game_state, Game.State.MENU, 100, 45)
    buttons[ENDED_STATE][EXIT_GAME] = Button("Quit", pygame.event.post, quit_event, 100, 45)

def update_player_pos():
    player.x, player.y = pygame.mouse.get_pos()

def update_enemies(dt):
    if game.state == Game.State.RUNNING:
        for enemy in enemies:
            if not enemy.check_touched(player.x, player.y, player.radius):
                enemy.move(player.x, player.y, dt)
            else:
                player.died_x, player.died_y = player.x, player.y
                change_game_state(Game.State.ENDED)
                return

        if floor(game.score) != game.curr_level:
            game.curr_level = floor(game.score)

            new_enemy = None
            if game.curr_level % 10 == 0:
                enemy_level = game.difficulty * len(enemies) + 1

                if game.curr_level % 60 == 0:
                    new_enemy = Chaser(enemy_level)
                elif game.curr_level % 40 == 0:
                    new_enemy = Bully(enemy_level)
                elif game.curr_level % 20 == 0:
                    new_enemy = Switcher(enemy_level)
                else:
                    new_enemy = Roamer(enemy_level)
            if new_enemy:
                enemies.append(new_enemy)

def update_score(dt):
    if game.state == Game.State.RUNNING:
        game.score += dt

def set_default_font():
    global default_font
    default_font = fonts[MEDIUM]

def draw_enemies():
    if game.state in [Game.State.RUNNING, Game.State.PAUSED, Game.State.ENDED]:
        for enemy in enemies:
            enemy.draw(WIN)

def draw_score():
    if game.state in [Game.State.RUNNING, Game.State.PAUSED]:
        score_text = fonts[LARGE].render(f"Score: {game.curr_level}", 1, WHITE)
        WIN.blit(score_text, ((WIDTH - score_text.get_width()) / 2, 10))

def draw_menus():
    if game.state == Game.State.MENU:
        title_text = fonts[MASSIVE].render("Save the Ball", 1, WHITE)
        WIN.blit(title_text, ((WIDTH - title_text.get_width()) / 2, 20))
        
        desc_text = fonts[MEDIUM].render("Move the ball using your mouse cursor and avoid touching the enemies for as long as you can!", 1, WHITE)
        WIN.blit(desc_text, ((WIDTH - desc_text.get_width()) / 2, 50 + fonts[MASSIVE].get_linesize()))

        buttons[MENU_STATE][PLAY_GAME].draw(WIN, WIDTH / 2 - 75, HEIGHT / 2, 10, 15)
        buttons[MENU_STATE][EXIT_GAME].draw(WIN, WIDTH / 2 - 75, HEIGHT / 2 + 55, 10, 15)
    elif game.state == Game.State.ENDED:
        fade_sur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        fade_sur.fill((0, 0, 0, 128))
        WIN.blit(fade_sur, (0, 0))
        
        global default_font
        default_font = fonts[LARGE]

        buttons[ENDED_STATE][REPLAY_GAME].draw(WIN, WIDTH / 2 - 50, HEIGHT / 1.8, 10, 10)
        buttons[ENDED_STATE][MENU].draw(WIN, WIDTH / 2 - 50, HEIGHT / 1.53, 10, 10)
        buttons[ENDED_STATE][EXIT_GAME].draw(WIN, WIDTH / 2 - 50, HEIGHT / 1.33, 10, 10)

        game_over_text = fonts[MASSIVE].render("Game Over", 1, WHITE)
        WIN.blit(game_over_text, ((WIDTH - game_over_text.get_width()) / 2, HEIGHT / 3 - fonts[MASSIVE].get_linesize()))

        score_text = fonts[LARGE].render(f"Score: {game.curr_level}", 1, WHITE)
        WIN.blit(score_text, ((WIDTH - score_text.get_width()) / 2, HEIGHT / 3))
    elif game.state == Game.State.PAUSED:
        fade_sur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        fade_sur.fill((0, 0, 0, 128))
        WIN.blit(fade_sur, (0, 0))
        #pygame.draw.rect(WIN, (0, 0, 0, 128), (0, 0, WIDTH, HEIGHT))

        pause_text = fonts[MASSIVE].render("Game Paused", 1, WHITE)
        WIN.blit(pause_text, ((WIDTH - pause_text.get_width()) / 2, HEIGHT / 2 - fonts[MASSIVE].get_linesize()))

        pause_desc_text = fonts[MEDIUM].render("Click on the center of the player ball to resume", 1, WHITE)
        WIN.blit(pause_desc_text, ((WIDTH - pause_desc_text.get_width()) / 2, HEIGHT / 2 + fonts[MASSIVE].get_linesize()))

def draw_fps_counter(fps):
    fps_text = fonts[MEDIUM].render(f"FPS: {fps}", 1, WHITE)
    WIN.blit(fps_text, (10, HEIGHT - 26))

def draw_player():
    if game.state == Game.State.PAUSED:
        fade_sur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        pygame.draw.circle(fade_sur, (255, 255, 255, 128), (player.paused_x, player.paused_y), player.radius)
        WIN.blit(fade_sur, (0, 0))

    if game.state == Game.State.ENDED:
        fade_sur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        pygame.draw.circle(fade_sur, (255, 255, 255, 128), (player.died_x, player.died_y), player.radius)
        WIN.blit(fade_sur, (0, 0))

    active_radius = player.radius / (1 if game.state == Game.State.RUNNING else 2)
    pygame.draw.circle(WIN, WHITE, (player.x, player.y), active_radius)

#========================================
# Equivalents to Lua's Love2D main hooks
#========================================
def load():
    change_game_state(Game.State.MENU)
    set_config()
    load_buttons()

def update(dt):
    update_player_pos()
    update_enemies(dt)
    update_score(dt)

def draw(fps):
    set_default_font()
    draw_enemies()
    draw_score()
    draw_menus()
    draw_fps_counter(fps)
    draw_player()

def mouse_pressed(x, y, button_pressed, isTouched, presses):
    print(x, y)
    radius = player.radius / 2
    if not game.state == Game.State.RUNNING:
        if button_pressed == 1:
            if game.state == Game.State.MENU:
                for _, button in buttons[MENU_STATE].items():
                    if button.check_pressed(x, y, radius):
                        break
            elif game.state == Game.State.ENDED:
                for _, button in buttons[ENDED_STATE].items():
                    if button.check_pressed(x, y, radius):
                        break
            elif game.state == Game.State.PAUSED:
                dx, dy = x - player.paused_x, y - player.paused_y
                d = sqrt(dx ** 2 + dy ** 2)
                if d <= radius:
                    change_game_state(Game.State.RUNNING)

def focus(f):
    if not f and game.state == Game.State.RUNNING:
        change_game_state(Game.State.PAUSED)

#========================================
# Python and Pygame specific code to run the game
#========================================
should_quit = False
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global should_quit
            should_quit = True
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            mouse_pressed(x, y, 1, False, 1)

        if event.type == pygame.WINDOWFOCUSLOST:
            focus(False)

        if event.type == pygame.WINDOWMOVED:
            focus(False)

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                focus(False)

FPS = 60
def main():
    run = True
    clock = pygame.time.Clock()

    load()

    while run:
        dt = clock.tick(FPS) / 1000

        handle_events()
        if should_quit:
            run = False
            break

        WIN.fill(BLACK)
        draw(floor(clock.get_fps() + 0.5))
        pygame.display.update()

        update(dt)

    pygame.quit()
        

if __name__ == '__main__':
    main()