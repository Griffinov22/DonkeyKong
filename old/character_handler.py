import pymunk
import pygame
import COLLISIONTYPES

# MARIO --------------------------------------

def get_mario_image(state = "standing-right"):
    match state:
        case "standing-left":
            img = pygame.image.load('images/mario-idle-left.png')
        case "standing-right":
            img = pygame.image.load('images/mario-idle-right.png')
        case "running-left":
            img = pygame.image.load('images/mario-running-left.gif')
        case "running-right":
            img = pygame.image.load('images/mario-running-right.gif')
        case "jumping-left":
            img = pygame.image.load('images/mario-jump-left.png')
        case "jumping-right":
            img = pygame.image.load('images/mario-jump-right.png')
        case "mario-faint":
            img = pygame.image.load('images/mario-faint.png')
        case "mario-climb":
            img = pygame.image.load('images/mario-climb.png')
        case _:
            raise LookupError("Invalid mario state:", state)
    return img

def get_mario(space, loc):
    img = pygame.image.load('images/mario-idle-right.png')
    mario_body = pymunk.Body(1, 100, pymunk.Body.DYNAMIC)
    mario_body.position = loc
    mario_shape = pymunk.Poly.create_box(mario_body, (img.get_width(), img.get_height()))
    mario_shape.collision_type = COLLISIONTYPES.mario_coll
    mario_shape.elasticity = 0
    mario_shape.friction = 1
    space.add(mario_body, mario_shape)

    return (mario_shape, mario_body)

# DONKEY KONG ---------------------------------