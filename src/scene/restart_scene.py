from constants import *
from rectangle import Rectangle
from .scene_type import SceneType
from .scene import Scene
from game_state_manager import game_state_manager
from button import Button

class RestartScene(Scene):
    def __init__(self):
        self.title = Rectangle.from_text(SceneType.RESTART_SCENE, TITLE_FONT, "Pong", SCREEN_WIDTH/2, 80)
        self.loss_msg = Rectangle.from_text(SceneType.RESTART_SCENE, MSG_FONT, "YOU LOSE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "red")
        self.win_msg = Rectangle.from_text(SceneType.RESTART_SCENE, MSG_FONT, "YOU WIN", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "green")

        self.back_button = Button.from_text(SceneType.RESTART_SCENE, "<-BACK", SMALL_MSG_FONT, pygame.Rect(50, 50, 80, 30), RestartScene.back_button_action)
    
    @property
    def scene_type(self):
        return SceneType.RESTART_SCENE
    
    @property
    def buttons(self):
        return [self.back_button]
    
    def update(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event):
                        if button is self.back_button:
                            return self.back_button_action()

    def render(self, screen):
        self._set_restart_scene(screen)

    def _set_restart_scene(self, screen):
        screen.fill("Black")
        self.title.display(screen)

        if game_state_manager.is_multiplayer:
            self.win_msg.change_text(MSG_FONT, "P1 WIN", "blue")
            self.loss_msg.change_text(MSG_FONT, "P2 WIN", "green")
        else:
            self.win_msg.change_text(MSG_FONT, "YOU WIN", "green")
            self.loss_msg.change_text(MSG_FONT, "YOU LOSE", "red")

        if game_state_manager.p1_win:  
            self.win_msg.display(screen)
        else:       
            self.loss_msg.display(screen)

        for button in self.buttons:
            button.draw(screen)

    def back_button_action(self):
        game_state_manager.reset_game()
        self.back_button.release()
        return SceneType.TITLE_SCENE
