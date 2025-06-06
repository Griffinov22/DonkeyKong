# DONKEY KONG REBUILT

# By: Griffin Overmyer
# Note to T.A: This project started in the old/ folder, but mario was glitching on the bars using pymunk, so I decided to use pygame and sprites instead of pymunk with pygame. Online resources were very helpful with the making of this game. Any questions about how it works should be directed towards me. Thank you. The only requirement per the assignment was to use Pygame in your python game. Thank you for reading, and I hope you enjoy the game. (:

import os
import random
import pygame

os.environ["SDL_VIDEO_CENTERED"] = '1' # gets information for the full screen
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width - 800, screen_height - 150

timer = pygame.time.Clock()
fps = 60
clicked_x = False

pygame.display.set_caption("Donkey Kong Rebuild 🦍🦍")

font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 30)

screen = pygame.display.set_mode((window_width,window_height))
# break screen up into 32x32 grid
section_width = window_width // 32
section_height = window_height // 32
# the space to bump mario up when he running into the bars
slope = section_height // 8

# barrels spawn roughly every 6 seconds (60fps * 6s = 360)
barrel_spawn_time = 360
barrel_count = barrel_spawn_time / 2
barrel_time = 360
# rolling barrel // play with scale numbers
barrel_img = pygame.transform.scale(pygame.image.load("assets/barrels/barrel.png"), (section_width * 1.5, section_height * 2))
barrel_side = pygame.transform.scale(pygame.image.load("assets/barrels/barrel2.png"), (section_width * 2, section_height * 2.5))

# dk
# 1 - picking up or rolling / 2 - front facing / 3 - front facing with barrel
dk1 = pygame.transform.scale(pygame.image.load("assets/dk/dk1.png"), (section_width * 5, section_height * 5))
dk2 = pygame.transform.scale(pygame.image.load("assets/dk/dk2.png"), (section_width * 5, section_height * 5))
dk3 = pygame.transform.scale(pygame.image.load("assets/dk/dk3.png"), (section_width * 5, section_height * 5))

# peach
peach1 = pygame.transform.scale(pygame.image.load("assets/peach/peach1.png"), (2 * section_width, 3 * section_height))
peach2 = pygame.transform.scale(pygame.image.load("assets/peach/peach2.png"), (2 * section_width, 3 * section_height))

# fireball
fireball = pygame.transform.scale(pygame.image.load("assets/fireball.png"), (1.5 * section_width, 2 * section_height))
fireball2 = pygame.transform.scale(pygame.image.load("assets/fireball2.png"), (1.5 * section_width, 2 * section_height))

# flame image
flames_img = pygame.transform.scale(pygame.image.load("assets/fire.png"), (section_width * 2, section_height))

# flame image
hammer = pygame.transform.scale(pygame.image.load("assets/hammer.png"), (section_width * 2, section_height * 2))

# mario images
standing = pygame.transform.scale(pygame.image.load("assets/mario/standing.png"), (section_width * 2, section_height * 2.5))
jumping = pygame.transform.scale(pygame.image.load("assets/mario/jumping.png"), (section_width * 2, section_height * 2.5))
running = pygame.transform.scale(pygame.image.load("assets/mario/running.png"), (section_width * 2, section_height * 2.5))
climbing1 = pygame.transform.scale(pygame.image.load("assets/mario/climbing1.png"), (section_width * 2, section_height * 2.5))
climbing2 = pygame.transform.scale(pygame.image.load("assets/mario/climbing2.png"), (section_width * 2, section_height * 2.5))

hammer_stand = pygame.transform.scale(pygame.image.load("assets/mario/hammer_stand.png"), (section_width * 2.5, section_height * 2.5))
hammer_jump = pygame.transform.scale(pygame.image.load("assets/mario/hammer_jump.png"), (section_width * 2.5, section_height * 2.5))
hammer_overhead = pygame.transform.scale(pygame.image.load("assets/mario/hammer_overhead.png"), (section_width * 2.5, section_height * 3.5))


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
# expand levels array to more levels (but this is already taking 40+ hrs)
active_level = 0

# should spawn fireball
fireball_trigger = False

# 1s counter for fps drawing (0-59)
counter = 0

# player score
score = 0
high_score = 0
bonus = 6000
lives = 3
reset_game = False
first_fireball_trigger = False
# have to reach 'target' platform in levels config to win
victory = False

# levels list[dict]
# think 'background'
levels = [
    {'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.y_change = 0
        self.x_speed = 3
        self.x_change = 0
        self.landed = False
        self.pos = 0
        # left = 0, right = 1
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = standing
        self.hammer = False
        # how long to hold the hammer
        self.max_hammer = 450
        self.hammer_len = self.max_hammer
        self.hammer_pos = 1
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hammer_box = self.rect
        self.rect.center = (x,y)
        self.over_barrel = False
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)

    def update(self):
        self.landed = False
        for i in range(len(plats)):
            if (self.bottom.colliderect(plats[i])):
                self.landed = True
                if not self.climbing:
                    # push player above the platform
                    self.rect.centery = plats[i].top - self.rect.height / 2 + 1

        if not self.landed and not self.climbing:
            self.y_change += 0.25
        self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        # animate up and down
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            # just standing still or default climbing pos.
            self.pos = 0

        if self.hammer:
            # how frequent mario swings hammer
            self.hammer_pos = (self.hammer_len // 30) % 2
            self.hammer_len -= 1
            
            if self.hammer_len == 0:
                self.hammer = False
                self.hammer_len = self.max_hammer

    def draw(self):
        if not self.hammer:
            if not self.climbing and self.landed:
                if self.pos == 0:
                    self.image = standing
                else:
                    self.image = running

            if not self.landed and not self.climbing:
                self.image = jumping
            if self.climbing:
                if self.pos == 0:
                    self.image = climbing1
                else:
                    self.image = climbing2
        else:
            # have the hammer
            if self.hammer_pos == 0:
                self.image = hammer_jump
            else:
                self.image = hammer_overhead
            
        
        if self.dir == -1:
            # going left
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
        
        self.calc_hitbox()

        if self.hammer_pos == 1 and self.hammer:
            screen.blit(self.image, (self.rect.left, self.rect.top - section_height))
        else:
            screen.blit(self.image, self.rect.topleft)

    def calc_hitbox(self):
        # used for hammer, ladder, etc..
        if not self.hammer:
            # no hammer // making inset margin spacing for hit box
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5), 
            (self.rect[2] - 30, self.rect[3] - 10))
        elif self.hammer_pos == 0:
            # holding hammer out
            if self.dir == 1:
                self.hitbox = pygame.rect.Rect((self.rect[0], self.rect[1] + 5), 
            (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] + self.hitbox[2], self.rect[1] + 5), (self.hitbox[2], self.rect[3] - 10))
            else:
                self.hitbox = pygame.rect.Rect((self.rect[0] + 40, self.rect[1] + 5), 
            (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] - self.hitbox[2], self.rect[1] + 5), (self.hitbox[2], self.rect[3] - 10))
        else:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5), 
            (self.rect[2] - 30, self.rect[3] - 10))
            self.hammer_box = pygame.rect.Rect((self.hitbox[0], self.hitbox[1] - section_height), (self.hitbox[2], section_height))

class Hammer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = hammer
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x * section_width
        # has the hammer been used?
        self.used = False

    def draw(self):
        if not self.used:
            screen.blit(self.image, (self.rect[0], self.rect[1]))
            
            if self.rect.colliderect(player.hitbox):
                self.kill()
                player.hammer = True
                # reset max hammer time
                player.hammer_len = player.max_hammer
                self.used = True

class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((47, 47))
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = 1
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        self.bottom = self.rect

    def update(self, fire_trig):
        if self.y_change < 8 and not self.falling:
            barrel.y_change += 2
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.y_change = 0
                self.falling = False
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                if random.randint(0, 4) == 4:
                    fire_trig = True
        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                self.x_change = 3
            else:
                self.x_change = -3
        else:
            self.x_change = 0
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height:
            self.kill()
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3
        self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom), (self.rect[2], 3))
        return fire_trig

    def check_fall(self):
        already_collided = False
        below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height))
        for lad in lads:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0, 60) == 60:
                    self.falling = True
                    self.y_change = 4
        if not already_collided:
            self.check_lad = False

    def draw(self):
        screen.blit(pygame.transform.rotate(barrel_img, 90 * self.pos), self.rect.topleft)

# inherit from sprite
class Flame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = 1
        self.count = 0
        # bounce in random pattern, but go forward
        self.x_count = 0
        self.x_change = 2
        self.x_max = 4
        self.y_change = 0
        self.row = 1
        # climbing ladder?
        self.check_lad = False
        self.climbing = False

    def update(self):
        if self.y_change < 3 and not flame.climbing:
            # fall
            flame.y_change += 0.25

        for i in range(len(plats)):
            if self.rect.colliderect(plats[i]):
                flame.climbing = False
                # makes it look like it's bouncing
                flame.y_change = -4
        # if flame collides with players hitbox - trigger reset of game (also barrels) // count 1/4s
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            # animation
            self.pos *= -1
            if self.x_count < self.x_max:
                self.x_count += 1
            else:
                #  row 1,3, and 5 go further right than left overall, otherwise flip
                self.x_count = 0
                if self.x_change > 0:
                    if self.row in [1,3,5]:
                        # go to the right more than left
                        self.x_max = random.randint(3,6)
                    else:
                        self.x_max = random.randint(6,10)
                else:
                    if self.row in [1,3,5]:
                        # go to the right more than left
                        self.x_max = random.randint(6,10)
                    else:
                        self.x_max = random.randint(3,6)
                # change direction
                self.x_change *= -1 
        if self.pos == 1:
            if self.x_change > 0:
                self.image = fireball
            else:
                self.image = pygame.transform.flip(fireball, True, False)
        else:
            if self.x_change > 0:
                self.image = fireball2
            else:
                self.image = pygame.transform.flip(fireball2, True, False)
        # move fireball
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height or self.rect.top < 0:
            # if goes off bottom of screen
            self.kill()
            

    def check_climb(self):
        already_collided = False
        for lad in lads:
            if self.rect.colliderect(lad) and not self.climbing and not self.check_lad:
                self.check_lad = True
                already_collided = True

                # checked very frequently, tweak if need
                if random.randint(0,120) == 120:
                    self.climbing = True
                    self.y_change = -4

        if not already_collided:
            # not hitting a ladder
            self.check_lad = False
        
        if self.rect.bottom < row6_y:
            self.row = 6
        elif self.rect.bottom < row5_y:
            self.row = 5
        elif self.rect.bottom < row4_y:
            self.row = 4
        elif self.rect.bottom < row3_y:
            self.row = 3
        elif self.rect.bottom < row2_y:
            self.row = 2
        else:
            self.row = 1

class Bridge:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 7
        platform_color = (225, 51, 129)
        for i in range(self.length):
            bot_coord = self.y_pos + section_height
            left_coord = self.x_pos + (section_width * i)
            mid_coord = left_coord + (section_width * 0.5)
            right_coord = left_coord + section_width
            top_coord = self.y_pos
            # draw 4 lines, top, bot, left diag, right diag
            pygame.draw.line(screen, platform_color, (left_coord, top_coord),
                             (right_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (mid_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (mid_coord, top_coord),
                             (right_coord, bot_coord), line_width)
        # get the top platform 'surface'
        top_line = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))
        # pygame.draw.rect(screen, 'blue', top_line)
        return top_line

class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        lad_color = 'light blue'
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(screen, lad_color, (left_coord, top_coord), (left_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (right_coord, top_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height),
                                (section_width, (lad_height * self.length * section_height + section_height)))
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

def draw_extras():
    # lives, level, bonus text
    screen.blit(font.render(f'I•{score}', True, 'white'), (3*section_width, 2*section_height))
    screen.blit(font.render(f'TOP•{high_score}', True, 'white'), (14 * section_width, 2 * section_height))
    screen.blit(font.render(f'[  ][        ][  ]', True, 'white'), (20 * section_width, 4 * section_height))
    screen.blit(font2.render(f'  M    BONUS     L ', True, 'white'), (20 * section_width + 5, 4 * section_height))
    screen.blit(font2.render(f'  {lives}       {bonus}        {active_level + 1}  ', True, 'white'),
                (20 * section_width + 5, 5 * section_height))
    # draw peach (simple doesn't need a function)
    if barrel_count < barrel_spawn_time / 2:
        screen.blit(peach1, (10 * section_width, row6_y - 6 * section_height))
    else:
        screen.blit(peach2, (10 * section_width, row6_y - 6 * section_height))
    # draw oil drum
    oil = draw_oil()
    # draw stationary barrels by dk
    draw_barrels()
    # draw dk
    draw_kong()

    return oil

def draw_oil():
    # math based on section width and height to get the right size. DO NOT TOUCH
    x_coord, y_coord = 4 * section_width, window_height - 4.5 * section_height
    oil = pygame.draw.rect(screen, 'blue', [x_coord, y_coord, 2 * section_width, 2.5 * section_height])
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 * section_width, y_coord, 2.2 * section_width, .2 * section_height])
    pygame.draw.rect(screen, 'blue',
                     [x_coord - 0.1 * section_width, y_coord + 2.3 * section_height, 2.2 * section_width,
                      .2 * section_height])
    pygame.draw.rect(screen, 'light blue',
                     [x_coord + 0.1 * section_width, y_coord + .2 * section_height, .2 * section_width,
                      2 * section_height])
    pygame.draw.rect(screen, 'light blue',
                     [x_coord, y_coord + 0.5 * section_height, 2 * section_width, .2 * section_height])

    pygame.draw.rect(screen, 'light blue',
                     [x_coord, y_coord + 1.7 * section_height, 2 * section_width, .2 * section_height])
    
    # antialias = True (smooths out fonts)
    screen.blit(font2.render('OIL', True, 'light blue'), (x_coord + .4 * section_width, y_coord + 0.7 * section_height))
    for i in range(4):
        pygame.draw.circle(screen, 'red',
                           (x_coord + 0.5 * section_width + i * 0.4 * section_width, y_coord + 2.1 * section_height), 3)
    # draw the flames on top
    if counter < 15 or 30 < counter < 45:
        screen.blit(flames_img, (x_coord, y_coord - section_height))
    else:
        # flip x = True, y = False
        screen.blit(pygame.transform.flip(flames_img, True, False), (x_coord, y_coord - section_height))
    return oil

def draw_barrels():
    # rotate barrel to upright pos
    screen.blit(pygame.transform.rotate(barrel_side, 90),(section_width * 1.2, section_height * 6.4))
    screen.blit(pygame.transform.rotate(barrel_side, 90),(section_width * 2.5, section_height * 6.4))
    screen.blit(pygame.transform.rotate(barrel_side, 90),(section_width * 2.5, section_height * 8.7))
    screen.blit(pygame.transform.rotate(barrel_side, 90),(section_width * 1.2, section_height * 8.7))
    
def draw_kong():
    phase_time = barrel_time // 4

    if barrel_spawn_time - barrel_count > 3 * phase_time:
        # draw last dk image
        dk_img = dk2
    elif barrel_spawn_time - barrel_count > 2 * phase_time:
        dk_img = dk1
    elif barrel_spawn_time - barrel_count > phase_time:
        dk_img = dk3
    else:
        # flip dk1
        dk_img = pygame.transform.flip(dk1, True, False)
        screen.blit(barrel_img, (250,250))
    screen.blit(dk_img, (3.5 * section_width, row6_y - 5.5 * section_height))

def check_climb():
    can_climb = False
    climb_down = False

    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))

    for lad in lads:
        if player.hitbox.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    
    # check to push player off the ladder
    if (not can_climb and (not climb_down or player.y_change < 0)) or \
        (player.landed and can_climb and player.y_change > 0 and not climb_down):
        player.climbing = False

    return can_climb, climb_down

def barrel_collide(reset):
    global score
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))

    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True
        elif not player.landed and not player.over_barrel and under.colliderect(brl.rect):
            player.over_barrel = True
            score += 100

    if player.landed:
        player.over_barrel = False

    return reset

def reset():
    global player, barrels, flames, hammers, first_fireball_trigger, victory, lives, bonus, barrel_spawn_time, barrel_count
    # pause game for 1.5s (freeze frame)
    pygame.time.delay(1500) 
    for bar in barrels:
        bar.kill()
    for flam in flames:
        flam.kill()
    for hams in hammers:
        hams.kill()
    for hams in hammers_list:
        hammers.add(Hammer(hams[0], hams[1]))

    lives -= 1
    bonus = 6000
    player.kill()
    player = Player(250, window_height - 130)
    first_fireball_trigger = False
    barrel_spawn_time = 360
    barrel_count = barrel_spawn_time / 2
    victory = False

def check_victory():
    target = levels[active_level]['target']
    target_rect = pygame.rect.Rect((target[0] * section_width, target[1]), (section_width * target[2], 1))
    # is player standing on target platform?
    return player.bottom.colliderect(target_rect)

barrels = pygame.sprite.Group()
flames = pygame.sprite.Group()
hammers = pygame.sprite.Group()
hammers_list = levels[active_level]['hammers']
# initiate hammers based on level list
# hammer is set up as (x,y)
for ham in hammers_list:
    hammers.add(Hammer(ham[0], ham[1]))

player = Player(250, window_height - 130)

run = True
while run:
    screen.fill('black')
    timer.tick(fps)

    if counter < 60:
        counter += 1
    else:
        counter = 0
        # subtract 100 from bonus
        if bonus > 0:
            bonus -= 100

    # draw bars and ladders using function
    plats, lads = draw_screen()
    # dk, oil barrel, barrels next to dk
    oil_drum = draw_extras()
    # help mario climb up and get off on ladders
    climb, down = check_climb()
    # is player on target platform?
    victory = check_victory()

    # barrel_count - time since last spawn
    if barrel_count < barrel_spawn_time:
        barrel_count += 1
    else:
        # setting rand time to spawn
        barrel_count = random.randint(0,120)
        # time for donkey kong to throw the barrel
        barrel_time = barrel_spawn_time - barrel_count 
        # location to drop barrel on top row bar
        barrel = Barrel(270,270)
        barrels.add(barrel)
        # add first fireball when first barrel spawns
        if not first_fireball_trigger:
            flame = Flame(5*section_width, window_height - 4 * section_height)
            flames.add(flame)
            first_fireball_trigger = True
    
    for barrel in barrels:     
        # draw rolling barrels
        barrel.draw()
        barrel.check_fall()
        fireball_trigger = barrel.update(fireball_trigger)
        # check if hammer smashes barrel
        if barrel.rect.colliderect(player.hammer_box) and player.hammer:
            barrel.kill()
            score += 500

    if fireball_trigger:
        # yes, this is random, but it works well
        flame = Flame(5 * section_width, window_height - 4 * section_height)
        flames.add(flame)
        fireball_trigger = False

    for flame in flames:
        # have to use for loop because this method is not in Sprite groups
        flame.check_climb()
        if flame.rect.colliderect(player.hitbox):
            reset_game = True
        
    flames.draw(screen)
    flames.update()

    # mario update
    player.update()
    player.draw()

    # hammer
    for ham in hammers:
        ham.draw()

    # checking reset game
    reset_game = barrel_collide(reset_game)
    if reset_game:
        if lives > 0:
            reset()
            reset_game = False
        else:
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            clicked_x = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not player.climbing:
                player.x_change = 1
                player.dir = 1
            if event.key == pygame.K_LEFT and not player.climbing:
                player.x_change = -1
                player.dir = -1
            if event.key == pygame.K_SPACE and player.landed:
                player.landed = False
                player.y_change = -6
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = -2
                    player.x_change = 0
                    player.climbing = True
            if event.key == pygame.K_DOWN:
                if down:
                    player.y_change = 2
                    player.x_change = 0
                    player.climbing = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_LEFT:
                player.x_change = 0
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = 0
            if event.key == pygame.K_DOWN:
                if down:
                    player.y_change = 0
                if player.climbing and player.landed:
                    # push player onto platform
                    player.climbing = False

    if victory:
        win_message = font.render("VICTORY!", True, 'white', 'black')
        screen.blit(win_message, ((window_width - win_message.get_width()) / 2, (window_height - win_message.get_height()) / 2))
        pygame.display.flip()

        score += bonus
        # terminate game loop
        run = False
        pygame.time.delay(3000)

        # extras if want to add more levels
        # reset_game = True
        # active_level += 1
        # lives += 1
        # if score > high_score:
        #     high_score = score
        # player.climbing = False
            
    pygame.display.flip()

if clicked_x:
    pygame.quit()
else:
    screen.fill('black')
    top_message = font.render(f"YOU {"WON" if victory else "LOST"}", True, 'white')
    mid_message = font.render(f"Thanks for playing!", True, 'white')
    bot_message = font.render(f"By Griffin Overmyer", True, 'white')
    messages_list = [top_message, mid_message, bot_message]

    screen.blit(top_message, ((window_width - top_message.get_width()) / 2, (window_height - top_message.get_height() - 200) / 2))
    screen.blit(mid_message, ((window_width - mid_message.get_width()) / 2, (window_height - mid_message.get_height()) / 2))
    screen.blit(bot_message, ((window_width - bot_message.get_width()) / 2, (window_height - bot_message.get_height() + 200) / 2))


    pygame.display.flip()

    waiting_to_exit = True
    while waiting_to_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_to_exit = False
    pygame.quit()

