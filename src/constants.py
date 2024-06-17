import pygame

def initialize_pygame():
    global screen
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    initialize_fonts()

def initialize_fonts():
    global TITLE_FONT, MSG_FONT, SMALL_MSG_FONT
    TITLE_FONT = pygame.font.Font(FONT, 80)
    MSG_FONT = pygame.font.Font(FONT, 50)
    SMALL_MSG_FONT = pygame.font.Font(FONT, 30)

SCREEN_HEIGHT = 550
SCREEN_WIDTH = 800
SCORE_HEIGHT = 50
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
BALL_SIZE = 20
MAX_BOUNCE_ANGLE = 75
PADDLE_SPEED = 4
BALL_RESET_COOLDOWN = 1500
FONT = "resources/font/VT323-Regular.ttf"
PORTAL_COLORS = ["blue", "red", "yellow", "orange", "green", "pink", "#00FFFF", "#FF1493", "#4B0082", "#808000", "#7FFF00", "#20B2AA", "#FFD700"]
BACKGROUND_COLOR = "black"
HIGHLIGHT_COLOR = "#FF8C00"
FILL_COLOR = "#4B0082"
TITLE_FONT = None
MSG_FONT = None
SMALL_MSG_FONT = None
screen = None

initialize_pygame()