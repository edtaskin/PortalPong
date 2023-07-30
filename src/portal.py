import pygame
from constants import *
from random import randint, choice

class Portal(pygame.sprite.Sprite):
    portals_g = pygame.sprite.Group()
    def __init__(self, current_time):
        super().__init__()
        self.color = PORTAL_COLORS[choice([x for x in range(len(PORTAL_COLORS))])]
        self.rect1 = pygame.Rect(randint(200, SCREEN_WIDTH/2 - 30), randint(50, SCREEN_HEIGHT - 50), 50, 50)
        self.rect2 = pygame.Rect(randint(SCREEN_WIDTH/2 + 30, SCREEN_WIDTH - 200), randint(50, SCREEN_HEIGHT - 50), 50, 50)
        self.consumed = False
        self.creation_time = current_time
        self.duration = randint(5000, 10000)
        Portal.portals_g.add(self)

    def isHit(self, ball):
        return ball.rect.colliderect(self.rect1) or ball.rect.colliderect(self.rect2)
    
    def hit(self, ball):
        self.consumed = True
        if ball.rect.colliderect(self.rect1):
            ball.rect.x = self.rect2.x
            ball.rect.y = self.rect2.y
            self.rect1 = None
        else:
            ball.rect.x = self.rect1.x
            ball.rect.y = self.rect1.y 
            self.rect2 = None
        self.duration = 2000

    def update(self, current_time):
        if current_time - self.creation_time >= self.duration:
            Portal.portals_g.remove(self)
    

