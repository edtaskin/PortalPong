import pygame
from constants import TITLE_SCREEN, RESTART_SCREEN, HIGHLIGHT_COLOR, FILL_COLOR

def is_mouse_in_rect(rect, mouse_x, mouse_y):
        return rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom

class Button:
    buttons = []
    title_screen_buttons = []
    restart_screen_buttons = []
    game_screen_buttons = []

    def __init__(self, display_screen, content, rect, action, outline_color="white", background_color="black"):
        self.content = content
        self.display_screen = display_screen
        self.rect = rect
        self.is_pressed = False
        self.action = action
        self.outline_color = outline_color
        self.background_color = background_color
        self.is_visible = True
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
    def from_image(cls, display_screen, img, rect, action, outline_color="white"):
        return cls(display_screen, img, rect, action, outline_color)

    @classmethod
    def from_text(cls, display_screen, txt, font, rect, action, txt_color="white", outline_color="white", background_color="black"):
        return cls(display_screen, font.render(txt, False, txt_color), rect, action, outline_color, background_color)
    
    def press(self):
        self.is_pressed = True
        self.background_color = HIGHLIGHT_COLOR

    def release(self):
        self.is_pressed = False
        self.background_color = "black"

    def set_visibility(self, is_visible):
        self.is_visible = is_visible

    def display(self, screen):
        if not self.is_visible:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if is_mouse_in_rect(self.rect, mouse_x, mouse_y) and not self.is_pressed:
            pygame.draw.rect(screen, FILL_COLOR, self.rect)
        else:
            pygame.draw.rect(screen, self.background_color, self.rect)
        if self.outline_color != None:
            pygame.draw.rect(screen, self.outline_color, self.rect, 1)
        screen.blit(self.content, self.rect)

