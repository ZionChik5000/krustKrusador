import pygame
import sys
import random
from data import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Krust Krusador")
tile = pygame.image.load("assets/tile.png")

clock = pygame.time.Clock()
running = True

def draw_map():
    for h in range(len(level.map)):
        for w in range(len(level.map[h])):
            screen.blit(
                pygame.transform.scale(tile, (int(TILE_SIZE * cameraZoom), int(TILE_SIZE * cameraZoom))),
                ((w * TILE_SIZE - cameraX) * cameraZoom + cameraXOffset,
                 (h * TILE_SIZE - cameraY) * cameraZoom + cameraYOffset)
            )

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_map()
    
    pygame.display.flip()
    clock.tick(60)
    