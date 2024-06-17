from constants import screen
import pygame
from game_state_manager import game_state_manager
from random import choice
from .scene_type import SceneType
from .title_scene import TitleScene
from .restart_scene import RestartScene
from .game_scene import GameScene

class SceneManager:
    def __init__(self):
        self.scenes = {
            SceneType.TITLE_SCENE: TitleScene(),
            SceneType.RESTART_SCENE: RestartScene(),
            SceneType.GAME_SCENE: GameScene()
        }
        self.current_scene = None
        self.current_scene_type = None

    def switch_to(self, scene_type):
        self.current_scene = self.scenes[scene_type]
    
    def update(self):
        self.current_scene.update()

    def render(self, screen):
        self.current_scene.render(screen)

    def handle_events(self, events):
        next_scene = self.current_scene.handle_events(events)
        if next_scene:
            self.switch_to(next_scene)