"""Pulse and breathing effects"""

from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import sine_wave, scale_color, wheel

# Constants for pulse configuration
PULSE_SINE_POWER = 2.0  # Higher power = sharper pulse peak
PULSE_COLOR_HUE_STEP = 16  # Color change per beat (slower = smaller number)


class PulseOnBeat(Effect, BPMSyncedEffect):
    """Pulse brightness on each beat"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, color=None):
        super().__init__(pixels, width, height, hardware_config, clock)
        self.color = color  # Optional fixed color, None for rainbow cycling

    def setup(self):
        self.color_offset = 0
        self.beat_count = 0

    def update(self):
        # Get beat phase (0.0 to 1.0)
        phase = self.get_beat_phase()

        # Track beat changes for color cycling using standardized beat detection
        if self.beat_occurred():
            self.beat_count += 1
            # Change color every 2 beats for slower rainbow cycling
            self.color_offset = (self.beat_count * PULSE_COLOR_HUE_STEP) % 256

        # Pulse on beat
        brightness = sine_wave(phase, power=PULSE_SINE_POWER)

        # Use fixed color or cycle through colors based on beats
        if self.color:
            color = self.color
        else:
            color = wheel(self.color_offset)

        final_color = scale_color(color, brightness)

        # Optimization: use fill() when setting all pixels to same color
        self.pixels.fill(final_color)

        return True  # Run forever (manager will stop after beats)

    def cleanup(self):
        """Clear display when effect ends"""
        from ..colors import COLORS
        self.pixels.fill(COLORS["OFF"])
