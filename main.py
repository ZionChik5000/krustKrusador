import pygame
import sys
import random
import math
from data import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    for h in range(len(level["map"])):
        for w in range(len(level["map"][h])):
            screen.blit(
                pygame.transform.scale(selectTile(level["map"][h][w]), (int(TILE_SIZE * cameraZoom), int(TILE_SIZE * cameraZoom))),
                ((w * TILE_SIZE - cameraX) * cameraZoom + cameraXOffset,
                 (h * TILE_SIZE - cameraY) * cameraZoom + cameraYOffset)
            )

def moveCamera():
    global cameraX, cameraY
    cameraX = cameraX + ((player["x"] - cameraX) * cameraFollowSpeed)
    cameraY = cameraY + ((player["y"] - cameraY) * cameraFollowSpeed)

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    moveCamera()
    draw_map()

    pygame.display.flip()
    clock.tick(60)
    