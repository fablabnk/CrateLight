"""Color definitions and utilities for LED animations"""

import random

COLORS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 128, 0),
    "PURPLE": (128, 0, 255),
    "MAGENTA": (255, 0, 128),
    "CYAN": (0, 255, 255),
    "OFF": (0, 0, 0),
}

def get_random_color():
    """Returns a random color tuple from the COLORS dictionary."""
    return random.choice(list(COLORS.values()))
