# sounds.py

class SoundManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, music=None, sounds=None):
        if self._initialized:
            return  
        self.music = music
        self.sounds = sounds
        self.sound_on = True
        self.music_on = True
        self._initialized = True

    def toggle_sound(self):
        self.sound_on = not self.sound_on

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on and self.music:
            self.music.set_volume(0.5)
            self.music.play('theme')
        elif self.music:
            self.music.set_volume(0)

    def play_sound(self, effect):
        if self.sound_on:
            effect.play()
            
    def play_click(self):
        self.play_sound(self.sounds.click_001)

    def start_music(self):
        if self.music_on and self.music:
            try:
                self.music.play('theme')
                self.music.set_volume(0.5)
            except:
                print("Error playing music")
