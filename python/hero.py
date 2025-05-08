from settings import TILE_SIZE, HERO_COLOR, COLS, ROWS
from pgzero.actor import Actor

class Hero:
    def __init__(self, start_grid=(1,1), keyboard=None):
        self.keyboard = keyboard
        self.prefix = f'alien_{HERO_COLOR}'
        self.walk_frames = [f'{self.prefix}_walk1', f'{self.prefix}_walk2']
        self.idle_frames = [f'{self.prefix}_stand', f'{self.prefix}',]
        x = start_grid[0] * TILE_SIZE + TILE_SIZE // 2
        y = start_grid[1] * TILE_SIZE + TILE_SIZE // 2
        self.actor = Actor(self.idle_frames[0], (x, y))
        self.actor.grid_pos = list(start_grid)
        self.actor.target_pos = list(start_grid)
        self.actor.speed = 4
        self.walk_frame = 0
        self.idle_frame = 0
        self.anim_timer = 0

    def update(self):
        moving = self.actor.grid_pos != self.actor.target_pos
        tx = self.actor.target_pos[0] * TILE_SIZE + TILE_SIZE // 2
        ty = self.actor.target_pos[1] * TILE_SIZE + TILE_SIZE // 2

        if moving:
            dx = tx - self.actor.x
            if abs(dx) > self.actor.speed:
                self.actor.x += self.actor.speed if dx > 0 else -self.actor.speed
            else:
                self.actor.x = tx
            dy = ty - self.actor.y
            if abs(dy) > self.actor.speed:
                self.actor.y += self.actor.speed if dy > 0 else -self.actor.speed
            else:
                self.actor.y = ty

            if self.actor.x == tx and self.actor.y == ty:
                self.actor.grid_pos = list(self.actor.target_pos)
                self.anim_timer = 0
                self.idle_frame = 0
                self.actor.image = self.idle_frames[self.idle_frame]
            else:
                self.anim_timer += 1
                if self.anim_timer >= 10:
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_frames)
                    self.actor.image = self.walk_frames[self.walk_frame]
                    self.anim_timer = 0
        else:
            self.anim_timer += 1
            if self.anim_timer >= 30:
                self.idle_frame = (self.idle_frame + 1) % len(self.idle_frames)
                self.actor.image = self.idle_frames[self.idle_frame]
                self.anim_timer = 0
            if self.keyboard.right:
                newPos = self.actor.grid_pos[0] + 1
                if newPos < COLS:
                    self.actor.target_pos[0] = newPos
            elif self.keyboard.left:
                newPos = self.actor.grid_pos[0] - 1
                if newPos >= 0:
                    self.actor.target_pos[0] = newPos                
            elif self.keyboard.down:
                newPos = self.actor.grid_pos[1] + 1
                if newPos < ROWS:
                    self.actor.target_pos[1] = newPos
            elif self.keyboard.up:
                newPos = self.actor.grid_pos[1] - 1
                if newPos >= 0:
                    self.actor.target_pos[1] = newPos

    def draw(self):
        self.actor.draw()