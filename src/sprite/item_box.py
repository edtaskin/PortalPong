from rectangle import Rectangle
from util.rect_util import create_rect
import os
from random import randint, choice
from constants import *
import pygame
from game_state_manager import game_state_manager

class ItemBox(pygame.sprite.Sprite):
    BOX_SIZE = 50
    RESOURCE_PATH = "resources/pixel_art/item_box"
    def __init__(self):
        super().__init__()
        self.images = [os.path.join(ItemBox.RESOURCE_PATH, file_name) for file_name in os.listdir(ItemBox.RESOURCE_PATH)]
        random_img_path = choice(self.images)
        self.image = pygame.image.load(random_img_path)
        self.image = pygame.transform.scale(self.image, (ItemBox.BOX_SIZE, ItemBox.BOX_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (randint(200, SCREEN_WIDTH - 200), randint(SCORE_HEIGHT + 30, SCREEN_HEIGHT - ItemBox.BOX_SIZE))
        self._consumed = False
        self._creation_time = pygame.time.get_ticks()
        self._duration = randint(5000, 10000)

    
    def draw(self, screen):
        if self.rect is not None:
            screen.blit(self.image, self.rect) 

    def is_consumed(self):
        return self._consumed
    

    def is_outdated(self):
        current_time = pygame.time.get_ticks()
        return current_time - self._creation_time >= self._duration
    

    def is_hit(self, ball):
        return ball.rect.colliderect(self.rect)
    

    def hit(self, ball, current_time):
        self._consumed = True
        if ball.rect.colliderect(self.rect):
            pass #TODO


    def update(self):
        if not self.is_consumed():
            return
        
        if self.is_outdated():
            self.rect = None