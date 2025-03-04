import pygame
import pymunk
import math
from block_handler import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((400, 500))
space = pymunk.Space()
space.gravity = (0, 0)
#load font
font = pygame.font.SysFont('Arial', 30)

levelBars = get_bars(space)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.fill((0,0,0))

    for i in range(len(levelBars)):
        screen.blit(barImage, dest=pygame.Rect(levelBars[i].bb.left, levelBars[i].bb.top, levelBars[i].bb.right - levelBars[i].bb.left, levelBars[i].bb.top - levelBars[i].bb.bottom))

    
    pygame.display.flip()