# TODO:
# Fix player movement and collision detection
# Fix player animation

# WORK IN PROGRESS:
# Collision detection is broken, isOnGround is always false

# FIXME:
# Broken player animation
# Collision problem #1: Touching bottom part of the tile causes player to slowly pass throught up the tile.
# Collision problem #2: if you touching the bottom part and also going to left/right direction causes player to immedeatly teleport to the opposide side of the tile and also going up one tile up if its possible.
# Jump works wierdly. Is should just add +10 to gravitaton, but not just going up for duration of time.

import pygame
from time import time
from data import *
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 30)
pygame.display.set_caption("Krust Krusador")

TILE_TEXTURES = {
    0: pygame.image.load("assets/empty.png").convert_alpha(),
    -1: pygame.image.load("assets/errorTile.png").convert_alpha(),
    1: pygame.image.load("assets/tileUp.png").convert(),
    2: pygame.image.load("assets/tileBottom.png").convert(),
    3: pygame.image.load("assets/flagUp.png").convert_alpha(),
    4: pygame.image.load("assets/flagDown.png").convert_alpha(),
    "default": pygame.image.load("assets/errorTile.png").convert()
}

def resizePlayerTextures():
    global playerIdleTexture, playerRunTexture
    playerIdleTexture = pygame.image.load("assets/playerIdle.png").convert_alpha()
    playerRunTexture = pygame.image.load("assets/playerRun.png").convert_alpha()
    playerIdleTexture = pygame.transform.scale(playerIdleTexture, (player["size"] * cameraZoom, player["size"] * cameraZoom))
    playerRunTexture = pygame.transform.scale(playerRunTexture, (player["size"] * cameraZoom, player["size"] * cameraZoom))
resizePlayerTextures()

def selectTile(tileType):
    return TILE_TEXTURES.get(tileType, TILE_TEXTURES["default"])

def draw_map():
    tile_map = level["map"]
    rows = len(tile_map)
    cols = len(tile_map[0]) if rows > 0 else 0

    scaled_size = int(TILE_SIZE * cameraZoom)

    offset_x = -cameraX * cameraZoom + cameraXOffset
    offset_y = -cameraY * cameraZoom + cameraYOffset

    screen_width, screen_height = screen.get_size()

    start_col = max(0, int((-offset_x) // scaled_size))
    end_col   = min(cols, int((-offset_x + screen_width) // scaled_size) + 1)
    start_row = max(0, int((-offset_y) // scaled_size))
    end_row   = min(rows,  int((-offset_y + screen_height) // scaled_size) + 1)

    scaled_tiles_cache = {}

    hitbox_surf = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)
    if debugMode:
        hitbox_surf.fill((0, 0, 255, 80))
    else:
        hitbox_surf.fill((0, 0, 0, 0))
    
    solidHitboxes.clear()
    
    for h in range(start_row, end_row):
        for w in range(start_col, end_col):
            tile_id = tile_map[h][w]
            if tile_id == 0:
                continue

            x = w * scaled_size + offset_x
            y = h * scaled_size + offset_y

            if tile_id not in scaled_tiles_cache:
                base_tex = selectTile(tile_id)
                scaled_tiles_cache[tile_id] = pygame.transform.scale(
                    base_tex, (scaled_size, scaled_size)
                )

            screen.blit(scaled_tiles_cache[tile_id], (x, y))
            screen.blit(hitbox_surf, (x, y))
            
            rect = pygame.Rect(w * TILE_SIZE, h * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            solidHitboxes.append(rect)
                

def drawPlayer():
    playerX = (player["x"] * player["size"] - cameraX) * cameraZoom + cameraXOffset
    playerY = (player["y"] * player["size"] - cameraY) * cameraZoom + cameraYOffset

    tick = round(time())
    if player["anyKeyPressed"]:
        if (tick * player["animationSpeed"]) % 2:
            screen.blit(playerRunTexture, (playerX, playerY))
        else:
            screen.blit(playerIdleTexture, (playerX, playerY))
    else:
        screen.blit(playerIdleTexture, (playerX, playerY))

    if debugMode:
        hitbox_surf = pygame.Surface((player["size"] * cameraZoom, player["size"] * cameraZoom), pygame.SRCALPHA)
        hitbox_surf.fill((255, 0, 0, 80))
        screen.blit(hitbox_surf, (playerX, playerY))

    player["playerCollider"] = pygame.Rect(
        player["x"] * player["size"],
        player["y"] * player["size"],
        player["size"],
        player["size"]
    )

def moveCamera(delta_time):
    global cameraX, cameraY
    targetX = player["x"] * player["size"] + player["size"] / 2
    targetY = player["y"] * player["size"] + player["size"] / 2

    targetX -= (WIDTH / 2) / cameraZoom
    targetY -= (HEIGHT / 2) / cameraZoom
    
    followSpeed = cameraFollowSpeed * delta_time * cameraZoom
    cameraX += (targetX - cameraX) * followSpeed
    cameraY += (targetY - cameraY) * followSpeed

def movePlayer(dx, dy):
    playerCollider = pygame.Rect(
        player["x"] * player["size"],
        player["y"] * player["size"],
        player["size"],
        player["size"]
    )
    
    player["x"] += dx
    playerCollider.x = player["x"] * player["size"]
    for hitbox in solidHitboxes:
        if playerCollider.colliderect(hitbox):
            if dx > 0:
                player["x"] = (hitbox.left - player["size"]) / player["size"]
            elif dx < 0:
                player["x"] = (hitbox.right) / player["size"]
            playerCollider.x = player["x"] * player["size"]

    player["y"] += dy
    playerCollider.y = player["y"] * player["size"]

    max_lift = 5
    lift = 0
    while lift < max_lift:
        collision = False
        for hitbox in solidHitboxes:
            if playerCollider.colliderect(hitbox):
                collision = True
                break
        if not collision:
            break
        playerCollider.y -= 1
        lift += 1
    player["y"] = playerCollider.y / player["size"]

    player["isOnGround"] = False
    feetCollider = playerCollider.copy()
    feetCollider.y += 1
    
    for hitbox in solidHitboxes:
        if feetCollider.colliderect(hitbox):
            player["isOnGround"] = True
            player["fallingSpeed"] = 0
            break



def handlePlayerInput(delta_time, dy):
    global debugMode, cameraZoom, cameraXOffset, cameraYOffset, running

    keys = pygame.key.get_pressed()
    dx = 0
    speed = player["speed"]

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= speed * delta_time
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += speed * delta_time

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                debugMode = not debugMode
            if event.key == pygame.K_w and player["isOnGround"]:
                player["isJumping"] = True
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                cameraZoom = max(0.5, min(cameraZoom + 0.025, 2.5))
                resizePlayerTextures()
            elif event.y < 0:
                cameraZoom = max(0.5, min(cameraZoom - 0.025, 2.5))
                resizePlayerTextures()

    player["anyKeyPressed"] = any(keys)
    movePlayer(dx, dy)

def handlePlayerGravity(delta_time):
    if player["isOnGround"]:
        if player["isJumping"]:
            player["fallingSpeed"] = -player["jumpHeight"]
            player["isJumping"] = False
    else:
        player["fallingSpeed"] += player["gravity"] * delta_time
        player["fallingSpeed"] = player["fallingSpeed"]

    return player["fallingSpeed"] * delta_time

def debug():
    if debugMode:
        print("\n" * 25 + "Debug Mode:\n" +
        f"Player Position: {round(player['x'])}, {round(player['y'])}\n" +
        f"Camera Position: {round(cameraX)}, {round(cameraY)}\n" +
        f"Is Player On Ground: {player['isOnGround']}\n")

        
        fps = int(clock.get_fps())                                                      
        fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))
        
clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(FRAMERATE) / 1000.0

    screen.fill(WHITE)

    draw_map()
    drawPlayer()
    moveCamera(delta_time)
    
    dy = handlePlayerGravity(delta_time)
    handlePlayerInput(delta_time, dy)

    debug()
    pygame.display.flip()