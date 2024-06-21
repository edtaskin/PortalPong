import pygame

class _GameStateManager:
    def __init__(self):
        self.set_default_settings()


    def set_default_settings(self):
        self.game_active = False
        self.is_game_over = False
        self.is_multiplayer = None
        self.is_online = False
        self.is_portals = False
        self.score_to_win = 3
        self.game_mode_selected = False
        self.player_count_selected = False
        self.p1_win = False
        self.play_music = True
        self.play_sound_fx = True
        self._user_events = []


    def reset_game(self):
        game_state_manager.game_active = False
        game_state_manager.is_game_over = True


    def define_user_event(self):
        user_events_count = len(self._user_events)
        new_event = pygame.USEREVENT + (user_events_count + 1)
        self._user_events.append(new_event)
        return new_event

game_state_manager = _GameStateManager()