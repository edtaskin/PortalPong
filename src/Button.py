import pygame
import Constants

class Button:
    def __init__(self, msg, font, x_pos, y_pos, width, height):
        self.msg = msg
        self.msg_text = font.render(msg, False, "white")
        self.font = font
        self.button_rect = pygame.Rect(x_pos, y_pos, width, height)
        self.msg_rect = self.msg_text.get_rect(midleft = (x_pos, y_pos))
        self.is_pressed = False

    def press_button(self):
        self.is_pressed = True

    def change_msg(self, new_msg):
        self.msg_text = self.font.render(new_msg, False, "white")