import pygame, Ball, Paddle, Portal
from Constants import *
from sys import exit
from random import randint, choice

def set_title_screen():
    screen.blit(title, title_rect)
    screen.blit(title_msg, title_msg_rect)
    # screen.blit(classic_mode_msg, classic_mode_rect)
    

def set_game_screen(p1, p2):
    screen.fill("Black")
    pygame.draw.ellipse(screen, "White", ball.rect)
    screen.blit(p1.surf, p1.rect)
    screen.blit(p2.surf, p2.rect)
    for portal in Portal.portals_g:
        if portal.rect1 != None:
            pygame.draw.rect(screen, portal.color, portal.rect1)
        if portal.rect2 != None:
            pygame.draw.rect(screen, portal.color, portal.rect2)  
    pygame.draw.line(screen, "White", (SCREEN_WIDTH/2, SCORE_HEIGHT), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    pygame.draw.line(screen, "White", (0,SCORE_HEIGHT), (SCREEN_WIDTH,SCORE_HEIGHT), 2)

def sprite_collision(ball_group, player_group, portal_group):
    for ball in ball_group:
        for player in player_group:
            if player.rect.colliderect(ball.rect):
                ball.velocity.x *= -1
                paddle_hit_fx.play(0,1000)
        for portal in portal_group:
            if portal.rect1 == None or portal.rect2 == None:
                continue
            if ball.rect.colliderect(portal.rect1):
                ball.rect.x = portal.rect2.x
                ball.rect.y = portal.rect2.y
                portal.rect1 = None
                portal.duration = 2000
                portal_fx.play()
            elif ball.rect.colliderect(portal.rect2):
                ball.rect.x = portal.rect1.x
                ball.rect.y = portal.rect1.y 
                portal.rect2 = None
                portal.duration = 2000
                portal_fx.play()

def update_score(ball, comp, player):
    # print(f"Current time: {pygame.time.get_ticks()}")
    comp_score_msg = msg_font.render(str(comp.score), False, "Red")
    screen.blit(comp_score_msg, comp_score_msg.get_rect(center = (25, SCORE_HEIGHT/2)))
    player_score_msg = msg_font.render(str(player.score), False, "Green")
    screen.blit(player_score_msg, player_score_msg.get_rect(center = (SCREEN_WIDTH-25, SCORE_HEIGHT/2)))
    
    if ball.rect.x >= SCREEN_WIDTH:
        comp.score += 1
        goal_fx.play(0)
    elif ball.rect.x <= 0:
        player.score += 1
        goal_fx.play(0)
    else:
        if not ball.in_cooldown: return

    if not ball.in_cooldown:
        ball.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        ball.velocity = pygame.math.Vector2(0,0)
        ball.start_cooldown_time = pygame.time.get_ticks()
        ball.in_cooldown = True

        #print(f"time:{pygame.time.get_ticks()}, ball: {ball.start_cooldown_time}") 
        check_game_over(comp, player) 

    if ball.in_cooldown and pygame.time.get_ticks() - ball.start_cooldown_time >= BALL_RESET_COOLDOWN: 
        ball.reset()

def check_game_over(comp, player):
    #print(f"comp_score={comp.score}, player_score={player.score}")
    if comp.score == score_to_win: 
        game_over(False)
    elif player.score == score_to_win:
        game_over(True)

def game_over(player_win):
    screen.fill("Black")
    set_title_screen()
    if player_win: screen.blit(win_msg, win_msg_rect)
    else: screen.blit(loss_msg, loss_msg_rect)
    
    reset_components(Ball.ball_sg, Paddle.player_g, Portal.portals_g)

def update_components(ball_g, player_g, portals_g):
    global player_win
    for ball in ball_g:
        ball.update()
    for player in player_g:
        player.update()
    for portal in portals_g:
        portal.update(pygame.time.get_ticks())

def reset_components(ball_g, player_g, portals_g):
    global player_win, game_active
    for ball in ball_g:
        ball.reset()
    for player in player_g:
        player.reset()
    portals_g.empty()
    player_win = None
    game_active = False

def is_mouse_in_rect(rect, mouse_x, mouse_y):
    return rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

title_font = pygame.font.Font(FONT, 80)
msg_font = pygame.font.Font(FONT, 50)

game_active = False
is_multiplayer = None
is_online = False
is_portals = False
start_time = 0

# Title screen
title = title_font.render("Pong", False, "White")
title_rect = title.get_rect(center = (SCREEN_WIDTH/2,80))

title_msg = msg_font.render("Press Space to start", False, "white")
title_msg_rect = title_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-100))

loss_msg = msg_font.render("YOU LOSE", False, "red")
loss_msg_rect = loss_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

win_msg = msg_font.render("YOU WIN", False, "green")
win_msg_rect = win_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

classic_mode_msg = msg_font.render("Classic", False, "white")
classic_mode_rect = classic_mode_msg.get_rect(midleft = (SCREEN_WIDTH/4, SCREEN_HEIGHT-200))
classic_mode_button = pygame.Rect(SCREEN_WIDTH/4, SCREEN_HEIGHT-225, 150, 50)

portals_mode_msg = msg_font.render("Portals", False, "white")
portals_mode_rect = portals_mode_msg.get_rect(midleft = (SCREEN_WIDTH/2, SCREEN_HEIGHT-200))
portals_mode_button = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT-225, 150, 50)

buttons = [classic_mode_button, portals_mode_button]
button_msgs = [classic_mode_msg, portals_mode_msg]

# Game
ball = Ball.Ball()
player1 = Paddle.Player(1)
player2 = Paddle.Player(2)
comp = Paddle.Computer(ball)
score_to_win = 3 #TODO Let the user choose this.

# Sound FX
bg_music = pygame.mixer.Sound("resources/audio/bg_music.mp3")
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

goal_fx = pygame.mixer.Sound("resources/audio/goal.wav")
paddle_hit_fx = pygame.mixer.Sound("resources/audio/paddle_hit.wav")
portal_fx = pygame.mixer.Sound("resources/audio/portal.wav")
# Timers 
portal_timer = pygame.USEREVENT + 1
pygame.time.set_timer(portal_timer, 5000)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button, msg in zip(buttons, button_msgs):
                game_active = True
                if msg == "Portals":
                    is_portals = True
                else:
                    is_portals = False

        if is_portals and event.type == portal_timer:
            portal = Portal.Portal(pygame.time.get_ticks())

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                is_game_over = False   

    if game_active:
        if is_multiplayer:
            set_game_screen(player1, player2)
        else:
            set_game_screen(player1, comp)
        update_components(Ball.ball_sg, Paddle.player_g, Portal.portals_g)
        sprite_collision(Ball.ball_sg, Paddle.player_g, Portal.portals_g)
        update_score(ball, comp, player1)
    else:
        set_title_screen()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button, msg in zip(buttons, button_msgs):
            if is_mouse_in_rect(button, mouse_x, mouse_y):
                pygame.draw.rect(screen, "grey", button)
            else:
                pygame.draw.rect(screen, "black", button)
                pygame.draw.rect(screen, "White", button, 1)
            screen.blit(msg, button)

    pygame.display.update()
    clock.tick(60)

