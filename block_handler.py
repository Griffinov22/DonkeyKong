import pymunk
import pygame
import math
import itertools

barImage = pygame.image.load('images/bar.png')
barWidth = barImage.get_width()
barHeight = barImage.get_height()

# GLOBALS
BARS_CONFIG = [
        [(50,380), 160, 0],
        [(215,380), 140, 4]
    ]

def get_bars(space):
    '''
    This function returns all the bars for the Donkey Kong game.
    It relies on the builder function 'make_bar.'
    '''
    # config of type [start_pos, width, rotation]
    # rotation is from the top left point
    levelBarBodies = []

    for i in range(len(BARS_CONFIG)):
        pos = BARS_CONFIG[i][0]
        width = BARS_CONFIG[i][1]
        rotation = BARS_CONFIG[i][2]
        body = make_bar(pos, width, space, rotation)
        levelBarBodies.append(body)
    
    # flatten list
    flat_list = list(itertools.chain(*levelBarBodies))
    return flat_list

def make_bar(pos,width,space, rotation = 0) -> list[pymunk.Poly]:
    bars = []

    for i in range(0, width + 1, barWidth):
        barBody = pymunk.Body(1,100, pymunk.Body.STATIC)
        
        offset_y = i * math.sin(math.radians(rotation))

        barBody.position = (pos[0] + i, pos[1] - offset_y)

        barShape = pymunk.Poly.create_box(barBody, (barWidth, barHeight))
        
        space.add(barBody, barShape)
        bars.append(barShape)

    # UNCOMMENT IF YOU WANT TO HANDLE THE EXTRA SPACING
    # rightSide = width + pos[0]
    # if rightSide % barWidth != 0:
    #     extraPxWidth = rightSide % barWidth
    #     barBody = pymunk.Body(1,100, pymunk.Body.STATIC) 
    #     offset_y = (rightSide - extraPxWidth) * math.sin(math.radians(rotation))
    #     barBody.position = (rightSide, pos[1] - offset_y)
    #     barBody.angle = rotation
    #     barShape = pymunk.Poly.create_box(barBody, (barWidth, barHeight))       
    #     space.add(barBody, barShape)
    #     bars.append(barShape)

    return bars

