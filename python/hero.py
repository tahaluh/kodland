import pygame
from settings import TILE_SIZE, HERO_COLOR, COLS, ROWS
from pgzero.actor import Actor
from labyrinth import Labyrinth

# Mazes are now unlimited

class Hero:
    def __init__(self, start_grid=(1,1), keyboard=None, current_maze=1, start_time=None):
        self.keyboard = keyboard
        self.prefix = f'alien_{HERO_COLOR}'
        self.walk_frames = [f'{self.prefix}_walk1', f'{self.prefix}_walk2']
        self.idle_frames = [f'{self.prefix}_stand', f'{self.prefix}',]
        
        # Track maze progress
        self.current_maze = current_maze
        self.start_time = start_time or pygame.time.get_ticks()
        
        # Initialize labyrinth
        self.labyrinth = Labyrinth(COLS, ROWS)
        
        # Set start position to entrance
        start_grid = self.labyrinth.get_entrance()
        x = start_grid[0] * TILE_SIZE + TILE_SIZE // 2
        y = start_grid[1] * TILE_SIZE + TILE_SIZE // 2
        
        self.actor = Actor(self.idle_frames[0], (x, y))
        self.actor.grid_pos = list(start_grid)
        self.actor.target_pos = list(start_grid)
        self.actor.speed = 4
        self.walk_frame = 0
        self.idle_frame = 0
        self.anim_timer = 0
        
        # Discover initial area
        self.labyrinth.discover_around_player(start_grid[0], start_grid[1])

    def has_reached_exit(self):
        exit_pos = self.labyrinth.get_exit()
        return (self.actor.grid_pos[0] == exit_pos[0] and 
                self.actor.grid_pos[1] == exit_pos[1])

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
                
                # Discover area around new position
                self.labyrinth.discover_around_player(
                    self.actor.grid_pos[0], 
                    self.actor.grid_pos[1]
                )
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
            
            # Handle movement input
            if self.keyboard:
                new_target = list(self.actor.target_pos)
                
                # Determine movement direction
                if self.keyboard.left and self.actor.target_pos[0] > 0:
                    new_target[0] -= 1
                elif self.keyboard.right and self.actor.target_pos[0] < COLS - 1:
                    new_target[0] += 1
                elif self.keyboard.up and self.actor.target_pos[1] > 0:
                    new_target[1] -= 1
                elif self.keyboard.down and self.actor.target_pos[1] < ROWS - 1:
                    new_target[1] += 1
                
                # Check if the new position is not a wall
                if not self.labyrinth.is_wall(new_target[0], new_target[1]):
                    self.actor.target_pos = new_target
                    self.actor.image = self.idle_frames[self.idle_frame]
                    self.anim_timer = 0


    def draw(self):
        self.actor.draw()