import pygame
from constants import *
from random import choice

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
        self.speed = MIN_BALL_SPEED
        self.rect = pygame.Rect(SCREEN_WIDTH/2 - BALL_SIZE/2, SCREEN_HEIGHT/2 - BALL_SIZE/2, BALL_SIZE, BALL_SIZE)
        self.start_cooldown_time = 0
        self.in_cooldown = False

    def reflect_ball(self):
        if self.rect.top <= SCORE_HEIGHT or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y *= -1
    
    def update(self):
        self.reflect_ball()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
    
    def reset(self):
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
        self.speed = MIN_BALL_SPEED
        self.in_cooldown = False


