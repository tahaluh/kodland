import pgzrun
from pgzero.rect import Rect
import settings
from settings import WIDTH, HEIGHT, TILE_SIZE
from menu import MenuManager
from sounds import SoundManager
from hero import Hero
from stars import StarField 

game_state    = 'menu'
sound_manager = SoundManager(music, sounds)
sound_manager.start_music()
menu          = MenuManager(sound_manager)
hero          = Hero(start_grid=(1, 1), keyboard=keyboard)
starfield     = StarField(count=200, big_chance=0.05, big_radius=2) 

def draw():
    screen.clear()
    if game_state == 'menu':
        menu.draw_menu(screen)
    elif game_state == 'sound_menu':
        menu.draw_sound_menu(screen)
    else:
        draw_game()

def draw_game():
    screen.fill((0, 0, 0))
    
    # stars
    starfield.draw(screen) 

    # Labyrinth
    hero.labyrinth.draw_labyrinth(screen)
    
    # Grid lines
    grid_color = (50, 50, 50)
    for x in range(0, WIDTH+1, TILE_SIZE):
        screen.draw.line((x, 0), (x, HEIGHT), grid_color)
    for y in range(0, HEIGHT+1, TILE_SIZE):
        screen.draw.line((0, y), (WIDTH, y), grid_color)
    
    hero.draw()
    
    # Maze counter and timer
    current_time = settings.tick
    elapsed_time = (current_time - hero.start_time) // 60  # Convert to seconds
    
    # Draw maze number
    screen.draw.text(
        f'Maze: {hero.current_maze}', 
        topleft=(10, 10), 
        color='white', 
        fontsize=24
    )
    
    # Draw timer
    screen.draw.text(
        f'Time: {elapsed_time}s', 
        topright=(WIDTH-10, 10), 
        color='white', 
        fontsize=24
    )

def update():
    global game_state, hero
    if game_state == 'game':
        hero.update()
        starfield.update()
         
        if hero.has_reached_exit():
            hero = Hero(
                start_grid=(1, 1), 
                keyboard=keyboard, 
                current_maze=hero.current_maze + 1
            )
    settings.tick += 1


def on_mouse_down(pos):
    global game_state, hero
    if game_state == 'menu':
        game_state = menu.handle_menu_click(pos, game_state)
    elif game_state == 'sound_menu':
        game_state = menu.handle_sound_menu_click(pos, game_state)

pgzrun.go()
