import settings
import random
from pgzero.rect import Rect

class PowerupManager:
    def __init__(self):
        self.move_cooldown = 15
        self.last_move_tick = -999

    POWERUP_OPTIONS = [
        {"name": "Speed Boost", "description": "+50% speed for 10s", "effect": "speed", "duration": 600},
        {"name": "Time Rewind", "description": "+10 seconds", "effect": "time", "duration": 600},
        {"name": "Vision Boost", "description": "+1 tile vision radius", "effect": "vision", "duration": 600}
    ]

    def apply_powerup(self, hero, powerup):
        if powerup['effect'] == 'speed':
            hero.actor.speed *= 1.5
            hero.speed_boost_start_time = settings.tick
        elif powerup['effect'] == 'time':
            hero.labyrinth.time_limit += 10 * 60
        elif powerup['effect'] == 'vision':
            hero.vision_radius += 1
            hero.vision_boost_start_time = settings.tick

    @classmethod
    def update_powerup_effects(self, hero):
        if hasattr(hero, 'speed_boost_start_time'):
            if settings.tick - hero.speed_boost_start_time > 600:
                hero.actor.speed = hero.base_speed
                delattr(hero, 'speed_boost_start_time')

        if hasattr(hero, 'vision_boost_start_time'):
            if settings.tick - hero.vision_boost_start_time > 600:
                hero.vision_radius -= 1
                delattr(hero, 'vision_boost_start_time')

    def get_random_powerup(self):
        return random.choice(self.POWERUP_OPTIONS)

    @classmethod
    def draw_powerup_menu(self, screen, selected_powerup, hero):
        from settings import WIDTH, HEIGHT

        hero.labyrinth.extra_time += 1 
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), color=(0, 0, 0, 128))

        screen.draw.text('Choose Your Power-Up', center=(WIDTH//2, HEIGHT//4), color='white', fontsize=36)

        option_height = 100
        option_width = 250
        option_spacing = 50

        for i, powerup in enumerate(self.POWERUP_OPTIONS):
            x = WIDTH//2 - option_width//2
            y = HEIGHT//2 + i * (option_height + option_spacing)
            screen.draw.filled_rect(Rect(x, y, option_width, option_height), color=(50, 50, 50))
            screen.draw.rect(Rect(x, y, option_width, option_height), color=(100, 100, 100))
            screen.draw.text(powerup['name'], center=(x + option_width//2, y + 30), color='white', fontsize=24)
            screen.draw.text(powerup['description'], center=(x + option_width//2, y + 60), color=(200, 200, 200), fontsize=20)

        screen.draw.text('Use arrow keys to select, SPACE to confirm', center=(WIDTH//2, HEIGHT - 50), color=(180, 180, 180), fontsize=20)

        selected_x = WIDTH//2 - option_width//2
        selected_y = HEIGHT//2 + selected_powerup * (option_height + option_spacing)
        for i in range(4):
            screen.draw.rect(Rect(selected_x + i, selected_y + i, option_width - 2*i, option_height - 2*i), color=(255, 255, 0))

    def handle_selection_input(self, keyboard, selected_index):
        if settings.tick - self.last_move_tick < self.move_cooldown:
            return selected_index

        if keyboard.down:
            selected_index = (selected_index + 1) % len(self.POWERUP_OPTIONS)
            self.last_move_tick = settings.tick
        elif keyboard.up:
            selected_index = (selected_index - 1) % len(self.POWERUP_OPTIONS)
            self.last_move_tick = settings.tick

        return selected_index

