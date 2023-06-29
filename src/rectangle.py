import pygame
from constants import TITLE_SCREEN

class Rectangle:
    rectangles = []
    title_screen_rectangles = []

    def __init__(self, display_screen, content, rect, outline=False):
        self.content = content
        self.rect = rect
        self.has_outline = outline
        Rectangle.rectangles.append(self)
        if display_screen == TITLE_SCREEN:
            Rectangle.title_screen_rectangles.append(self)

    @classmethod
    def from_image(cls, display_screen, img, rect, outline=False):
        return cls(display_screen, img, rect, outline)

    @classmethod
    def from_text(cls, display_screen, font, msg, centerx, centery, color="white", outline=False):
        content = font.render(msg, False, color)
        rect = content.get_rect(center = (centerx, centery))
        return cls(display_screen, content, rect, outline)
    
    @classmethod
    def from_rect(cls, display_screen, content, rect, outline=False):
        return cls(display_screen, content, rect, outline)

    def update_text(self, font, new_txt, color="white"):
        self.content = font.render(new_txt, False, color)

    def display(self, screen):
        screen.blit(self.content, self.rect)
        if self.has_outline:
            pygame.draw.rect(screen, "white", self.rect, 1)
