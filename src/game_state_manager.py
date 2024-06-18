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
        self.portal_timer = pygame.USEREVENT + 1
        self.play_music = True
        self.play_sound_fx = True


    def reset_game(self):
        game_state_manager.game_active = False
        game_state_manager.is_game_over = True


    def start_timer(self, timer, duration):
        pygame.time.set_timer(timer, duration)

game_state_manager = _GameStateManager()