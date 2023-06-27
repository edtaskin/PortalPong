import pygame

buttons = []

class Button:
    def __init__(self, msg, font, display_screen, x_pos, y_pos, width, height):
        self.msg = msg
        self.msg_text = font.render(msg, False, "white")
        self.font = font
        self.button_rect = pygame.Rect(x_pos, y_pos, width, height)
        self.msg_rect = self.msg_text.get_rect(center = (x_pos, y_pos))
        self.display_screen = display_screen
        self.is_pressed = False
        buttons.append(self)