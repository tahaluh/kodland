import settings
from settings import TILE_SIZE, HERO_COLOR, COLS, ROWS
from pgzero.actor import Actor

class Hero:
    def __init__(self, start_grid=(1, 1), keyboard=None, current_maze=1, labyrinth=None, powerup_manager=None):
        self.powerup_manager = powerup_manager
        self.keyboard = keyboard
        self.prefix = f'alien_{HERO_COLOR}'
        self.flipped = 0

        self.current_maze = current_maze

        self.labyrinth = labyrinth
        start_grid = self.labyrinth.get_entrance()

        x = start_grid[0] * TILE_SIZE + TILE_SIZE // 2
        y = start_grid[1] * TILE_SIZE + TILE_SIZE // 2

        walk_frames, idle_frames = self.get_current_frames()
        self.actor = Actor(idle_frames[0], (x, y))
        self.actor.grid_pos = list(start_grid)
        self.actor.target_pos = list(start_grid)
        self.base_speed = 2
        self.speed_boosts_collected = 0  
        self.actor.speed = self.base_speed
        
        self.vision_radius = 1

        self.walk_frame = 0
        self.idle_frame = 0
        self.anim_timer = 0
        
        self.show_powerup_menu = False
        self.selected_powerup = None

        self.is_invulnerable = False
        self.invulnerability_duration = 180  
        self.invulnerability_timer = 0

        self.last_move_direction = (1, 0)

        self.projectile_speed = 5
        self.projectile_cooldown = 10
        self.projectile_timer = 0
        self.projectiles = []
        self.space_pressed = False
        self.space_released = True

        self.labyrinth.discover_around_player(start_grid[0], start_grid[1], radius=self.vision_radius)

    def has_reached_exit(self):
        exit_pos = self.labyrinth.get_exit()
        return (
            self.actor.grid_pos[0] == exit_pos[0]
            and self.actor.grid_pos[1] == exit_pos[1]
        )

    def get_current_frames(self):
        suffix = '_flipped' if self.flipped else ''
        walk_frames = [f'{self.prefix}_walk1{suffix}', f'{self.prefix}_walk2{suffix}']
        idle_frames = [f'{self.prefix}_stand{suffix}', f'{self.prefix}{suffix}']
        return walk_frames, idle_frames

    def update(self):
        moving = self.actor.grid_pos != self.actor.target_pos
        tx = self.actor.target_pos[0] * TILE_SIZE + TILE_SIZE // 2
        ty = self.actor.target_pos[1] * TILE_SIZE + TILE_SIZE // 2

        walk_frames, idle_frames = self.get_current_frames()

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

            if dx != 0 or dy != 0:
                self.last_move_direction = (dx, dy)

            if self.actor.x == tx and self.actor.y == ty:
                self.actor.grid_pos = list(self.actor.target_pos)
                self.anim_timer = 0
                self.idle_frame = 0
                self.actor.image = idle_frames[self.idle_frame]
                
                x, y = self.actor.grid_pos
                if self.labyrinth.is_speed_boost_square(x, y):
                    self.selected_powerup = 0  
                    self.show_powerup_menu = True
                    self.labyrinth.remove_speed_boost_square(x, y)
                
                self.labyrinth.discover_around_player(
                    self.actor.grid_pos[0], self.actor.grid_pos[1], radius=self.vision_radius
                )
            else:
                self.anim_timer += 1
                if self.anim_timer >= 10:
                    self.walk_frame = (self.walk_frame + 1) % len(walk_frames)
                    self.actor.image = walk_frames[self.walk_frame]
                    self.anim_timer = 0
        else:
            self.anim_timer += 1
            if self.anim_timer >= 30:
                self.idle_frame = (self.idle_frame + 1) % len(idle_frames)
                self.actor.image = idle_frames[self.idle_frame]
                self.anim_timer = 0

            if self.keyboard:
                new_target = list(self.actor.target_pos)

                if self.keyboard.left and self.actor.target_pos[0] > 0:
                    new_target[0] -= 1
                    self.flipped = 1
                elif self.keyboard.right and self.actor.target_pos[0] < COLS - 1:
                    new_target[0] += 1
                    self.flipped = 0
                elif self.keyboard.up and self.actor.target_pos[1] > 0:
                    new_target[1] -= 1
                elif self.keyboard.down and self.actor.target_pos[1] < ROWS - 1:
                    new_target[1] += 1

                if not self.labyrinth.is_wall(new_target[0], new_target[1]):
                    self.actor.target_pos = new_target
                    self.anim_timer = 0
                    self.idle_frame = 0
                    _, idle_frames = self.get_current_frames()
                    self.actor.image = idle_frames[self.idle_frame]

    def draw(self, screen):
        if self.is_invulnerable:
            if (self.invulnerability_timer // 10) % 2 == 0:
                self.actor.draw()
        else:
            self.actor.draw()
        
        if self.show_powerup_menu:
            self.powerup_manager.draw_powerup_menu(screen, self.selected_powerup, self)
        
    def handle_powerup_menu_input(self):
        if not self.show_powerup_menu or not self.keyboard:
            return
       
        self.selected_powerup = self.powerup_manager.handle_selection_input(self.keyboard, self.selected_powerup)
        if self.keyboard.space:
            selected_powerup = self.powerup_manager.POWERUP_OPTIONS[self.selected_powerup]
            self.powerup_manager.apply_powerup(self, selected_powerup)
            self.show_powerup_menu = False
        if self.keyboard.space and self.projectile_timer >= self.projectile_cooldown and self.space_released:
            # Create a new projectile in the last movement direction
            start_pos = (
                self.actor.grid_pos[0] * settings.TILE_SIZE + settings.TILE_SIZE // 2, 
                self.actor.grid_pos[1] * settings.TILE_SIZE + settings.TILE_SIZE // 2
            )
            self.projectiles.append(Projectile(start_pos, self.last_move_direction))
            self.projectile_timer = 0
            self.space_pressed = True
            self.space_released = False
        
        if not self.keyboard.space:
            self.space_pressed = False
            self.space_released = True
        
    def pass_maze(self):
        self.current_maze += 1
        
        start_grid = self.labyrinth.get_entrance()
        
        x = start_grid[0] * TILE_SIZE + TILE_SIZE // 2
        y = start_grid[1] * TILE_SIZE + TILE_SIZE // 2
        
        self.actor.x = x
        self.actor.y = y
        self.actor.grid_pos = list(start_grid)
        self.actor.target_pos = list(start_grid)
        self.labyrinth.discover_around_player(start_grid[0], start_grid[1], radius=self.vision_radius)
        
        self.actor.speed = self.base_speed
