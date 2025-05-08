import random
from pygame import Rect
from settings import WIDTH, HEIGHT

class StarField:
    def __init__(self, count=200, big_chance=0.05, big_radius=2):
        self.count        = count
        self.big_chance   = big_chance
        self.big_radius   = big_radius
        self.colors       = [
            (150,150,150),
            (200,200,200),
            (240,240,240),
            (255,255,255),
        ]
        self.stars = []
        self._generate()

    def _generate(self):
        self.stars.clear()
        for _ in range(self.count):
            self.stars.append({
                "x":     random.randint(0, WIDTH-1),
                "y":     random.randint(0, HEIGHT-1),
                "phase": random.randrange(len(self.colors)),
                "size":  self.big_radius if random.random() < self.big_chance else 0
            })

    def update(self):
        for s in self.stars:
            if random.random() < 0.05:
                s["phase"] = (s["phase"] + 1) % len(self.colors)

    def draw(self, screen):
        for s in self.stars:
            color = self.colors[s["phase"]]
            if s["size"] > 0:
                screen.draw.filled_circle((s["x"], s["y"]), s["size"], color)
            else:
                screen.draw.filled_rect(Rect(s["x"], s["y"], 1, 1), color)
