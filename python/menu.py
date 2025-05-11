# menu.py
from settings import WIDTH, HEIGHT
from pygame import Rect

class MenuManager:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager

        btn_w, btn_h = 200, 40
        spacing = 20
        
        labels = ["start", "sound", "exit"]
        total_h = len(labels) * btn_h + (len(labels)-1) * spacing

        start_y = HEIGHT//2 - total_h//2

        self.buttons = {}
        for i, label in enumerate(labels):
            x = WIDTH//2 - btn_w//2
            y = start_y + i * (btn_h + spacing)
            self.buttons[label] = Rect(x, y, btn_w, btn_h)

        labels2 = ["toggle_music", "toggle_sound", "back"]
        total_h2 = len(labels2) * btn_h + (len(labels2)-1) * spacing
        start_y2 = HEIGHT//2 - total_h2//2
        self.sound_buttons = {}
        for i, label in enumerate(labels2):
            x = WIDTH//2 - btn_w//2
            y = start_y2 + i * (btn_h + spacing)
            self.sound_buttons[label] = Rect(x, y, btn_w, btn_h)

    def draw_menu(self, screen):
        screen.fill((30, 30, 30))
        screen.draw.text("Labirintus", center=(screen.width // 2, 80), fontsize=40, color="white")
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
