"""Pre-built LED effects for CrateLight"""

from .pulse import PulseOnBeat
from .wave import WaveEffect
from .flash import FlashOnBeat, StrobeEffect
from .rainbow import RainbowChase
from .gameoflife import GameOfLife

__all__ = [
    'PulseOnBeat',
    'WaveEffect',
    'FlashOnBeat',
    'StrobeEffect',
    'RainbowChase',
    'GameOfLife',
]
