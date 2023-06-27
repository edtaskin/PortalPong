import pygame

class Button:
    buttons = []

    def __init__(self, display_screen, content, rect, txt=None):
        self.content = content
        self.display_screen = display_screen
        self.rect = rect
        self.is_pressed = False
        self.txt = txt
        Button.buttons.append(self)
        
    @classmethod
    def from_image(cls, display_screen, img, rect):
        return cls(display_screen, img, rect)

    @classmethod
    def from_text(cls, display_screen, txt, font, rect):
        return cls(display_screen, font.render(txt, False, "white"), rect, txt)