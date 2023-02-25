import pygame, Ball, Paddle, Portal
from Constants import *
from sys import exit
from random import randint, choice

def set_title_screen():
    screen.blit(title, title_rect)
    screen.blit(title_msg, title_msg_rect)

def set_game_screen(screen):
    screen.fill("Black")
    pygame.draw.ellipse(screen, "White", ball.rect)
    screen.blit(player.surf, player.rect)
    screen.blit(comp.surf, comp.rect)
    pygame.draw.aaline(screen, "Grey", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))

def sprite_collision(ball_group, player_group):
    for ball in ball_group:
        for player in player_group:
            if player.rect.colliderect(ball.rect):
                ball.velocity.x *= -1

def check_game_over(ball):
    global player_win
    if ball.rect.x > SCREEN_WIDTH:
        player_win = False
        game_over()
    elif ball.rect.x < 0:
        player_win = True
        game_over()

def game_over():
    print("HERE")
    screen.fill("Black")
    set_title_screen()
    if ball.rect.right >= SCREEN_WIDTH:
        screen.blit(loss_msg, loss_msg_rect)
    else:
        screen.blit(win_msg, win_msg_rect)
    reset_components(ball_sg, player_g)

def update_components(ball_g, player_g):
    global player_win
    for ball in ball_g:
        ball.update(player_win)
    for player in player_g:
        player.update()

def reset_components(ball_g, player_g):
    global player_win, game_active
    for ball in ball_g:
        ball.reset()
    for player in player_g:
        player.reset()
    player_win = None
    game_active = False


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

title_font = pygame.font.Font("font\VT323-Regular.ttf", 80)
msg_font = pygame.font.Font("font\VT323-Regular.ttf", 50)

game_active = False
player_win = None
start_time = 0

# Title screen
title = title_font.render("Pong", False, "White")
title_rect = title.get_rect(center = (SCREEN_WIDTH/2,80))

title_msg = msg_font.render("Press Space to start", False, "White")
title_msg_rect = title_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-100))

loss_msg = msg_font.render("YOU LOSE", False, "Red")
loss_msg_rect = loss_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

win_msg = msg_font.render("YOU WIN", False, "Green")
win_msg_rect = win_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))


# Game
ball = Ball.Ball()
player = Paddle.Player()
comp = Paddle.Computer(ball)

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
                # start_time = int(pygame.time.get_ticks()/1000) #TODO

    if game_active:
        set_game_screen(screen)
        update_components(ball_sg, player_g)
        sprite_collision(ball_sg, player_g)
        check_game_over(ball)
    else:
        set_title_screen()

    pygame.display.update()
    clock.tick(60)