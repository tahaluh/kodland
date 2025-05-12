import settings

class Projectile:
    def __init__(self, start_pos, direction):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.direction = direction
        self.speed = 2
        self.active = True
        self.size = 5
    
    def update(self, labyrinth):
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed

        grid_x = int(new_x // settings.TILE_SIZE)
        grid_y = int(new_y // settings.TILE_SIZE)

        if labyrinth.is_wall(grid_x, grid_y):
            self.active = False
            return
        
        self.x = new_x
        self.y = new_y
    
    def draw(self, screen):
        if self.active:
            screen.draw.filled_circle((self.x, self.y), self.size, (255, 255, 255))
    
    def check_ghost_collision(self, ghosts):
        if not self.active:
            return []
        
        ghosts_to_remove = []
        for ghost in ghosts:
            if (int(self.x // settings.TILE_SIZE) == ghost.actor.grid_pos[0] and 
                int(self.y // settings.TILE_SIZE) == ghost.actor.grid_pos[1]):
                ghosts_to_remove.append(ghost)
                self.active = False
                break
        
        return ghosts_to_remove
