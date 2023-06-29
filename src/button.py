import pygame
from constants import TITLE_SCREEN, RESTART_SCREEN, HIGHLIGHT_COLOR

def is_mouse_in_rect(rect, mouse_x, mouse_y):
        return rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom

class Button:
    buttons = []
    title_screen_buttons = []
    restart_screen_buttons = []
    game_screen_buttons = []

    def __init__(self, display_screen, content, rect, action, background_color=0):
        self.content = content
        self.display_screen = display_screen
        self.rect = rect
        self.is_pressed = False
        self.action = action
        self.background_color = background_color
        Button.buttons.append(self)
        if not type(self.display_screen) == list:
            screens = [self.display_screen]
            for screen in screens:
                if screen == TITLE_SCREEN:
                    Button.title_screen_buttons.append(self)
                elif screen == RESTART_SCREEN:
                    Button.restart_screen_buttons.append(self)
                else:
                    Button.game_screen_buttons.append(self)

    @classmethod
    def from_image(cls, display_screen, img, rect, action):
        return cls(display_screen, img, rect, action)

    @classmethod
    def from_text(cls, display_screen, txt, font, rect, action, txt_color="white", background_color=0):
        return cls(display_screen, font.render(txt, False, txt_color), rect, action, background_color)
    
    def display(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if is_mouse_in_rect(self.rect, mouse_x, mouse_y) or self.is_pressed:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, self.rect)
        elif self.background_color == 1:
            pygame.draw.rect(screen, "white", self.rect)
        else:
            pygame.draw.rect(screen, "white", self.rect, 1)
        screen.blit(self.content, self.rect)

