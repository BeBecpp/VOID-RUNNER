# src/settings.py

# Window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "VOID RUNNER"

# Colors
BLACK = (5, 5, 8)
DARK_GRAY = (18, 18, 24)
WHITE = (245, 245, 245)
LIGHT_GRAY = (170, 170, 180)
GRAY = (90, 90, 100)
RED = (255, 42, 42)
DARK_RED = (120, 10, 20)

# Extra colors
GEM_BLUE = (80, 190, 255)
GEM_GLOW = (20, 90, 140)
GREEN = (70, 180, 120)
YELLOW = (240, 190, 80)

# Player
PLAYER_RADIUS = 10
PLAYER_SPEED = 6

# Obstacles
OBSTACLE_MIN_SIZE = 24
OBSTACLE_MAX_SIZE = 52
OBSTACLE_START_COUNT = 7
OBSTACLE_START_SPEED = 4
OBSTACLE_SPEED_INCREMENT = 0.003

# Gems
GEM_RADIUS = 9
GEM_SCORE_VALUE = 25
GEM_SPAWN_PADDING = 70

# Score
SURVIVAL_SCORE_MULTIPLIER = 1
GEM_SCORE_MULTIPLIER = 25

# Difficulty
DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]

DIFFICULTY_SETTINGS = {
    "EASY": {
        "obstacle_count": 5,
        "speed_bonus": -0.6,
        "gem_value": 20,
        "survival_score_rate": 0.5,
    },
    "MEDIUM": {
        "obstacle_count": 7,
        "speed_bonus": 0,
        "gem_value": 25,
        "survival_score_rate": 1,
    },
    "HARD": {
        "obstacle_count": 10,
        "speed_bonus": 1.2,
        "gem_value": 35,
        "survival_score_rate": 1.5,
    },
}

# Files
HIGHSCORE_FILE = "data/highscore.txt"

# Font
FONT_NAME = None
TITLE_FONT_SIZE = 72
MENU_FONT_SIZE = 28
HUD_FONT_SIZE = 28
SMALL_FONT_SIZE = 20