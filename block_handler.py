import pymunk
import pygame
import math
import itertools

barImage = pygame.image.load('images/bar.png')
barWidth = barImage.get_width()
barHeight = barImage.get_height()

ladderImage = pygame.image.load('images/ladder.png')
ladderWidth = ladderImage.get_width()
ladderHeight = ladderImage.get_height()

tallBarrelImage = pygame.image.load('images/tall-barrel.png')
tallBarrelImageHeight = tallBarrelImage.get_height()
tallBarrelImageWidth = tallBarrelImage.get_width()

# GLOBALS
BARS_CONFIG = [
    # bottom bar and ending ramp
        [(50,380), 160, 0],
        [(215,380), 140, 3],
    # bar 2 
        [(50,330), 290, -3],
    # bar 3
        [(70, 300), 290, 3],
    # bar 4
        [(50, 230), 290, -3],
    # bar 5
        [(70, 200), 290, 3],
    # bar 6 small ram and bar
        [(250, 150), 90, -3],
        [(50, 150), 195, 0],
    # bar 7 princess bar
        [(150, 115), 80, 0]
    ]

LADDERS_CONFIG = [
    [(330,345), 18],
    [(200, 295), 32],
    [(100, 300), 24],
    [(150, 279), 10],
    [(150, 239), 10],
    [(223, 241), 44],
    [(330, 245), 32],
    [(300, 225), 12],
    [(300, 190), 12],
    [(180, 195), 32],
    [(80, 200), 24],
    [(205, 175), 12],
    [(205, 150), 12],
    [(320, 155), 24],
    [(225, 118), 24],
    [(135, 85), 60],
    [(115, 85), 60]
]

TALL_BARRELS_CONFIG = [
    [(50, 130)],
    [(50, 115)],
    [(60, 130)],
    [(60, 115)],
]

def get_static_background(space):
    bg = {
        "bars": {
            "items": get_bars(space),
            "image": barImage
            },
        "ladders" : {
            "items":get_ladders(space),
            "image": ladderImage
            },
        "tallBarells": {
            "items": get_tallBarrels(space),
            "image": tallBarrelImage
        }
    }
    return bg

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
        barBody = pymunk.Body(pymunk.Body.STATIC)
        
        offset_y = i * math.sin(math.radians(rotation))

        barBody.position = (pos[0] + i, pos[1] - offset_y)

        barShape = pymunk.Poly.create_box(barBody, (barWidth, barHeight))
        
        space.add(barBody, barShape)
        bars.append(barShape)

    return bars

def get_ladders(space):
    ladderBodies = []
    for i in range(len(LADDERS_CONFIG)):
        pos = LADDERS_CONFIG[i][0]
        height = LADDERS_CONFIG[i][1]
        body = make_ladder(pos, height, space)
        ladderBodies.append(body)
    flat_list = list(itertools.chain(*ladderBodies))
    return flat_list

def make_ladder(pos, height, space):
    ladders = []

    for i in range(0, height + 1, ladderHeight):
        ladderBody = pymunk.Body(pymunk.Body.STATIC)
        ladderBody.position = (pos[0], pos[1] + i)

        if i + ladderHeight > height:
            # Create a partial ladder segment for the remaining height
            remaining_height = height - i
            ladderShape = pymunk.Poly.create_box(ladderBody, (ladderWidth, remaining_height))
        else:
            ladderShape = pymunk.Poly.create_box(ladderBody, (ladderWidth, ladderHeight))

        space.add(ladderBody, ladderShape)
        ladders.append(ladderShape)

    return ladders

def get_tallBarrels(space):
    barrelBodies = []
    for i in range(len(TALL_BARRELS_CONFIG)):
        pos = TALL_BARRELS_CONFIG[i][0]
        body = make_tallBarrel(pos, space)
        barrelBodies.append(body)
    return barrelBodies

def make_tallBarrel(pos, space):
        barrelBody = pymunk.Body(pymunk.Body.STATIC)
        barrelBody.position = (pos[0], pos[1])

        barrelShape = pymunk.Poly.create_box(barrelBody, (tallBarrelImageWidth, tallBarrelImageHeight))

        space.add(barrelBody, barrelShape)
        return barrelShape
