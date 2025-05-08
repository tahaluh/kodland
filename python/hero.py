from settings import TILE_SIZE, HERO_COLOR
from pgzero.actor import Actor

HERO_COLOR = 'blue'
HERO_PREFIX = f'alien_{HERO_COLOR}'

WALK_FRAMES = [f'{HERO_PREFIX}_walk1', f'{HERO_PREFIX}_walk2']
IDLE_FRAMES = [f'{HERO_PREFIX}', f'{HERO_PREFIX}_stand']

hero = Actor(IDLE_FRAMES[0], (TILE_SIZE // 2, TILE_SIZE // 2))
hero.grid_pos = [1, 1]
hero.target_pos = [1, 1]
hero.speed = 4
hero.walk_frame = 0
hero.idle_frame = 0
hero.anim_timer = 0

def update_hero(keyboard):
    moving = hero.grid_pos != hero.target_pos

    if moving:
        target_px = [hero.target_pos[0] * TILE_SIZE + TILE_SIZE // 2,
                     hero.target_pos[1] * TILE_SIZE + TILE_SIZE // 2]
        dx = target_px[0] - hero.x
        dy = target_px[1] - hero.y

        if abs(dx) > hero.speed:
            hero.x += hero.speed if dx > 0 else -hero.speed
        else:
            hero.x = target_px[0]
        if abs(dy) > hero.speed:
            hero.y += hero.speed if dy > 0 else -hero.speed
        else:
            hero.y = target_px[1]

        # Caminhando
        hero.anim_timer += 1
        if hero.anim_timer >= 10:
            hero.walk_frame = (hero.walk_frame + 1) % len(WALK_FRAMES)
            hero.image = WALK_FRAMES[hero.walk_frame]
            hero.anim_timer = 0
    else:
        hero.anim_timer += 1
        if hero.anim_timer >= 30:
            hero.idle_frame = (hero.idle_frame + 1) % len(IDLE_FRAMES)
            hero.image = IDLE_FRAMES[hero.idle_frame]
            hero.anim_timer = 0

        if keyboard.right:
            hero.target_pos[0] += 1
        elif keyboard.left:
            hero.target_pos[0] -= 1
        elif keyboard.down:
            hero.target_pos[1] += 1
        elif keyboard.up:
            hero.target_pos[1] -= 1

