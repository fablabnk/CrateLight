import random

COLORS = {
    "RED": (0, 255, 0),
    "GREEN": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 128, 0),
    "PURPLE": (128, 0, 255),
    #"LIME": (128, 255, 0),
    #"TEAL": (0, 255, 128),
    #"PASTEL_GREEN": (192, 64, 64),
    #"PASTEL_BLUE": (64, 64, 255),
    #"PASTEL_RED": (64, 255, 64),
    #"PASTEL_PURPLE": (128, 64, 192),
    #"PASTEL_YELLOW": (192, 192, 64),
    #"SKY_BLUE": (64, 128, 255),
    #"SUNSET": (255, 64, 32),
    #"AQUA": (64, 255, 192),
    "MAGENTA": (255, 0, 128),
    #"GOLD": (255, 192, 0),
    #"TURQUOISE": (64, 255, 128),
    #"PEACH": (255, 64, 64),
    #"INDIGO": (64, 0, 255),
    #"CHARTREUSE": (128, 255, 0),
    #"OLIVE": (128, 128, 0),
    #"GRAY": (128, 128, 128),
    #"DARK_GRAY": (64, 64, 64),
    #"LIGHT_GRAY": (192, 192, 192),
    #"MINT": (128, 255, 192),
    #"LAVENDER": (192, 128, 255),
    #"ROSE": (255, 128, 192),
    #"CORAL": (255, 128, 64),
    "CYAN": (0, 255, 255),
    #"PINK": (255, 0, 255),
    "OFF": (0, 0, 0),
}

def get_random_color():
    """Returns a random color tuple from the COLORS dictionary."""
    return random.choice(list(COLORS.values()))