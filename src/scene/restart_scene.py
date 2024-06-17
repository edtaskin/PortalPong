from constants import *
from rectangle import Rectangle
from .scene_type import SceneType
from .scene import Scene
from game_state_manager import game_state_manager
from button import Button

class RestartScene(Scene):
    def __init__(self):
        self.title = Rectangle.from_text(SceneType.TITLE_SCENE, TITLE_FONT, "Pong", SCREEN_WIDTH/2,80)
        self.loss_msg = Rectangle.from_text(SceneType.RESTART_SCENE, MSG_FONT, "YOU LOSE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "red")
        self.win_msg = Rectangle.from_text(SceneType.RESTART_SCENE, MSG_FONT, "YOU WIN", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "green")

        if game_state_manager.is_multiplayer:
            self.win_msg.change_text(MSG_FONT, "P1 WIN", "green")
            self.loss_msg.change_text(MSG_FONT, "P2 WIN", "blue")

        self.back_button = Button.from_text(SceneType.RESTART_SCENE, "<-BACK", SMALL_MSG_FONT, pygame.Rect(50, 50, 80, 30), RestartScene.back_button_action)

    @property
    def scene_type(self):
        return SceneType.TITLE_SCENE
    
    @property
    def buttons(self):
        return None
    
    def update(self):
        pass

    def handle_events(self, events):
        pass

    def render(self, screen):
        self.set_restart_scene(screen)

    def set_restart_scene(self, screen):
        screen.fill("Black")
        #self.display.title.display(screen)
        self.title_msg.display(screen)
        
        if game_state_manager.p1_win:  
            self.win_msg.display(screen)
        else:       
            self.loss_msg.display(screen)

    def back_button_action(scene):
        game_state_manager.game_active = False
        game_state_manager.is_game_over = False
        #reset_group_of_buttons(title_screen_buttons)
        scene.back_button.release()
        return SceneType.TITLE_SCENE
