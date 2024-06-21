from abc import ABC, abstractmethod
from sprite.button import Button
from scene.scene_type import SceneType
from game_state_manager import game_state_manager

class Scene(ABC):
    def __init__(self):
        self.switched_to_scene_event = game_state_manager.define_user_event()
        
    @property
    @abstractmethod
    def scene_type(self) -> SceneType:
        pass

    @property
    def buttons(self) -> list[Button]:
        pass

    @abstractmethod
    def render(self, screen):
        """
        Displays the updated scene on the screen.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Updates the game states as per the game logic.
        """
        pass

    @abstractmethod
    def handle_events(self, events):
        pass
