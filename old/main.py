import pygame
import pymunk
from block_handler import *
from character_handler import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((400, 500))
space = pymunk.Space()
space.gravity = (0, 100)
font = pygame.font.SysFont('Arial', 30)

# CHARACTERS
mario_x = 100
mario_y = 370
(mario_shape, mario_body) = get_mario(space, (mario_x, mario_y))
mario_img = get_mario_image()
mario_speed = 1

#BG
bg = get_static_background(space)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        # MARIO CONTROLS ----------------------- 
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RIGHT:
                    pass
                case pygame.K_LEFT:
                    pass
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_RIGHT:
                    mario_img = get_mario_image("standing-right")
                case pygame.K_LEFT:
                    mario_img = get_mario_image("standing-left")

    keys = pygame.key.get_pressed()
    if  keys[pygame.K_RIGHT]:
        mario_body.velocity = (mario_speed, mario_body.velocity.y)
    elif keys[pygame.K_LEFT]:
        mario_body.velocity = (-mario_speed, mario_body.velocity.y)

    # update physics and redraw
    screen.fill((0,0,0))
    space.step(1/60.0)

    draw_bg(screen, bg)
    draw_image(screen, mario_body, mario_shape, mario_img)
    
    pygame.display.update()