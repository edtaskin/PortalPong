import pygame
from constants import *
from random import choice

MIN_BALL_SPEED = 6
MAX_BALL_SPEED = 9

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
        self.speed = MIN_BALL_SPEED
        self.rect = pygame.Rect(SCREEN_WIDTH/2 - BALL_SIZE/2, SCREEN_HEIGHT/2 - BALL_SIZE/2, BALL_SIZE, BALL_SIZE)
        self.start_cooldown_time = 0
        self.in_cooldown = False
        self.reflections_disabled = False
        self.reflections_disabled_at = 0

    def reflect_ball(self):
        if self.rect.top <= SCORE_HEIGHT or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y *= -1
    
    def update(self):
        if self.in_cooldown:
            if pygame.time.get_ticks() - self.start_cooldown_time >= BALL_RESET_COOLDOWN: 
                self.in_cooldown = False
                self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
            else:
                return

        self.reflect_ball()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.reflections_disabled and pygame.time.get_ticks() - self.reflections_disabled_at >= 300:
            self.reflections_disabled = False
            self.reflections_disabled_at = 0
    
    def reset(self):
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
        self.speed = MIN_BALL_SPEED
        self.in_cooldown = False

    def disable_reflections(self):
        self.reflections_disabled = True
        self.reflections_disabled_at = pygame.time.get_ticks()