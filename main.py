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

longBar = make_bar((50,380), 300, space, math.pi/4)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.fill((0,0,0))

    
    for i in range(len(longBar)):
        screen.blit(barImage, dest=pygame.Rect(longBar[i].bb.left, longBar[i].bb.top, longBar[i].bb.right - longBar[i].bb.left, longBar[i].bb.top - longBar[i].bb.bottom))

    
    pygame.display.flip()