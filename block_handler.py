import pymunk
import pygame

barImage = pygame.image.load('images/bar.png')
barWidth = barImage.get_width()
barHeight = barImage.get_height()

def make_bar(pos,width,space, rotation = 0) -> list[pymunk.Poly]:
    bars = []
    for i in range(pos[0],width+pos[0] + 1,barWidth):
        barBody = pymunk.Body(pymunk.Body.STATIC)
        barBody.position = (i, pos[1])
        barBody.angle = rotation

        barShape = pymunk.Segment(barBody, (barWidth, barHeight))
        barShape.body.angle = rotation

        space.add(barBody, barShape)
        bars.append(barShape)

    return bars