import pygame
# TODO Can it be used anywhere else?
def create_rect(centerx, centery, width, height):
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (centerx, centery)
    return rect
