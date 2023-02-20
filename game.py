import pygame
from sys import exit
from random import randint, choice
from math import sin, cos

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.pos = pygame.math.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
        self.speed = MIN_BALL_SPEED
        # self.dir = pygame.math.Vector2((choice([-1,1]), 0))
        self.surf = pygame.Surface((BALL_SIZE,BALL_SIZE))
        self.surf.fill("White")
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    def reflect_ball(self):
        global player_win
        if self.rect.left <= 0:
            player_win = True
            # self.velocity.x *= -1
        if self.rect.right >= SCREEN_WIDTH:
            player_win = False
            # self.velocity.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y *= -1

    # def reflect(self, normal_vector):
    #     self.dir = self.dir.reflect(normal_vector)
    
    def update(self):
        self.reflect_ball()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
    
    def reset(self):
        self.velocity = pygame.math.Vector2(MIN_BALL_SPEED * choice([-1,1]), MIN_BALL_SPEED * choice([-1,1]))
        self.speed = MIN_BALL_SPEED
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = PADDLE_SPEED
        self.dir = 0 # 0 for not moving, 1 for +y, -1 for -y
        self.surf = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.surf.fill("White")

class Player(Paddle):
    def __init__(self):
        super().__init__()
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH-30, SCREEN_HEIGHT/2))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
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
        # self.rect.center = (round(self.rect.x), round(self.rect.y))

    def reset(self):
        self.dir = 0
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH-30, SCREEN_HEIGHT/2))

class Computer(Paddle):
    def __init__(self):
        super().__init__()
        self.rect = self.surf.get_rect(center = (30, SCREEN_HEIGHT/2))
        self.target_y = 0
        # self.track_ball = False

    def move_towards_ball(self): # Func outside class?
        global ball
        if self.rect.y < ball.rect.y:
            if self.rect.bottom <= SCREEN_HEIGHT:
                self.dir = 1
        elif self.rect.y > ball.rect.y:
            if self.rect.top >= 0:
                self.dir = -1
        else: self.dir = 0
        print(self.dir)
        self.rect.y += self.dir * self.speed
                

    def update(self):
        self.move_towards_ball()

    def reset(self):
        self.rect.center = (30, SCREEN_HEIGHT/2)

def set_title_screen():
    screen.blit(title, title_rect)
    screen.blit(title_msg, title_msg_rect)

def set_game_screen(screen):
    screen.fill("Black")
    screen.blit(ball.surf, ball.rect)
    screen.blit(player.surf, player.rect)
    screen.blit(comp.surf, comp.rect)
    # pygame.draw(screen, "Grey", middle_line) # TODO
    # screen.blit(top_surf, top_rect)
    # screen.blit(bottom_surf, bottom_rect)

def sprite_collision(ball_group, player_group):
    for ball in ball_group:
        for player in player_group:
            if player.rect.colliderect(ball.rect):
                pos_from_paddle_center = player.rect.y - ball.rect.y
                normalized_pos = pos_from_paddle_center/(PADDLE_HEIGHT/2)
                bounce_angle = normalized_pos * MAX_BOUNCE_ANGLE
                ball.speed = normalized_pos * MAX_BALL_SPEED 
                if ball.speed < MIN_BALL_SPEED: ball.speed = MIN_BALL_SPEED
                ball.velocity.x = ball.speed * cos(bounce_angle)
                ball.velocity.y = ball.speed * sin(bounce_angle)
                if player is Computer:
                    player.target_y = 0

def game_over(ball):
    screen.fill("Black")
    set_title_screen()
    if ball.rect.right >= SCREEN_WIDTH:
        screen.blit(loss_msg, loss_msg_rect)
    else:
        screen.blit(win_msg, win_msg_rect)


#TODO
# def game_over_msg_animation(msg_rect):
#     if msg_rect.top <= 0:


pygame.init()
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
BALL_SIZE = 20
MAX_BOUNCE_ANGLE = 75
PADDLE_SPEED = 4
MIN_BALL_SPEED = 6
MAX_BALL_SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

title_font = pygame.font.Font("font\VT323-Regular.ttf", 80)
msg_font = pygame.font.Font("font\VT323-Regular.ttf", 50)

game_active = False
player_win = None
start_time = 0

middle_line = pygame.Rect(SCREEN_WIDTH/2-2, 0, 4, SCREEN_HEIGHT)
# Title screen
# TODO Animation
title = title_font.render("Pong", False, "White")
title_rect = title.get_rect(center = (SCREEN_WIDTH/2,80))

title_msg = msg_font.render("Press Space to start", False, "White")
title_msg_rect = title_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-100))

loss_msg = msg_font.render("YOU LOSE", False, "Red")
loss_msg_rect = loss_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

win_msg = msg_font.render("YOU WIN", False, "Green")
win_msg_rect = win_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# Game
# top_surf = pygame.Surface((SCREEN_WIDTH, 10))
# top_surf.fill("White")
# top_rect = top_surf.get_rect(midbottom = (SCREEN_WIDTH/2,10))
# bottom_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT-10))
# bottom_surf.fill("White")
# bottom_rect = bottom_surf.get_rect(midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT-10))

def update_components():
    player.update()
    comp.update()
    ball.update()

def reset_components(ball, player):
    global player_win
    ball.reset()
    player.reset()
    comp.reset()
    player_win = None

ball = Ball()
player = Player()
comp = Computer()

# Groups
ball_sg = pygame.sprite.GroupSingle()
ball_sg.add(ball)

player_g = pygame.sprite.Group()
player_g.add(player)
player_g.add(comp)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                is_game_over = False
                # start_time = int(pygame.time.get_ticks()/1000) #TODO Unused?

    if game_active:
        set_game_screen(screen)
        update_components()
        sprite_collision(ball_sg, player_g)
        if player_win != None:
            game_over(ball)
            game_active = False
            reset_components(ball, player)
    else:
        set_title_screen()

    pygame.display.update()
    clock.tick(60)