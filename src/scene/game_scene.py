from .scene import Scene
import pygame
from rectangle import Rectangle
from .scene_type import SceneType
from constants import *
from button import Button
from ball import Ball
from portal import Portal
from rectUtilities import create_rect
from paddle import Player, Computer
from game_state_manager import game_state_manager
from .scene_type import SceneType
from random import choice
import sound

class GameScene(Scene):
    def __init__(self) -> None:
        up_arrow_key_img = pygame.image.load("resources\\pixel_art\\up_arrow.png").convert_alpha()
        down_arrow_key_img = pygame.image.load("resources\\pixel_art\\down_arrow.png").convert_alpha()
        up_arrow_key_img = pygame.transform.scale_by(up_arrow_key_img, 0.08)
        down_arrow_key_img = pygame.transform.scale_by(down_arrow_key_img, 0.08)

        self.w_key = Rectangle.from_rect(SceneType.GAME_SCENE, SMALL_MSG_FONT, "W", 
                                         pygame.Rect(100, 5, 20, 20), 
                                         "black", None, None, "white")
        self.s_key = Rectangle.from_rect(SceneType.GAME_SCENE, SMALL_MSG_FONT, "S", 
                                         pygame.Rect(self.w_key.rect.left, self.w_key.rect.bottom + 1, self.w_key.rect.width, self.w_key.rect.height), 
                                         "black", None, None, "white")
        self.up_arrow_key = Rectangle.from_image(SceneType.GAME_SCENE, up_arrow_key_img, 
                                                 pygame.Rect(SCREEN_WIDTH - 100, self.w_key.rect.top, self.w_key.rect.width, self.w_key.rect.height))
        self.down_arrow_key = Rectangle.from_image(SceneType.GAME_SCENE, down_arrow_key_img, 
                                                   pygame.Rect(self.up_arrow_key.rect.left, self.up_arrow_key.rect.bottom + 1, self.w_key.rect.width, self.w_key.rect.height))
        self.assist_keys_display_time = None

        home_img = pygame.image.load("resources\pixel_art\home_icon.png").convert_alpha()
        home_img = pygame.transform.scale_by(home_img, 0.15)
        self.home_button = Button.from_image(SceneType.GAME_SCENE, home_img, create_rect(SCREEN_WIDTH/2, SCORE_HEIGHT/2, home_img.get_width(), home_img.get_height()), self.home_button_action)

        self._buttons = [self.home_button]

        self.ball = Ball()
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.comp = Computer(self.ball)

        self.singleplayer_players = pygame.sprite.Group()
        self.singleplayer_players.add(self.player1, self.comp)
        self.multiplayer_players = pygame.sprite.Group()
        self.multiplayer_players.add(self.player1, self.player2)

        self.balls = [self.ball]
        self.portals = pygame.sprite.Group()

    @property
    def scene_type(self):
        return SceneType.GAME_SCENE
    
    @property
    def buttons(self):
        return self._buttons
    

    def update(self):
        pass

    def render(self, screen):
        p1, p2 = self._get_players()
        self.set_game_screen(p1, p2, screen)
        #self.update_score(self.ball, p1, p1)
        #self.update_components()
        #self.sprite_collision()

    def _get_players(self):
        if game_state_manager.is_multiplayer:
            p1, p2 = self.player1, self.player2
        else:
            p1, p2 = self.player1, self.comp
        return p1, p2

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            if event.type == game_state_manager.portal_timer and game_state_manager.is_portals:
                game_state_manager.start_timer(game_state_manager.portal_timer, choice([2000, 3000, 4000, 5000]))

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event):
                        if button is self.home_button:
                            return self.home_button_action()

        if game_state_manager.game_active:
            p1, p2 = self._get_players()
            self.update_score(self.ball, p1, p2)
            self.update_components()
            self.sprite_collision()
        else:
            if game_state_manager.is_game_over:
                return SceneType.RESTART_SCENE
            else:
                return SceneType.TITLE_SCENE


    def display_control_assist(self):
        if self.assist_keys_display_time == None:
            self.assist_keys_display_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.assist_keys_display_time < 2500:
            if game_state_manager.is_multiplayer:
                self.w_key.change_outline("red", 2)
            self.up_arrow_key.change_outline("red", 2)
        else:
            if game_state_manager.is_multiplayer:
                self.w_key.change_outline("white", 2)
                self.s_key.change_outline("red", 2)
            self.up_arrow_key.change_outline(None)
            self.down_arrow_key.change_outline("red", 2)

        if game_state_manager.is_multiplayer:
            self.w_key.display(screen)
            self.s_key.display(screen)
        self.up_arrow_key.display(screen)
        self.down_arrow_key.display(screen)


    def home_button_action(self):
        self.reset_components()
        game_state_manager.game_active = False
        game_state_manager.is_game_over = False
        return SceneType.TITLE_SCENE


    def set_game_screen(self, p1, p2, screen):
        screen.fill("Black")
        pygame.draw.ellipse(screen, "White", self.ball.rect)
        p1.display(screen)
        p2.display(screen)

        for button in self._buttons:
            button.draw(screen)

        if self.assist_keys_display_time == None:
            self.assist_keys_display_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.assist_keys_display_time <= 5000: 
            self.display_control_assist()
        else:
            self.assist_keys_display_time = 0
            self.s_key.change_outline(None)
            self.down_arrow_key.change_outline(None)

        if game_state_manager.is_portals:
            for portal in self.portals:
                if portal.rect1 != None:
                    pygame.draw.rect(screen, portal.color, portal.rect1)
                if portal.rect2 != None:
                    pygame.draw.rect(screen, portal.color, portal.rect2)  
                if game_state_manager.play_sound_fx and portal.is_consumed:
                    for rect in portal.sprinkles:
                        pygame.draw.rect(screen, portal.color, rect)
        
        pygame.draw.line(screen, "white", (SCREEN_WIDTH/2, SCORE_HEIGHT), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
        pygame.draw.line(screen, "white", (0,SCORE_HEIGHT), (SCREEN_WIDTH,SCORE_HEIGHT), 2)


    def sprite_collision(self):
        players = self.multiplayer_players if game_state_manager.is_multiplayer else self.singleplayer_players

        for ball in self.balls:
            for player in players:
                if not ball.reflections_disabled and player.rect.colliderect(ball.rect):
                    ball.velocity.x *= -1
                    self.play_sound_fx(sound.paddle_hit_fx, 1000)
                    ball.disable_reflections()

            if not game_state_manager.is_portals:
                continue

            for portal in self.portals:
                if portal.is_consumed():
                    continue
                if portal.is_hit(ball):
                    portal.hit(ball, pygame.time.get_ticks())
                    self.play_sound_fx(sound.portal_fx)


    def update_score(self, ball, p1, p2):
        p1_score_msg = MSG_FONT.render(str(p1.score), False, "blue" if game_state_manager.is_multiplayer else "red")
        screen.blit(p1_score_msg, p1_score_msg.get_rect(center = (25, SCORE_HEIGHT/2)))
        p2_score_msg = MSG_FONT.render(str(p2.score), False, "green")
        screen.blit(p2_score_msg, p2_score_msg.get_rect(center = (SCREEN_WIDTH-25, SCORE_HEIGHT/2)))
        
        if ball.rect.x >= SCREEN_WIDTH:
            p1.score += 1
            self.play_sound_fx(sound.goal_fx)
        elif ball.rect.x <= 0:
            p2.score += 1
            self.play_sound_fx(sound.goal_fx)
        else:
            if not ball.in_cooldown: return

        if ball.in_cooldown and pygame.time.get_ticks() - ball.start_cooldown_time >= BALL_RESET_COOLDOWN: 
            ball.reset()

        if not ball.in_cooldown:
            ball.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            ball.velocity = pygame.math.Vector2(0,0)
            ball.start_cooldown_time = pygame.time.get_ticks()
            ball.in_cooldown = True
            return self.check_game_over(p1, p2) 

    def check_game_over(self, comp, player):
        if comp.score < game_state_manager.score_to_win and player.score < game_state_manager.score_to_win:
            return False
        
        game_state_manager.p1_win = player.score == game_state_manager.score_to_win
        self.reset_components()
        return SceneType.RESTART_SCENE


    def update_components(self):
        for ball in self.balls:
            ball.update()
        
        if game_state_manager.is_multiplayer:
            for player in self.multiplayer_players:
                player.update()
        else:
            for player in self.singleplayer_players:
                player.update()

        if game_state_manager.is_portals:        
            for portal in self.portals:
                portal.update(pygame.time.get_ticks())


    def reset_components(self):
        self._reset_balls()
        self._reset_players()
        self.portals.empty()
        game_state_manager.set_default_settings()

    def _reset_balls(self):
        for ball in self.balls:
            ball.reset()

    def _reset_players(self):
        for player in self.singleplayer_players:
            player.reset()
        
        for player in self.multiplayer_players:
            player.reset()
    

    def play_sound_fx(self, fx, stop_at=None):
        if not game_state_manager.play_sound_fx:
            return
        if stop_at == None:
            fx.play(0)
        else:
            fx.play(0, stop_at)