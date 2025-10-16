"""Flash and strobe effects"""

from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS, get_random_color
from ..utils import scale_color, wheel


class FlashOnBeat(Effect, BPMSyncedEffect):
    """
    Flash bright on each beat

    Usage:
        manager.add_effect(FlashOnBeat, beats=4, rainbow=True)  # Rainbow cycling
        manager.add_effect(FlashOnBeat, beats=4, random_color=True)  # Random colors
        manager.add_effect(FlashOnBeat, beats=4, color=COLORS["RED"])  # Fixed color
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 color=None, rainbow=False, random_color=False):
        """
        Initialize flash effect

        Args:
            color: Fixed color to use (None for white)
            rainbow: Cycle through rainbow colors on each beat
            random_color: Use random color on each beat
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.fixed_color = color
        self.rainbow = rainbow
        self.random_color = random_color
        self.beat_color = COLORS["WHITE"]
        self.rainbow_offset = 0

    def setup(self):
        self.beat_color = COLORS["WHITE"]
        self.rainbow_offset = 0
        self.last_phase = 1.0  # Track when beat occurs

    def update(self):
        phase = self.get_beat_phase()

        # Detect new beat (phase wraps from ~1.0 to ~0.0)
        if phase < 0.1 and self.last_phase > 0.9:
            # New beat! Update color
            if self.rainbow:
                self.beat_color = wheel(self.rainbow_offset)
                self.rainbow_offset = (self.rainbow_offset + 32) % 256
            elif self.random_color:
                self.beat_color = get_random_color()
            elif self.fixed_color:
                self.beat_color = self.fixed_color
            else:
                self.beat_color = COLORS["WHITE"]

        self.last_phase = phase

        # Sharp flash at beat start
        if phase < 0.1:
            brightness = 1.0 - (phase / 0.1)  # Fast decay
        else:
            brightness = 0.0

        color = scale_color(self.beat_color, brightness)

        for i in range(len(self.pixels)):
            self.pixels[i] = color

        return True


class StrobeEffect(Effect, BPMSyncedEffect):
    """
    Strobe on every beat

    Usage:
        manager.add_effect(StrobeEffect, beats=4, rainbow=True)  # Rainbow cycling
        manager.add_effect(StrobeEffect, beats=4, random_color=True)  # Random colors
        manager.add_effect(StrobeEffect, beats=4)  # Default color cycling
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 rainbow=False, random_color=False):
        """
        Initialize strobe effect

        Args:
            rainbow: Cycle through rainbow colors smoothly
            random_color: Use random color on each beat
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.rainbow = rainbow
        self.random_color = random_color

    def setup(self):
        self.colors = [COLORS["RED"], COLORS["BLUE"], COLORS["GREEN"], COLORS["YELLOW"],
                      COLORS["CYAN"], COLORS["MAGENTA"], COLORS["WHITE"]]
        self.color_index = 0
        self.rainbow_offset = 0
        self.current_color = self.colors[0]

    def update(self):
        # Change color on beat
        if self.is_beat(tolerance=0.15):
            if self.rainbow:
                # Smooth rainbow cycling
                self.current_color = wheel(self.rainbow_offset)
                self.rainbow_offset = (self.rainbow_offset + 32) % 256
            elif self.random_color:
                # Random color each beat
                self.current_color = get_random_color()
            else:
                # Cycle through preset colors
                self.color_index = (self.color_index + 1) % len(self.colors)
                self.current_color = self.colors[self.color_index]

        phase = self.get_beat_phase()

        # Quick flash
        if phase < 0.2:
            color = self.current_color
        else:
            color = COLORS["OFF"]

        for i in range(len(self.pixels)):
            self.pixels[i] = color

        return True
