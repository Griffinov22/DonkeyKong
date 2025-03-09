import pygame
import pymunk
from block_handler import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((400, 500))
space = pymunk.Space()
space.gravity = (0, 0)
#load font
font = pygame.font.SysFont('Arial', 30)

bg = get_static_background(space)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.fill((0,0,0))

    for key, bgObj in bg.items():
        for i in range(len(bgObj["items"])):
            item = bgObj["items"][i]
            image = bgObj["image"]
            rect = pygame.Rect(item.bb.left, item.bb.top, item.bb.right - item.bb.left, item.bb.top - item.bb.bottom)
            
            if rect.height < image.get_height():
                cropped_image = pygame.transform.chop(image, rect)
                screen.blit(cropped_image, rect)
            else:
                screen.blit(image, rect)


    
    pygame.display.flip()