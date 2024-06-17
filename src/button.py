import pygame
from constants import BACKGROUND_COLOR, HIGHLIGHT_COLOR, FILL_COLOR

def is_mouse_in_rect(rect, mouse_x, mouse_y):
        return rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom

class Button:
    def __init__(self, display_screen, content, rect, action, outline_color="white", background_color="black", text=None):
        self.text = text
        self.content = content
        self.display_screen = display_screen
        self.rect = rect
        self.is_pressed = False
        self.action = action
        self.outline_color = outline_color
        self.background_color = background_color
        self.is_visible = True

    @classmethod
    def from_image(cls, display_screen, img, rect, action, outline_color="white"):
        return cls(display_screen, img, rect, action, outline_color)

    @classmethod
    def from_text(cls, display_screen, text, font, rect, action, text_color="white", outline_color="white", background_color="black"):
        return cls(display_screen, font.render(text, False, text_color), rect, action, outline_color=outline_color, background_color=background_color, text=text)
    
    def press(self):
        self.is_pressed = True
        self.background_color = FILL_COLOR
        #self.action()

    def release(self):
        self.is_pressed = False
        self.background_color = BACKGROUND_COLOR

    def set_visibility(self, is_visible):
        self.is_visible = is_visible

    def draw(self, screen):
        if not self.is_visible:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if is_mouse_in_rect(self.rect, mouse_x, mouse_y) and not self.is_pressed:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, self.rect)
        elif self.is_pressed:
            pygame.draw.rect(screen, self.background_color, self.rect)
        if self.outline_color != None:
            pygame.draw.rect(screen, self.outline_color, self.rect, 1)
        screen.blit(self.content, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    @staticmethod
    def reset_group_of_buttons(buttons):
        for button in buttons:
            button.release()