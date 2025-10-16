"""Pre-built LED effects for CrateLight"""

from .pulse import PulseOnBeat
from .wave import WaveEffect
from .flash import FlashOnBeat, StrobeEffect
from .rainbow import RainbowChase
from .game_of_life import GameOfLife
from .scrolling import StaticText, ScrollingText, BlinkingText, CountdownEffect
from .random_fill import RandomFill, PixelRandomFill, RandomStrobe
from .color_scroll import (
    ColorScrollVertical,
    ColorScrollHorizontal,
    RainbowScrollVertical,
    RainbowScrollHorizontal,
)

# Optional GFX font effects (requires adafruit_bitmap_font)
try:
    from .scrolling_gfx import GFXScrollingText, GFXStaticText
    HAS_GFX_EFFECTS = True
except ImportError:
    HAS_GFX_EFFECTS = False
    GFXScrollingText = None
    GFXStaticText = None

__all__ = [
    'PulseOnBeat',
    'WaveEffect',
    'FlashOnBeat',
    'StrobeEffect',
    'RainbowChase',
    'GameOfLife',
    'StaticText',
    'ScrollingText',
    'BlinkingText',
    'CountdownEffect',
    'RandomFill',
    'PixelRandomFill',
    'RandomStrobe',
    'ColorScrollVertical',
    'ColorScrollHorizontal',
    'RainbowScrollVertical',
    'RainbowScrollHorizontal',
    'GFXScrollingText',
    'GFXStaticText',
]
