# menu.py
from pygame import Rect

class MenuManager:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager

        self.buttons = {
            "start": Rect(220, 150, 200, 40),
            "sound": Rect(220, 210, 200, 40),
            "exit": Rect(220, 270, 200, 40),
        }

        self.sound_buttons = {
            "toggle_music": Rect(200, 150, 240, 40),
            "toggle_sound": Rect(200, 210, 240, 40),
            "back": Rect(200, 270, 240, 40),
        }

    def draw_menu(self, screen):
        screen.fill((30, 30, 30))
        screen.draw.text("ROGUELIKE GAME", center=(screen.width // 2, 80), fontsize=40, color="white")
        for label, rect in self.buttons.items():
            screen.draw.filled_rect(rect, (50, 50, 150))
            screen.draw.text(label.upper(), center=rect.center, fontsize=30, color="white")

    def draw_sound_menu(self, screen):
        screen.fill((20, 20, 60))
        screen.draw.text("SOUND SETTINGS", center=(screen.width // 2, 80), fontsize=36, color="white")
        screen.draw.text(f"Music: {'ON' if self.sound_manager.music_on else 'OFF'}", center=self.sound_buttons["toggle_music"].center, fontsize=28, color="white")
        screen.draw.text(f"Sound: {'ON' if self.sound_manager.sound_on else 'OFF'}", center=self.sound_buttons["toggle_sound"].center, fontsize=28, color="white")
        screen.draw.text("BACK", center=self.sound_buttons["back"].center, fontsize=28, color="white")
        for rect in self.sound_buttons.values():
            screen.draw.rect(rect, (100, 100, 180))

    def handle_menu_click(self, pos, game_state):
        if self.buttons["start"].collidepoint(pos):
            self.sound_manager.play_click()
            return 'game'
        elif self.buttons["sound"].collidepoint(pos):
            self.sound_manager.play_click()
            return 'sound_menu'
        elif self.buttons["exit"].collidepoint(pos):
            exit()
        return game_state

    def handle_sound_menu_click(self, pos, game_state):
        if self.sound_buttons["toggle_music"].collidepoint(pos):
            self.sound_manager.toggle_music()
            self.sound_manager.play_click()
        elif self.sound_buttons["toggle_sound"].collidepoint(pos):
            self.sound_manager.toggle_sound()
            self.sound_manager.play_click()
        elif self.sound_buttons["back"].collidepoint(pos):
            self.sound_manager.play_click()
            return 'menu'
        return game_state
