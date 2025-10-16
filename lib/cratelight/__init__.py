"""CrateLight - LED Animation Library for Raspberry Pi Pico"""

from .colors import COLORS, get_random_color
from .grid_utils import (
    ids_by_coord,
    coords_to_id,
    id_to_coords,
    clear_grid,
    borders,
    color_coords,
    color_id,
    draw_from_grid
)
from .animations import (
    light_up_grid_horizontal,
    light_up_grid_vertical,
    light_up_grid
)
from .game_of_life import gol_step
from .effect_base import Effect
from .clock import ClockSource, BPMClock, FixedBPMClock, ManualClock
from .utils import wheel, scale_color, sine_wave, lerp_color
from .hardware import (
    HardwareConfig,
    CrateLightGrid,
    LEDStrip,
    ZigzagGrid,
    LinearGrid
)
from .effect_manager import EffectManager, BPMSyncedEffect
from .text import Font, Font8x8, TextRenderer

# Optional GFX font support (requires adafruit_bitmap_font)
try:
    from .text_gfx import GFXTextRenderer, SimpleGFXTextRenderer
    HAS_GFX_FONTS = True
except ImportError:
    HAS_GFX_FONTS = False
    GFXTextRenderer = None
    SimpleGFXTextRenderer = None

from . import effects

__version__ = "0.1.0"
__all__ = [
    "COLORS",
    "get_random_color",
    "ids_by_coord",
    "coords_to_id",
    "id_to_coords",
    "clear_grid",
    "borders",
    "color_coords",
    "color_id",
    "draw_from_grid",
    "light_up_grid_horizontal",
    "light_up_grid_vertical",
    "light_up_grid",
    "gol_step",
    "Effect",
    "ClockSource",
    "BPMClock",
    "FixedBPMClock",
    "ManualClock",
    "wheel",
    "scale_color",
    "sine_wave",
    "lerp_color",
    "HardwareConfig",
    "CrateLightGrid",
    "LEDStrip",
    "ZigzagGrid",
    "LinearGrid",
    "EffectManager",
    "BPMSyncedEffect",
    "Font",
    "Font8x8",
    "TextRenderer",
    "GFXTextRenderer",
    "SimpleGFXTextRenderer",
    "HAS_GFX_FONTS",
    "effects",
]
