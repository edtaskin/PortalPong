from constants import *
from rectangle import Rectangle
from .scene_type import SceneType
from .scene import Scene
from button import Button
from game_state_manager import game_state_manager
from rectUtilities import create_rect
import sound

class TitleScene(Scene):
    def __init__(self):
        self.title = Rectangle.from_text(SceneType.TITLE_SCENE, TITLE_FONT, "Pong", SCREEN_WIDTH/2,80)
        self.title_msg = Rectangle.from_text(SceneType.TITLE_SCENE, MSG_FONT, "Select a game mode", SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
        self.game_mode_msg = Rectangle.from_text(SceneType.TITLE_SCENE, SMALL_MSG_FONT, "Game mode:", self.title_msg.rect.left - 100, SCREEN_HEIGHT/2 - 75)

        self.classic_mode_button = Button.from_text(SceneType.TITLE_SCENE, "Classic", MSG_FONT, pygame.Rect(self.title_msg.rect.left, self.game_mode_msg.rect.centery - 25, 150, 50), self.classic_mode_button_action)
        self.portals_mode_button = Button.from_text(SceneType.TITLE_SCENE, "Portals", MSG_FONT, pygame.Rect(self.title_msg.rect.right - 150, self.game_mode_msg.rect.centery - 25, 150, 50), self.portals_mode_button_action)
        self.game_mode_buttons = [self.classic_mode_button, self.portals_mode_button]


        player_count_msg = Rectangle.from_text(SceneType.TITLE_SCENE, SMALL_MSG_FONT, "Player count:", self.game_mode_msg.rect.centerx, SCREEN_HEIGHT/2 + 25)

        self.singleplayer_button = Button.from_text(SceneType.TITLE_SCENE, "1P", MSG_FONT, pygame.Rect(self.classic_mode_button.rect.centerx, player_count_msg.rect.centery -25, 50, 50), self.player_count_button_action)
        self.multiplayer_button = Button.from_text(SceneType.TITLE_SCENE, "2P", MSG_FONT, pygame.Rect(self.portals_mode_button.rect.centerx, player_count_msg.rect.centery - 25, 50, 50), self.player_count_button_action)
        self.player_count_buttons = [self.singleplayer_button, self.multiplayer_button]


        score_to_win_msg = Rectangle.from_text(SceneType.TITLE_SCENE, SMALL_MSG_FONT, "Score to win:", self.game_mode_msg.rect.centerx, 3*SCREEN_HEIGHT/4)

        self.score_to_win_buttons = []
        self.score_to_win_buttons.append(Button.from_text(SceneType.TITLE_SCENE, "3", MSG_FONT, pygame.Rect(self.classic_mode_button.rect.centerx, score_to_win_msg.rect.centery - 25, 50, 50), lambda: self.score_to_win_button_action(3)))
        self.score_to_win_buttons.append(Button.from_text(SceneType.TITLE_SCENE, "7", MSG_FONT, pygame.Rect(SCREEN_WIDTH/2, score_to_win_msg.rect.centery - 25, 50, 50), lambda: self.score_to_win_button_action(7)))
        self.score_to_win_buttons.append(Button.from_text(SceneType.TITLE_SCENE, "11", MSG_FONT, pygame.Rect(self.portals_mode_button.rect.centerx, score_to_win_msg.rect.centery - 25, 50, 50), lambda: self.score_to_win_button_action(11)))

        settings_icon = pygame.image.load("resources\\pixel_art\\settings_icon.png").convert_alpha()
        settings_icon = pygame.transform.scale_by(settings_icon, 1/5)
        self.settings_button = Button.from_image(SceneType.TITLE_SCENE, settings_icon, pygame.Rect(SCREEN_WIDTH-100, 25, settings_icon.get_width(), settings_icon.get_height()), self.settings_button_action)

        music_icon = pygame.image.load("resources\\pixel_art\\music_icon.png").convert_alpha()
        music_icon = pygame.transform.scale_by(music_icon, 1/6)
        self.music_button = Button.from_image(SceneType.TITLE_SCENE, music_icon, create_rect(
            self.settings_button.rect.centerx, self.settings_button.rect.centery + 70, music_icon.get_width(), music_icon.get_height()), self.music_button_action)
        self.music_button.set_visibility(False)
        
        self.sound_fx_button = Button.from_text(SceneType.TITLE_SCENE, "Fx", MSG_FONT, create_rect(
            self.settings_button.rect.centerx, self.music_button.rect.centery + 70, music_icon.get_width(), music_icon.get_height()), self.sound_fx_button_action)
        self.sound_fx_button.set_visibility(False)

        self.settings_rect = Rectangle(SceneType.TITLE_SCENE, None, create_rect(self.settings_button.rect.centerx, (self.music_button.rect.centerx + self.sound_fx_button.rect.centerx)/2, self.settings_button.rect.width, self.music_button.rect.height + self.sound_fx_button.rect.height + 10), None, None, "red")
        self.settings_rect.set_visibility(False)

        self.settings_buttons = [self.settings_button, self.music_button, self.sound_fx_button]

        self._buttons = self.game_mode_buttons + self.player_count_buttons + self.score_to_win_buttons + self.settings_buttons

        self._buttons_pressed_condition = {
            self.classic_mode_button: not game_state_manager.is_portals,
            self.portals_mode_button: game_state_manager.is_portals,
            self.singleplayer_button: not game_state_manager.is_multiplayer,
            self.multiplayer_button: game_state_manager.is_multiplayer,
            self.score_to_win_buttons[0]: game_state_manager.score_to_win == 3, # TODO Remove hard-coding
            self.score_to_win_buttons[1]: game_state_manager.score_to_win == 7,
            self.score_to_win_buttons[2]: game_state_manager.score_to_win == 11,
            self.settings_button: None,
            self.music_button: game_state_manager.play_music,
            self.sound_fx_button: game_state_manager.play_sound_fx
        }

        for button in self._buttons:
            assert button in self._buttons_pressed_condition.keys() 


    @property
    def scene_type(self):
        return SceneType.TITLE_SCENE
    
    @property
    def buttons(self):
        return self._buttons
    
    def update(self):
        pass

    def render(self, screen):
        self._set_title_screen(screen)


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_state_manager.game_mode_selected:
                    game_state_manager.game_active = True
                    return SceneType.GAME_SCENE
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event):
                        if button is self.classic_mode_button:
                            self.classic_mode_button_action()
                        elif button is self.portals_mode_button:
                            self.portals_mode_button_action()
                        elif button is self.singleplayer_button or button is self.multiplayer_button:
                            self.player_count_button_action()
                        elif button in self.player_count_buttons:
                                self.score_to_win_button_action(int(button.content))


    def _set_title_screen(self, screen):
        screen.fill("Black")
        for rect in Rectangle.title_screen_rectangles:
            rect.display(screen)

        for button in self.buttons:
            if self._buttons_pressed_condition[button]:
                button.press()
            button.draw(screen)

    def game_mode_button_action(self):
        Button.reset_group_of_buttons(self.game_mode_buttons)
        game_state_manager.game_mode_selected = True
        self.title_msg.change_text(MSG_FONT, "Press Space to start")
        
    def classic_mode_button_action(self):
        self.game_mode_button_action()
        game_state_manager.is_portals = False
        #self.classic_mode_button.press()
        self.portals_mode_button.release()

    def portals_mode_button_action(self):
        self.game_mode_button_action()
        game_state_manager.is_portals = True
        game_state_manager.start_timer(game_state_manager.portal_timer, 3000)
        self.classic_mode_button.release()
        #scene.portals_mode_button.press()

    def player_count_button_action(self):
        Button.reset_group_of_buttons(self.player_count_buttons)
        if game_state_manager.is_multiplayer:
            #self.multiplayer_button.press()
            self.singleplayer_button.release()
        else:
            self.multiplayer_button.release()
            #self.singleplayer_button.press()
        #game_state_manager.is_multiplayer = button is self.multiplayer_button # TODO

    def score_to_win_button_action(self, score):
        Button.reset_group_of_buttons(self.score_to_win_buttons)
        game_state_manager.score_to_win = score
        self.score_to_win_buttons[score].press()

    def settings_button_action(self):
        self.music_button.set_visibility(not self.music_button.is_visible)
        self.sound_fx_button.set_visibility(not self.sound_fx_button.is_visible)
        if self.music_button.is_visible:
            self.settings_rect.set_visibility(True)
        self.settings_button.release()

    def music_button_action(self):
        game_state_manager.play_music = not game_state_manager.play_music
        if game_state_manager.play_music:
            sound.bg_music.play(loops=-1)
            self.music_button.release()
        else:
            sound.bg_music.stop()

    def sound_fx_button_action(self):
        game_state_manager.play_sound_fx = not game_state_manager.play_sound_fx
        if game_state_manager.play_sound_fx:
            self.sound_fx_button.release()


title_scene = TitleScene()