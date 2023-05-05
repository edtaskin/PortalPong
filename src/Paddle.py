import pygame
from constants import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = PADDLE_SPEED
        self.dir = 0 # 0 for not moving, 1 for +y, -1 for -y
        self.surf = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.surf.fill("White")
        self.score = 0
    
    def reset(self):
        self.dir = 0
        self.score = 0

class Player(Paddle):
    def __init__(self):
        super().__init__()
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH-30, SCREEN_HEIGHT/2))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > SCORE_HEIGHT:
            self.dir = -1
        elif keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.dir = 1
        else:
            self.dir = 0

    # def reflect_player(self):
    #     if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
    #         self.dir = (-1)*self.dir

    def update(self):
        self.player_input()
        self.rect.y += self.dir * self.speed

    def reset(self):
        super().reset()
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH-30, SCREEN_HEIGHT/2))


class Computer(Paddle):
    def __init__(self, ball):
        super().__init__()
        self.rect = self.surf.get_rect(center = (30, SCREEN_HEIGHT/2))
        self.ball = ball

    def move_towards_ball(self):
        if self.rect.y < self.ball.rect.y:
            if self.rect.bottom <= SCREEN_HEIGHT:
                self.dir = 1
        elif self.rect.y > self.ball.rect.y:
            if self.rect.top >= SCORE_HEIGHT:
                self.dir = -1
        else: self.dir = 0
        self.rect.y += self.dir * self.speed            

    def update(self):
        self.move_towards_ball()

    def reset(self):
        super().reset()
        self.rect.center = (30, SCREEN_HEIGHT/2)