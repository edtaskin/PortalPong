import pygame
from scene.scene_type import SceneType

class Rectangle:
    rectangles = []
    title_screen_rectangles = []

    def __init__(self, display_screen, content, rect, outline_color=None, outline_width=None, background_color=None):
        self.content = content
        self.rect = rect
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.background_color = background_color
        self.is_visible = True
        Rectangle.rectangles.append(self)
        if display_screen == SceneType.TITLE_SCENE:
            Rectangle.title_screen_rectangles.append(self)

    @classmethod
    def from_image(cls, display_screen, img, rect, outline_color = None, outline_width=None):
        return cls(display_screen, img, rect, outline_color, outline_width)

    @classmethod
    def from_text(cls, display_screen, font, msg, centerx, centery, color="white", outline_color=None, outline_width=None):
        content = font.render(msg, False, color)
        rect = content.get_rect(center = (centerx, centery))
        return cls(display_screen, content, rect, outline_color, outline_width)
    
    @classmethod
    def from_rect(cls, display_screen, font, msg, rect, color="white", outline_color=None, outline_width=None, background_color="black"):
        return cls(display_screen, font.render(msg, False, color), rect, outline_color, outline_width, background_color)

    def change_text(self, font, new_txt, color="white"):
        self.content = font.render(new_txt, False, color)

    def change_outline(self, outline_color, outline_width=None):
        self.outline_color = outline_color
        self.outline_width =outline_width

    def set_visibility(self, is_visible):
        self.is_visible = is_visible

    def display(self, screen):
        if not self.is_visible:
            return
        if self.background_color != None:
            pygame.draw.rect(screen, self.background_color, self.rect)
        if self.outline_color != None and self.outline_width != None:
            pygame.draw.rect(screen, self.outline_color, self.rect, self.outline_width)
        if self.content != None:
            screen.blit(self.content, self.rect)