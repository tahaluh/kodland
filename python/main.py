import pgzrun
import random
from pygame import Rect
from hero import hero, update_hero
from menu import MenuManager
from sounds import SoundManager


WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32

game_state = 'menu'

sound_manager = SoundManager(music, sounds) 
menu = MenuManager(sound_manager)

def draw():
    screen.clear()
    if game_state == 'menu':
        menu.draw_menu(screen)
    elif game_state == 'sound_menu':
        menu.draw_sound_menu(screen)
    elif game_state == 'game':
        draw_game()


def draw_game():
    screen.fill((0, 0, 0))
    hero.draw()

def update():
    if game_state == 'game':
        update_hero(keyboard)

def on_mouse_down(pos):
    global game_state
    if game_state == 'menu':
        game_state = menu.handle_menu_click(pos, game_state)
    elif game_state == 'sound_menu':
        game_state = menu.handle_sound_menu_click(pos, game_state)




sound_manager.start_music()

pgzrun.go()
