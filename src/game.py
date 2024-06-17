import pygame
from constants import *

from scene.scene_type import SceneType
from scene.scene_manager import SceneManager


pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

scene_manager = SceneManager()
scene_manager.switch_to(SceneType.TITLE_SCENE)

# Game loop
while True:
    events = pygame.event.get()
    scene_manager.handle_events(events)
    scene_manager.update()
    scene_manager.render(screen)
    pygame.display.flip()
    clock.tick(60)