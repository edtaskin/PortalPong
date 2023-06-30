import pygame
from ball import Ball 
from paddle import Paddle, Player, Computer 
from portal import Portal 
from button import Button
from rectangle import Rectangle
from constants import *
from sys import exit
from random import randint, choice

def set_title_screen():
    screen.fill("Black")
    for rect in Rectangle.title_screen_rectangles:
        rect.display(screen)
    for button in Button.title_screen_buttons:
        button.display(screen)
  
def set_restart_screen():
    screen.fill("Black")
    title.display(screen)
    title_msg.display(screen)
    for button in Button.restart_screen_buttons :
        button.display(screen)
    if p1_win:  win_msg.display(screen)
    else:       loss_msg.display(screen)

def set_game_screen(p1, p2):
    global assist_keys_display_time
    screen.fill("Black")
    pygame.draw.ellipse(screen, "White", ball.rect)
    p1.display(screen)
    p2.display(screen)

    for button in Button.game_screen_buttons:
        button.display(screen)

    if assist_keys_display_time == None:
        assist_keys_display_time = pygame.time.get_ticks()

    if pygame.time.get_ticks() - assist_keys_display_time <= 5000: 
        display_control_assist()
    else:
        assist_keys_display_time = 0
        s_key.change_outline(None)
        down_arrow_key.change_outline(None)

    if is_portals:
        for portal in Portal.portals_g:
            if portal.rect1 != None:
                pygame.draw.rect(screen, portal.color, portal.rect1)
            if portal.rect2 != None:
                pygame.draw.rect(screen, portal.color, portal.rect2)  
    
    pygame.draw.line(screen, "white", (SCREEN_WIDTH/2, SCORE_HEIGHT), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    pygame.draw.line(screen, "white", (0,SCORE_HEIGHT), (SCREEN_WIDTH,SCORE_HEIGHT), 2)

def sprite_collision(ball_group, player_group, portal_group):
    for ball in ball_group:
        for player in player_group:
            if not ball.reflections_disabled and player.rect.colliderect(ball.rect):
                ball.velocity.x *= -1
                play_sound_fx(paddle_hit_fx, 1000)
                ball.disable_reflections()
        if is_portals:
            for portal in portal_group:
                if portal.rect1 == None or portal.rect2 == None:
                    continue
                if ball.rect.colliderect(portal.rect1):
                    ball.rect.x = portal.rect2.x
                    ball.rect.y = portal.rect2.y
                    portal.rect1 = None
                    portal.duration = 2000
                    play_sound_fx(portal_fx)
                elif ball.rect.colliderect(portal.rect2):
                    ball.rect.x = portal.rect1.x
                    ball.rect.y = portal.rect1.y 
                    portal.rect2 = None
                    portal.duration = 2000
                    play_sound_fx(portal_fx)

def update_score(ball, p1, p2):
    p1_score_msg = MSG_FONT.render(str(p1.score), False, "blue" if is_multiplayer else "red")
    screen.blit(p1_score_msg, p1_score_msg.get_rect(center = (25, SCORE_HEIGHT/2)))
    p2_score_msg = MSG_FONT.render(str(p2.score), False, "green")
    screen.blit(p2_score_msg, p2_score_msg.get_rect(center = (SCREEN_WIDTH-25, SCORE_HEIGHT/2)))
    
    if ball.rect.x >= SCREEN_WIDTH:
        p1.score += 1
        play_sound_fx(goal_fx)
    elif ball.rect.x <= 0:
        p2.score += 1
        play_sound_fx(goal_fx)
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
    reset_components()
    set_restart_screen()

def update_components(ball_g, player_g, portals_g):
    for ball in ball_g:
        ball.update()
    for player in player_g:
        player.update()
    for portal in portals_g:
        portal.update(pygame.time.get_ticks())

def reset_components():
    global game_active, player_win, is_game_over, game_mode_selected, is_multiplayer, score_to_win, is_portals, assist_keys_display_time
    player_g = multiplayer_g if is_multiplayer else singleplayer_g
    for ball in Ball.ball_sg:
        ball.reset()
    for player in player_g:
        player.reset()
    Portal.portals_g.empty()
    player_win = None
    game_active = False
    is_game_over = True
    game_mode_selected = False
    is_multiplayer = False # Revert back to default options
    score_to_win = 3
    is_portals = False
    assist_keys_display_time = None

def reset_group_of_buttons(buttons):
    for button in buttons:
        button.release()
    if buttons == title_screen_buttons:
        singleplayer_button.press()    # Default options
        score_to_win_buttons[0].press()
        back_button.release()

# TODO Can it be used anywhere else?
def create_rect(centerx, centery, width, height):
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (centerx, centery)
    return rect

def play_sound_fx(fx, stop_at=None):
    if play_fx:
        if stop_at == None:
            fx.play(0)
        else:
            fx.play(0, stop_at)

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
current_screen = TITLE_SCREEN
play_music = True
play_fx = True

# Title screen
title = Rectangle.from_text(TITLE_SCREEN, TITLE_FONT, "Pong", SCREEN_WIDTH/2,80)
title_msg = Rectangle.from_text(TITLE_SCREEN, MSG_FONT, "Select a game mode", SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
loss_msg = Rectangle.from_text(RESTART_SCREEN, MSG_FONT, "YOU LOSE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "red")
win_msg = Rectangle.from_text(RESTART_SCREEN, MSG_FONT, "YOU WIN", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "green")

def game_mode_button_action():
    global game_mode_selected, title_msg
    reset_group_of_buttons(game_mode_buttons)
    game_mode_selected = True
    title_msg.change_text(MSG_FONT, "Press Space to start")
    
def classic_mode_button_action():
    global is_portals
    game_mode_button_action()
    is_portals = False

def portals_mode_button_action():
    global is_portals
    game_mode_button_action()
    is_portals = True
    pygame.time.set_timer(portal_timer, 5000)

game_mode_msg = Rectangle.from_text(TITLE_SCREEN, SMALL_MSG_FONT, "Game mode:", title_msg.rect.left - 100, SCREEN_HEIGHT/2 - 75)

classic_mode_button = Button.from_text(TITLE_SCREEN, "Classic", MSG_FONT, pygame.Rect(title_msg.rect.left, game_mode_msg.rect.centery - 25, 150, 50), classic_mode_button_action)
portals_mode_button = Button.from_text(TITLE_SCREEN, "Portals", MSG_FONT, pygame.Rect(title_msg.rect.right - 150, game_mode_msg.rect.centery - 25, 150, 50), portals_mode_button_action)
game_mode_buttons = [classic_mode_button, portals_mode_button]

def player_count_button_action():
    global is_multiplayer
    reset_group_of_buttons(player_count_buttons)
    is_multiplayer = button is multiplayer_button

player_count_msg = Rectangle.from_text(TITLE_SCREEN, SMALL_MSG_FONT, "Player count:", game_mode_msg.rect.centerx, SCREEN_HEIGHT/2 + 25)

singleplayer_button = Button.from_text(TITLE_SCREEN, "1P", MSG_FONT, pygame.Rect(classic_mode_button.rect.centerx, player_count_msg.rect.centery -25, 50, 50), player_count_button_action)
singleplayer_button.press() 
multiplayer_button = Button.from_text(TITLE_SCREEN, "2P", MSG_FONT, pygame.Rect(portals_mode_button.rect.centerx, player_count_msg.rect.centery - 25, 50, 50), player_count_button_action)
player_count_buttons = [singleplayer_button, multiplayer_button]

def score_to_win_button_action(score):
    global score_to_win
    reset_group_of_buttons(score_to_win_buttons)
    score_to_win = score

score_to_win_msg = Rectangle.from_text(TITLE_SCREEN, SMALL_MSG_FONT, "Score to win:", game_mode_msg.rect.centerx, 3*SCREEN_HEIGHT/4)

score_to_win_buttons = []
score_to_win_buttons.append(Button.from_text(TITLE_SCREEN, "3", MSG_FONT, pygame.Rect(classic_mode_button.rect.centerx, score_to_win_msg.rect.centery - 25, 50, 50), lambda: score_to_win_button_action(3)))
score_to_win_buttons.append(Button.from_text(TITLE_SCREEN, "7", MSG_FONT, pygame.Rect(SCREEN_WIDTH/2, score_to_win_msg.rect.centery - 25, 50, 50), lambda: score_to_win_button_action(7)))
score_to_win_buttons.append(Button.from_text(TITLE_SCREEN, "11", MSG_FONT, pygame.Rect(portals_mode_button.rect.centerx, score_to_win_msg.rect.centery - 25, 50, 50), lambda: score_to_win_button_action(11)))
score_to_win_buttons[0].press()

title_screen_buttons = game_mode_buttons + player_count_buttons + score_to_win_buttons

def settings_button_action():
    music_button.set_visibility(not music_button.is_visible)
    sound_fx_button.set_visibility(not sound_fx_button.is_visible)
    if music_button.is_visible:
        settings_rect.set_visibility(True)
    settings_button.release()

def music_button_action():
    global play_music
    play_music = not play_music
    if play_music:
        bg_music.play(loops=-1)
        music_button.release()
    else:
        bg_music.stop()

def sound_fx_button_action():
    global play_fx
    play_fx = not play_fx
    if play_fx:
        sound_fx_button.release()

settings_icon = pygame.image.load("resources\\pixel_art\\settings_icon.png").convert_alpha()
settings_icon = pygame.transform.scale_by(settings_icon, 1/5)
settings_button = Button.from_image(TITLE_SCREEN, settings_icon, pygame.Rect(SCREEN_WIDTH-100, 25, settings_icon.get_width(), settings_icon.get_height()), settings_button_action)

music_icon = pygame.image.load("resources\\pixel_art\\music_icon.png").convert_alpha()
music_icon = pygame.transform.scale_by(music_icon, 1/6)
music_button = Button.from_image(TITLE_SCREEN, music_icon, create_rect(settings_button.rect.centerx, settings_button.rect.centery + 70, music_icon.get_width(), music_icon.get_height()), music_button_action)
music_button.set_visibility(False)

sound_fx_button = Button.from_text(TITLE_SCREEN, "Fx", MSG_FONT, create_rect(settings_button.rect.centerx, music_button.rect.centery + 70, music_icon.get_width(), music_icon.get_height()), sound_fx_button_action)
sound_fx_button.set_visibility(False)

settings_rect = Rectangle(TITLE_SCREEN, None, create_rect(settings_button.rect.centerx, (music_button.rect.centerx + sound_fx_button.rect.centerx)/2, settings_button.rect.width, music_button.rect.height + sound_fx_button.rect.height + 10), None, None, "red")
settings_rect.set_visibility(False)
# Restart Screen
def back_button_action():
    global game_active, is_game_over
    game_active = False
    is_game_over = False
    reset_group_of_buttons(title_screen_buttons)
    back_button.release()

back_button = Button.from_text(RESTART_SCREEN, "<-BACK", SMALL_MSG_FONT, pygame.Rect(50, 50, 80, 30), back_button_action)

# Game Screen
up_arrow_key_img = pygame.image.load("resources\\pixel_art\\up_arrow.png").convert_alpha()
down_arrow_key_img = pygame.image.load("resources\\pixel_art\\down_arrow.png").convert_alpha()
up_arrow_key_img = pygame.transform.scale_by(up_arrow_key_img, 0.08)
down_arrow_key_img = pygame.transform.scale_by(down_arrow_key_img, 0.08)

w_key = Rectangle.from_rect(GAME_SCREEN, SMALL_MSG_FONT, "W", pygame.Rect(100, 5, 20, 20), "black", None, None, "white")
s_key = Rectangle.from_rect(GAME_SCREEN, SMALL_MSG_FONT, "S", pygame.Rect(w_key.rect.left, w_key.rect.bottom + 1, w_key.rect.width, w_key.rect.height), "black", None, None, "white")
up_arrow_key = Rectangle.from_image(GAME_SCREEN, up_arrow_key_img, pygame.Rect(SCREEN_WIDTH - 100, w_key.rect.top, w_key.rect.width, w_key.rect.height))
down_arrow_key = Rectangle.from_image(GAME_SCREEN, down_arrow_key_img, pygame.Rect(up_arrow_key.rect.left, up_arrow_key.rect.bottom + 1, w_key.rect.width, w_key.rect.height))
assist_keys_display_time = None

def display_control_assist():
    global assist_keys_display_time
    if assist_keys_display_time == None:
        assist_keys_display_time = pygame.time.get_ticks()
    if pygame.time.get_ticks() - assist_keys_display_time < 2500:
        if is_multiplayer:
            w_key.change_outline("red", 2)
        up_arrow_key.change_outline("red", 2)
    else:
        if is_multiplayer:
            w_key.change_outline("white", 2)
            s_key.change_outline("red", 2)
        up_arrow_key.change_outline(None)
        down_arrow_key.change_outline("red", 2)

    if is_multiplayer:
        w_key.display(screen)
        s_key.display(screen)
    up_arrow_key.display(screen)
    down_arrow_key.display(screen)

home_img = pygame.image.load("resources\pixel_art\home_icon.png").convert_alpha()
home_img = pygame.transform.scale_by(home_img, 0.15)

def home_button_action():
    global game_active, is_game_over
    reset_components()
    game_active = False
    is_game_over = False
    reset_group_of_buttons(title_screen_buttons)

home_button = Button.from_image(GAME_SCREEN, home_img, create_rect(SCREEN_WIDTH/2, SCORE_HEIGHT/2, home_img.get_width(), home_img.get_height()), home_button_action)

# Game
ball = Ball()
player1 = Player(1)
player2 = Player(2)
comp = Computer(ball)
score_to_win = 3 

singleplayer_g = pygame.sprite.Group()
singleplayer_g.add(player1, comp)
multiplayer_g = pygame.sprite.Group()
multiplayer_g.add(player1, player2)

# Sound FX
bg_music = pygame.mixer.Sound("resources/audio/bg_music.mp3")
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

goal_fx = pygame.mixer.Sound("resources/audio/goal.wav")
paddle_hit_fx = pygame.mixer.Sound("resources/audio/paddle_hit.wav")
portal_fx = pygame.mixer.Sound("resources/audio/portal.wav")
sound_fx = [goal_fx, paddle_hit_fx, portal_fx]

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
                if button.rect.collidepoint(event.pos):
                    button.action()
                    if button is not settings_button or button is not home_button:
                        button.press()
                    if button is music_button:
                        if play_music:
                            button.release()
                    elif button is sound_fx_button:
                        if play_fx:
                            button.release()

        if is_portals and event.type == portal_timer:
            portal = Portal(pygame.time.get_ticks())
            pygame.time.set_timer(portal_timer, choice([2000, 3000, 4000, 5000, 6000, 7000]))
        
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_mode_selected:
                    game_active = True
                    if is_multiplayer:
                        win_msg.change_text(MSG_FONT, "P1 WIN", "green")
                        loss_msg.change_text(MSG_FONT, "P2 WIN", "blue")
                    else:
                        win_msg.change_text(MSG_FONT, "YOU WIN", "green")
                        loss_msg.change_text(MSG_FONT, "YOU LOSE", "red")
                else:
                    title_msg.change_text(MSG_FONT, "Select a game mode", "red")                        
    if game_active:
        current_screen = GAME_SCREEN
        if is_multiplayer:
            set_game_screen(player1, player2)
            update_score(ball, player1, player2)
            update_components(ball.ball_sg, multiplayer_g, Portal.portals_g)
            sprite_collision(ball.ball_sg, multiplayer_g, Portal.portals_g)
        else:
            set_game_screen(player1, comp)
            update_score(ball, comp, player1)
            update_components(ball.ball_sg, singleplayer_g, Portal.portals_g)
            sprite_collision(ball.ball_sg, singleplayer_g, Portal.portals_g)
    else:
        if is_game_over:
            current_screen = RESTART_SCREEN
            set_restart_screen()
        else:
            current_screen = TITLE_SCREEN
            set_title_screen()
            
    pygame.display.update()
    clock.tick(60)