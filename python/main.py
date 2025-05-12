import pgzrun
from pgzero.rect import Rect
import settings
from settings import WIDTH, HEIGHT, TILE_SIZE, COLS, ROWS
from menu import MenuManager
from sounds import SoundManager
from hero import Hero
from stars import StarField 
from labyrinth import Labyrinth
from powerup import PowerupManager



game_state    = 'menu'
game_over_button = None  # Will be set in draw_game_over()
sound_manager = SoundManager(music, sounds)
sound_manager.start_music()
menu          = MenuManager(sound_manager)
labyrinth     = Labyrinth(COLS, ROWS)
powerup_manager = PowerupManager()
hero          = Hero(start_grid=(1, 1), keyboard=keyboard, labyrinth=labyrinth, powerup_manager=powerup_manager)
starfield     = StarField(count=200, big_chance=0.05, big_radius=2) 

def draw():
    screen.clear()
    if game_state == 'menu':
        menu.draw_menu(screen)
    elif game_state == 'sound_menu':
        menu.draw_sound_menu(screen)
    elif game_state == 'game':
        draw_game()
    elif game_state == 'game_over':
        draw_game_over()

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
    
    hero.draw(screen)
    
    # Maze counter and timer
    reaming_time = labyrinth.time_limit // 60
    
    # Draw maze number
    screen.draw.text(
        f'Maze: {hero.current_maze}', 
        topleft=(10, 10), 
        color='white', 
        fontsize=24
    )
    
    # Draw timer
    screen.draw.text(
        f'Time: {reaming_time}s', 
        topright=(WIDTH-10, 10), 
        color='white', 
        fontsize=24
    )

def update():
    global game_state, hero
    if game_state == 'game':
        hero.update()
        starfield.update()
        labyrinth.update()
        
        # Check for game over conditions
        reaming_time = labyrinth.time_limit // 60
        
        if reaming_time <= 0:
            game_state = 'game_over'
        
        # Handle powerup menu input
        if hero.show_powerup_menu:
            hero.handle_powerup_menu_input()
        
        # Update powerup effects
        PowerupManager.update_powerup_effects(hero=hero)
         
        if hero.has_reached_exit():
            labyrinth.reset()
            hero.pass_maze()
            
        if labyrinth.time_limit <= 0:
            game_state = 'game_over'
    settings.tick += 1

def draw_game_over():
    screen.fill((0, 0, 0))
    
    # Game Over text
    screen.draw.text(
        'GAME OVER', 
        center=(WIDTH//2, HEIGHT//3), 
        color='red', 
        fontsize=72
    )
    
    # Maze reached
    screen.draw.text(
        f'Maze Reached: {hero.current_maze}', 
        center=(WIDTH//2, HEIGHT//2), 
        color='white', 
        fontsize=36
    )
    
    # Back to Menu button
    button_width, button_height = 200, 50
    button_x = WIDTH//2 - button_width//2
    button_y = HEIGHT * 2//3
    
    screen.draw.filled_rect(
        Rect(button_x, button_y, button_width, button_height), 
        color=(100, 100, 100)
    )
    screen.draw.rect(
        Rect(button_x, button_y, button_width, button_height), 
        color=(200, 200, 200)
    )
    screen.draw.text(
        'Back to Menu', 
        center=(WIDTH//2, button_y + button_height//2), 
        color='white', 
        fontsize=24
    )
    
    # Store button rect for click detection
    global game_over_button
    game_over_button = Rect(button_x, button_y, button_width, button_height)

def on_mouse_down(pos):
    global game_state, hero
    if game_state == 'menu':
        game_state = menu.handle_menu_click(pos, game_state)
    elif game_state == 'sound_menu':
        game_state = menu.handle_sound_menu_click(pos, game_state)
    elif game_state == 'game_over':
        if game_over_button.collidepoint(pos):
            game_state = 'menu'
            labyrinth = Labyrinth(COLS, ROWS)
            hero = Hero(start_grid=(1, 1), keyboard=keyboard, labyrinth=labyrinth, powerup_manager=powerup_manager)
pgzrun.go()
