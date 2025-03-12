# DONKEY KONG REBUILT

# By: Griffin Overmyer
# Note to T.A: This project started in the old/ folder, but mario was glitching on the bars, so I decided to use pygame and sprites instead. Online resources were very helpful with the making of this game.
import os
import random
import pygame

os.environ["SDL_VIDEO_CENTERED"] = '1' # gets information for the full screen
pygame.init()
info = pygame.display.Info()
window_width, window_height = 500, 600

timer = pygame.time.Clock()
fps = 60

pygame.display.set_caption("Donkey Kong Rebuild 🦍🦍")
screen = pygame.display.set_mode((window_width,window_height))
# break screen up into 32x32 grid
section_width = window_width // 32
section_height = window_height // 32
# the space to bump mario up when he running into the bars
slope = section_height // 8

# bars config
start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height
row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope

# level 1
active_level = 0

# levels list[dict]
# think 'background'
levels = [{'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
                       (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
                       (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
                       (25, row2_y, 3), (22, row2_y - slope, 3),
                       (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
                       (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
                       (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
                       (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
                       (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
                       (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
                       (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
                       (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
                       (25, row4_y, 3), (22, row4_y - slope, 3),
                       (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
                       (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
                       (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
                       (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
                       (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
                       (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
                       (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
                       (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
                       (25, row6_y, 3), (22, row6_y - slope, 3),
                       (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
                       (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
                       (10, row6_y - 3 * section_height, 3)],
           'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                       (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                       (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                       (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                       (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                       (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                       (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                       (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                       (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                       (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)],
          'hammers': [(4, row6_top + section_height), (4, row4_top+section_height)],
           'target': (13, row6_y - 4 * section_height, 3)}]


class Bridge:
    def __init__(self, x,y, width):
        self.x = x * section_width
        self.y = y
        self.width = width
        self.top = self.draw()

    def draw(self):
        line_width = 3
        platform_color = (225,51,129) # you could use red or dark red
        for i in range(self.width):
            bot_coord = self.y + section_height
            left_coord = self.x + (section_width * i)
            mid_coord = left_coord + (section_width * 1/2) # half the box
            right_coord = left_coord + section_width
            top_coord = self.y
            # draws straight across
            # top boundary
            pygame.draw.line(screen, platform_color, (left_coord, top_coord), (right_coord, top_coord), line_width)
            # bottom boundary
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord), (right_coord, bot_coord), line_width)
            # draws the cross section of the bars
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord), (mid_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (mid_coord, top_coord), (right_coord, bot_coord), line_width)
        # get the top platform surface
        top_line = pygame.rect.Rect((self.x, self.y), (self.width * section_width, 2))
        # shows a line on top of bar
        # pygame.draw.rect(screen, 'blue', top_line)
        return top_line

class Ladder:
    # legth is height
    def __init__(self, x, y, length):
        self.x = x * section_width
        self.y = y
        self.length = length
        # used for if mario is climbing
        self.body = self.draw()
    
    def draw(self):
        line_width = 3
        ladder_color = 'light blue'
        for i in range(self.length):
            top = self.y + 0.6 * section_height * i
            bot = top + 0.6 * section_height
            # y position!
            mid = (0.6 / 2) * section_height + top
            left = self.x
            right = left + section_width
            # left side
            pygame.draw.line(screen, ladder_color, (left, top), (left, bot), line_width)
            # right side
            pygame.draw.line(screen, ladder_color, (right, top), (right, bot), line_width)
            # wrung (middle part)
            pygame.draw.line(screen, ladder_color, (left, mid), (right, mid), line_width)
        body = pygame.rect.Rect((self.x, self.y - section_height), (section_width, (0.6 * self.length * section_height + section_height)))
        return body


# draw platforms and ladders
def draw_screen():
    # x,y,width
    platforms = []
    # climbable ladders
    climbers = []

    ladders_objs = []
    bridges_objs = []

    bridges = levels[active_level]['bridges']
    ladders = levels[active_level]['ladders']

    for ladder in ladders:
        ladder_obj = Ladder(ladder[0],ladder[1], ladder[2])
        ladders_objs.append(ladder_obj)
        # don't allow broken ladders to be climbable (checking height)
        if ladder[2] >= 3:
            climbers.append(ladders_objs[-1].body)
    for bridge in bridges:
        bar_obj = Bridge(bridge[0],bridge[1], bridge[2])
        bridges_objs.append(bar_obj)
        platforms.append(bridges_objs[-1].top)

    return platforms, climbers



running = True
while running:
    screen.fill('black')
    timer.tick(fps)

    # draw bars and ladders using function
    plats, lads = draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    
pygame.quit()
