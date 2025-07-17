import pygame
import sys
import random
import math
from data import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 30)
pygame.display.set_caption("Krust Krusador")

clock = pygame.time.Clock()
running = True

def selectTile(tileType):
    match tileType:
        case 0:
            return pygame.image.load("assets/empty.png")
        case 1:
            return pygame.image.load("assets/tile.png")
        case -1:
            return pygame.image.load("assets/empty.png")

def draw_map():
    tile_map = level["map"]
    rows = len(tile_map)
    cols = len(tile_map[0]) if rows > 0 else 0

    scaled_size = int(TILE_SIZE * cameraZoom)
    offset_x = -cameraX * cameraZoom + cameraXOffset
    offset_y = -cameraY * cameraZoom + cameraYOffset

    screen_width, screen_height = screen.get_size()

    start_col = max(0, int((-offset_x) // scaled_size))
    end_col = min(cols, int((-offset_x + screen_width) // scaled_size) + 1)
    
    start_row = max(0, int((-offset_y) // scaled_size))
    end_row = min(rows, int((-offset_y + screen_height) // scaled_size) + 1)

    scaled_tiles_cache = {}

    for h in range(start_row, end_row):
        y = h * scaled_size + offset_y
        row = tile_map[h]

        for w in range(start_col, end_col):
            x = w * scaled_size + offset_x
            tile_id = row[w]

            if tile_id not in scaled_tiles_cache:
                scaled_tiles_cache[tile_id] = pygame.transform.scale(
                    selectTile(tile_id), (scaled_size, scaled_size)
                )
            screen.blit(scaled_tiles_cache[tile_id], (x, y))



def moveCamera():
    global cameraX, cameraY
    cameraX = cameraX + ((player["x"] - cameraX) * cameraFollowSpeed)
    cameraY = cameraY + ((player["y"] - cameraY) * cameraFollowSpeed)


def handlePlayerInput(delta_time):
    keys = pygame.key.get_pressed()
    
    dx, dy = 0, 0
    speed = player["speed"]
    
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= speed * delta_time
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += speed * delta_time
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= speed * delta_time
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += speed * delta_time

    player["x"] += dx
    player["y"] += dy

    

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                   
    delta_time = clock.tick(60)


    moveCamera()
    handlePlayerInput(delta_time)
    draw_map()

    fps = int(clock.get_fps())                                                      
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(1000)
    