import pygame
from constants import *
from random import randint, choice, uniform
from rectUtilities import create_rect

PORTAL_SIZE = 50
SPRINKLE_COUNT = 20
SPRINKLE_SIZE = 5
ANIMATION_DURATION = 3000

class Portal(pygame.sprite.Sprite):
    portals_g = pygame.sprite.Group()
    def __init__(self, current_time):
        super().__init__()
        self.color = PORTAL_COLORS[choice([x for x in range(len(PORTAL_COLORS))])]
        self.rect1 = create_rect(randint(200, SCREEN_WIDTH/2 - 30), randint(SCORE_HEIGHT + 30, SCREEN_HEIGHT - PORTAL_SIZE), PORTAL_SIZE, PORTAL_SIZE)
        self.rect2 = create_rect(randint(SCREEN_WIDTH/2 + 30, SCREEN_WIDTH - 200), randint(SCORE_HEIGHT + 30, SCREEN_HEIGHT - PORTAL_SIZE), PORTAL_SIZE, PORTAL_SIZE)
        self.sprinkles = [] # Store smaller rects for the animation
        self.sprinkle_directions = []
        self.consumed = False
        self.creation_time = current_time
        self.duration = randint(5000, 10000)
        Portal.portals_g.add(self)

    def isHit(self, ball):
        return ball.rect.colliderect(self.rect1) or ball.rect.colliderect(self.rect2)
    
    def hit(self, ball, current_time):
        self.consumed = True
        if ball.rect.colliderect(self.rect1):
            ball.rect.x = self.rect2.x
            ball.rect.y = self.rect2.y
            self.play_animation(self.rect1)
            self.rect1 = None
        else:
            ball.rect.x = self.rect1.x
            ball.rect.y = self.rect1.y 
            self.play_animation(self.rect2)
            self.rect2 = None
        self.creation_time = current_time
        self.duration = ANIMATION_DURATION

    def update(self, current_time):
        if current_time - self.creation_time >= self.duration:
            Portal.portals_g.remove(self)
        elif self.consumed:
            for rect, dir in zip(self.sprinkles, self.sprinkle_directions):
                rect.x += dir[0]
                rect.y += dir[1]
    
    def play_animation(self, rect):
        x, y = rect.x, rect.y
        for i in range(SPRINKLE_COUNT):
            self.sprinkles.append(create_rect(x, y, SPRINKLE_SIZE, SPRINKLE_SIZE))
            self.sprinkle_directions.append((uniform(-3, 3), uniform(-3, 3)))
        


