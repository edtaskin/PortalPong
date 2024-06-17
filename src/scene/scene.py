from abc import ABC, abstractmethod
from button import Button
from scene.scene_type import SceneType

class Scene(ABC):
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
        """Updates the game states as per the game logic."""
        pass

    @abstractmethod
    def handle_events(self, events):
        pass
    
    # TODO: Del
    def handle_button_click(self, click_pos):
        for button in self.buttons:
            if button.rect.collidepoint(click_pos):
                    print("HEREEEEE")
                    button.press()
