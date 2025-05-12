import random
from pgzero.actor import Actor
import settings
from settings import COLS, ROWS, TILE_SIZE

class Ghost:
    def __init__(self, labyrinth, start_grid=None):
        self.labyrinth = labyrinth
        
        if start_grid is None:
            start_grid = self._find_random_start_position()
        
        x = start_grid[0] * TILE_SIZE + TILE_SIZE // 2
        y = start_grid[1] * TILE_SIZE + TILE_SIZE // 2
        self.actor = Actor('ghost', (x, y))
        
        self.actor.grid_pos = list(start_grid)
        self.actor.target_pos = list(start_grid)
        
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.current_direction = random.choice(self.directions)
        self.speed = 2 
        
        self.move_cooldown = 15
        self.move_timer = 0
    
    def _find_random_start_position(self):
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            
            if (not self.labyrinth.is_wall(x, y) and 
                (x, y) != self.labyrinth.get_entrance() and 
                (x, y) != self.labyrinth.get_exit()):
                return (x, y)
            
            attempts += 1
        
        return self.labyrinth.get_entrance()
    
    def update(self):
        tx = self.actor.target_pos[0] * TILE_SIZE + TILE_SIZE // 2
        ty = self.actor.target_pos[1] * TILE_SIZE + TILE_SIZE // 2
        
        dx = tx - self.actor.x
        dy = ty - self.actor.y

        if abs(dx) > self.speed or abs(dy) > self.speed:
            if abs(dx) > self.speed:
                self.actor.x += self.speed if dx > 0 else -self.speed
            else:
                self.actor.x = tx

            if abs(dy) > self.speed:
                self.actor.y += self.speed if dy > 0 else -self.speed
            else:
                self.actor.y = ty

            return
        
        self.move_timer += 1
        
        if self.move_timer < self.move_cooldown:
            return
        
        self.move_timer = 0
        
        new_x = self.actor.grid_pos[0] + self.current_direction[0]
        new_y = self.actor.grid_pos[1] + self.current_direction[1]
        
        if self.labyrinth.is_wall(new_x, new_y):
            self.current_direction = random.choice(self.directions)
            return
        
        self.actor.grid_pos[0] = new_x
        self.actor.grid_pos[1] = new_y
        self.actor.target_pos[0] = new_x
        self.actor.target_pos[1] = new_y
    
    def draw(self, screen):
        if self.labyrinth.is_discovered(self.actor.grid_pos[0], self.actor.grid_pos[1]):
            self.actor.draw()
    
    def check_collision(self, hero):
        if not hero.is_invulnerable:
            if (self.actor.grid_pos[0] == hero.actor.grid_pos[0] and 
                self.actor.grid_pos[1] == hero.actor.grid_pos[1]):
                return True
        return False
