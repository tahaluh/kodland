import random

class Labyrinth:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.discovered_grid = [[False for _ in range(width)] for _ in range(height)]
        self.speed_boost_squares = set()
        self.generate_maze()
        self.set_entrance_and_exit()
        self.add_speed_boost_squares()

    def generate_maze(self):
        def carve_path(x, y):
            self.grid[y][x] = 0
            
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.grid[ny][nx] == 1):
                    self.grid[y + dy][x + dx] = 0
                    carve_path(nx, ny)
        
        start_x, start_y = random.randrange(1, self.width-1, 2), random.randrange(1, self.height-1, 2)
        carve_path(start_x, start_y)

    def set_entrance_and_exit(self):
        mid_x, mid_y = self.width // 2, self.height // 2
        self.grid[mid_y][mid_x] = 2
        
        border_sides = ['top', 'bottom', 'left', 'right']
        exit_side = random.choice(border_sides)
        
        if exit_side == 'top':
            x = random.randrange(1, self.width-1, 2)
            self.grid[0][x] = 3
        elif exit_side == 'bottom':
            x = random.randrange(1, self.width-1, 2)
            self.grid[self.height-1][x] = 3
        elif exit_side == 'left':
            y = random.randrange(1, self.height-1, 2)
            self.grid[y][0] = 3
        else:
            y = random.randrange(1, self.height-1, 2)
            self.grid[y][self.width-1] = 3

    def add_speed_boost_squares(self, num_squares=10):
        attempts = 0
        while len(self.speed_boost_squares) < num_squares and attempts < 100:
            x = random.randrange(1, self.width-1)
            y = random.randrange(1, self.height-1)
            
            if (self.grid[y][x] == 0 and 
                (x, y) not in self.speed_boost_squares):
                self.grid[y][x] = 4
                self.speed_boost_squares.add((x, y))
            
            attempts += 1

    def discover_around_player(self, player_x, player_y):
        adjacent_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for dx, dy in adjacent_offsets:
            nx, ny = player_x + dx, player_y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height):
                self.discovered_grid[ny][nx] = True

    def is_wall(self, x, y):
        return self.grid[y][x] == 1

    def is_speed_boost_square(self, x, y):
        return self.grid[y][x] == 4

    def remove_speed_boost_square(self, x, y):
        if (x, y) in self.speed_boost_squares:
            self.speed_boost_squares.remove((x, y))
            self.grid[y][x] = 0  # Change to a regular path

    def is_discovered(self, x, y):
        return self.discovered_grid[y][x]

    def get_entrance(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 2:
                    return x, y
        return None

    def get_exit(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 3:
                    return x, y
        return None
