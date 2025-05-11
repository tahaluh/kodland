import pgzrun
import pygame
from pgzero.rect import Rect
from settings import WIDTH, HEIGHT, TILE_SIZE, ROWS, COLS
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
    for y in range(ROWS):
        for x in range(COLS):
            tile_x = x * TILE_SIZE
            tile_y = y * TILE_SIZE
            
            # Wall tiles
            if hero.labyrinth.is_discovered(x, y):
                if hero.labyrinth.is_wall(x, y):
                    screen.draw.filled_rect(
                        Rect((tile_x, tile_y), (TILE_SIZE, TILE_SIZE)), 
                        color=(30, 30, 30)
                    )
                
                # Exit tile
                elif hero.labyrinth.grid[y][x] == 3:
                    screen.draw.filled_rect(
                        Rect((tile_x, tile_y), (TILE_SIZE, TILE_SIZE)), 
                        color=(255, 0, 0)  # Red
                    )
            
            # Fog for undiscovered tiles
            if not hero.labyrinth.is_discovered(x, y):
                screen.draw.filled_rect(
                    Rect((tile_x, tile_y), (TILE_SIZE, TILE_SIZE)), 
                    color=(20, 20, 20)  # Dark fog
                )
    
    # Grid lines
    grid_color = (50, 50, 50)
    for x in range(0, WIDTH+1, TILE_SIZE):
        screen.draw.line((x, 0), (x, HEIGHT), grid_color)
    for y in range(0, HEIGHT+1, TILE_SIZE):
        screen.draw.line((0, y), (WIDTH, y), grid_color)
    
    hero.draw()
    
    # Maze counter and timer
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - hero.start_time) // 1000  # Convert to seconds
    
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
        
        # Check if player has reached exit
        if hero.has_reached_exit():
            # Move to next maze
            hero = Hero(
                start_grid=(1, 1), 
                keyboard=keyboard, 
                current_maze=hero.current_maze + 1
            )


def on_mouse_down(pos):
    global game_state, hero
    if game_state == 'menu':
        game_state = menu.handle_menu_click(pos, game_state)
    elif game_state == 'sound_menu':
        game_state = menu.handle_sound_menu_click(pos, game_state)

pgzrun.go()
