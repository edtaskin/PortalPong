import pygame
from constants import *
from random import randint, choice, uniform
from rectUtilities import create_rect

PORTAL_SIZE = 50
SPRINKLE_COUNT = 20
SPRINKLE_SIZE = 5
ANIMATION_DURATION = 3000
UNHIT_PORTAL_DURATION = 1000

class Portal(pygame.sprite.Sprite):
    def __init__(self, current_time):
        super().__init__()
        self.color = PORTAL_COLORS[choice([x for x in range(len(PORTAL_COLORS))])]
        self.rect1 = create_rect(randint(200, SCREEN_WIDTH/2 - 30), randint(SCORE_HEIGHT + 30, SCREEN_HEIGHT - PORTAL_SIZE), PORTAL_SIZE, PORTAL_SIZE)
        self.rect2 = create_rect(randint(SCREEN_WIDTH/2 + 30, SCREEN_WIDTH - 200), randint(SCORE_HEIGHT + 30, SCREEN_HEIGHT - PORTAL_SIZE), PORTAL_SIZE, PORTAL_SIZE)
        self.sprinkles = [] # Store smaller rects for the animation
        self._sprinkle_directions = []
        self._consumed = False
        self._creation_time = current_time
        self._duration = randint(5000, 10000)

    def is_consumed(self):
        return self._consumed
    

    def is_hit(self, ball):
        return ball.rect.colliderect(self.rect1) or ball.rect.colliderect(self.rect2)
    
    def hit(self, ball, current_time):
        self._consumed = True
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
        self._creation_time = current_time
        self._duration = ANIMATION_DURATION

    def update(self, current_time):
        if current_time - self._creation_time >= self._duration:
            Portal.portals_g.remove(self)
        elif self.is_consumed():
            if current_time - self._creation_time >= UNHIT_PORTAL_DURATION:
                if self.rect1 != None:
                    self.rect1 = None
                elif self.rect2 != None:
                    self.rect2 = None
            for rect, dir in zip(self.sprinkles, self._sprinkle_directions):
                rect.x += dir[0]
                rect.y += dir[1]
    
    def play_animation(self, rect):
        x, y = rect.x, rect.y
        for i in range(SPRINKLE_COUNT):
            self.sprinkles.append(create_rect(x, y, SPRINKLE_SIZE, SPRINKLE_SIZE))
            self._sprinkle_directions.append((uniform(-3, 3), uniform(-3, 3)))
        


