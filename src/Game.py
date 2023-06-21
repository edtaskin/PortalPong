import pygame
import Ball, Paddle, Portal, Button
from Constants import *
from sys import exit
from random import randint, choice

def set_title_screen():
    screen.fill("Black")
    screen.blit(title, title_rect)
    screen.blit(title_msg, title_msg_rect)
    screen.blit(game_mode_msg, game_mode_msg_rect)
    screen.blit(player_count_msg, player_count_msg_rect)
    screen.blit(score_to_win_msg, score_to_win_msg_rect)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for button in Button.buttons:
        if is_mouse_in_rect(button.button_rect, mouse_x, mouse_y) or button.is_pressed:
            pygame.draw.rect(screen, "#4B0082", button.button_rect)
        else:
            pygame.draw.rect(screen, "white", button.button_rect, 1)
        screen.blit(button.msg_text, button.button_rect)
  
def set_restart_screen():
    screen.fill("Black")
    screen.blit(title, title_rect)
    screen.blit(title_msg, title_msg_rect)
    if p1_win: screen.blit(win_msg, win_msg_rect)
    else: screen.blit(loss_msg, loss_msg_rect)

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
            if not ball.reflections_disabled and player.rect.colliderect(ball.rect):
                ball.velocity.x *= -1
                paddle_hit_fx.play(0,1000)
                ball.disable_reflections()
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

def update_score(ball, p1, p2):
    p1_score_msg = MSG_FONT.render(str(p1.score), False, "Red")
    screen.blit(p1_score_msg, p1_score_msg.get_rect(center = (25, SCORE_HEIGHT/2)))
    p2_score_msg = MSG_FONT.render(str(p2.score), False, "Green")
    screen.blit(p2_score_msg, p2_score_msg.get_rect(center = (SCREEN_WIDTH-25, SCORE_HEIGHT/2)))
    
    if ball.rect.x >= SCREEN_WIDTH:
        p1.score += 1
        goal_fx.play(0)
    elif ball.rect.x <= 0:
        p2.score += 1
        goal_fx.play(0)
    else:
        if not ball.in_cooldown: return

    if not ball.in_cooldown:
        ball.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        ball.velocity = pygame.math.Vector2(0,0)
        ball.start_cooldown_time = pygame.time.get_ticks()
        ball.in_cooldown = True
        check_game_over(p1, p2) 

    if ball.in_cooldown and pygame.time.get_ticks() - ball.start_cooldown_time >= BALL_RESET_COOLDOWN: 
        ball.reset()

def check_game_over(comp, player):
    global p1_win
    if comp.score == score_to_win: 
        p1_win = False
        game_over()
    elif player.score == score_to_win:
        p1_win = True
        game_over()

def game_over():
    global is_game_over
    is_game_over = True
    set_restart_screen()
    reset_components(Ball.ball_sg, Paddle.player_g, Portal.portals_g)

def update_components(ball_g, player_g, portals_g):
    for ball in ball_g:
        ball.update()
    for player in player_g:
        player.update()
    for portal in portals_g:
        portal.update(pygame.time.get_ticks())

def reset_components(ball_g, player_g, portals_g):
    global game_active
    for ball in ball_g:
        ball.reset()
    for player in player_g:
        player.reset()
    portals_g.empty()
    #player_win = None
    game_active = False
    reset_all_buttons()

def reset_all_buttons():
    for button in Button.buttons:
        button.is_pressed = False

def reset_group_of_buttons(buttons):
    for button in buttons:
        button.is_pressed = False

def is_mouse_in_rect(rect, mouse_x, mouse_y):
    return rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

TITLE_FONT = pygame.font.Font(FONT, 80)
MSG_FONT = pygame.font.Font(FONT, 50)
SMALL_MSG_FONT = pygame.font.Font(FONT, 30)

game_active = False
is_game_over = False
is_multiplayer = None
is_online = False
is_portals = False
game_mode_selected = False
player_count_selected = False
p1_win = False

# Title screen
title = TITLE_FONT.render("Pong", False, "White")
title_rect = title.get_rect(center = (SCREEN_WIDTH/2,80))

title_msg = MSG_FONT.render("Select a game mode", False, "white")
title_msg_rect = title_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50))

loss_msg = MSG_FONT.render("YOU LOSE", False, "red")
loss_msg_rect = loss_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

win_msg = MSG_FONT.render("YOU WIN", False, "green")
win_msg_rect = win_msg.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

game_mode_msg = SMALL_MSG_FONT.render("Game mode:", False, "white")
game_mode_msg_rect = game_mode_msg.get_rect(center = (title_msg_rect.left - 100, SCREEN_HEIGHT/2 - 75))
classic_mode_button = Button.Button("Classic", MSG_FONT, title_msg_rect.left, game_mode_msg_rect.centery - 25, 150, 50)
portals_mode_button = Button.Button("Portals", MSG_FONT, title_msg_rect.right - 150, game_mode_msg_rect.centery - 25, 150, 50)
game_mode_buttons = [classic_mode_button, portals_mode_button]

player_count_msg = SMALL_MSG_FONT.render("Player count:", False, "white")
player_count_msg_rect = player_count_msg.get_rect(midright = (classic_mode_button.button_rect.left, SCREEN_HEIGHT/2 + 25))
singleplayer_button = Button.Button("1P", MSG_FONT, classic_mode_button.button_rect.centerx, player_count_msg_rect.centery -25, 50, 50)
singleplayer_button.is_pressed = True
multiplayer_button = Button.Button("2P", MSG_FONT, portals_mode_button.button_rect.centerx, player_count_msg_rect.centery - 25, 50, 50)
player_count_buttons = [singleplayer_button, multiplayer_button]

score_to_win_msg = SMALL_MSG_FONT.render("Score to win:", False, "white")
score_to_win_msg_rect = score_to_win_msg.get_rect(midright = (classic_mode_button.button_rect.left, 3*SCREEN_HEIGHT/4))
score_to_win_buttons = []
score_to_win_buttons.append(Button.Button("3", MSG_FONT, classic_mode_button.button_rect.centerx, score_to_win_msg_rect.centery - 25, 50, 50))
score_to_win_buttons.append(Button.Button("7", MSG_FONT, SCREEN_WIDTH/2, score_to_win_msg_rect.centery - 25, 50, 50))
score_to_win_buttons.append(Button.Button("11", MSG_FONT, portals_mode_button.button_rect.centerx, score_to_win_msg_rect.centery - 25, 50, 50))
score_to_win_buttons[0].is_pressed = True

# Game
ball = Ball.Ball()
player1 = Paddle.Player(1)
player2 = Paddle.Player(2)
comp = Paddle.Computer(ball)
score_to_win = 3 

# Sound FX
bg_music = pygame.mixer.Sound("resources/audio/bg_music.mp3")
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

goal_fx = pygame.mixer.Sound("resources/audio/goal.wav")
paddle_hit_fx = pygame.mixer.Sound("resources/audio/paddle_hit.wav")
portal_fx = pygame.mixer.Sound("resources/audio/portal.wav")

# Timers 
portal_timer = pygame.USEREVENT + 1

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in Button.buttons:
                if button.button_rect.collidepoint(event.pos):
                    if button in game_mode_buttons:
                        reset_group_of_buttons(game_mode_buttons)
                        game_mode_selected = True
                        title_msg = MSG_FONT.render("Press Space to start", False, "white")
                        is_portals = button is portals_mode_button
                        if is_portals:
                            pygame.time.set_timer(portal_timer, 5000)
                    elif button in player_count_buttons:
                        reset_group_of_buttons(player_count_buttons)
                        is_multiplayer = button is multiplayer_button
                    else:
                        reset_group_of_buttons(score_to_win_buttons)
                        score_to_win = int(button.msg)
                    button.is_pressed = True
        
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_mode_selected:
                    game_active = True
                else:
                    title_msg = MSG_FONT.render("Select a game mode", False, "red")
                        

        if is_portals and event.type == portal_timer:
            portal = Portal.Portal(pygame.time.get_ticks())

    if game_active:
        if is_multiplayer:
            set_game_screen(player1, player2)
            update_score(ball, player1, player2)
        else:
            set_game_screen(player1, comp)
            update_score(ball, comp, player1)
        update_components(Ball.ball_sg, Paddle.player_g, Portal.portals_g)
        sprite_collision(Ball.ball_sg, Paddle.player_g, Portal.portals_g)
        
    else:
        if is_game_over:
            set_restart_screen()
        else:
            set_title_screen()
            
    pygame.display.update()
    clock.tick(60)

