import pygame
import constants

class Button:
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x # (x, y) is the corrdinates of the top-left corner
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.Font(constants.FONT, 30)
            text = font.render(self.text, 1, "White")
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))