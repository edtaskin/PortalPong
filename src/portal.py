import pygame
from constants import *
from random import randint, choice

portals_g = pygame.sprite.Group()

class Portal(pygame.sprite.Sprite):
    def __init__(self, current_time):
        super().__init__()
        self.color = PORTAL_COLORS[choice([x for x in range(len(PORTAL_COLORS))])]
        self.rect1 = pygame.Rect(randint(200, SCREEN_WIDTH/2 - 30), randint(50, SCREEN_HEIGHT - 50), 50, 50)
        self.rect2 = pygame.Rect(randint(SCREEN_WIDTH/2 + 30, SCREEN_WIDTH - 200), randint(50, SCREEN_HEIGHT - 50), 50, 50)
        self.creation_time = current_time
        self.duration = randint(5000, 10000)
        portals_g.add(self)
    
    def update(self, current_time):
        if current_time - self.creation_time >= self.duration:
            portals_g.remove(self)
    

