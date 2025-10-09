"""Pulse and breathing effects"""

from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import sine_wave, scale_color, wheel


class PulseOnBeat(Effect, BPMSyncedEffect):
    """Pulse brightness on each beat"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, color=None):
        super().__init__(pixels, width, height, hardware_config, clock)
        self.color = color  # Optional fixed color, None for rainbow cycling

    def setup(self):
        self.color_offset = 0

    def update(self):
        # Get beat phase (0.0 to 1.0)
        phase = self.get_beat_phase()

        # Pulse on beat
        brightness = sine_wave(phase, power=2.0)

        # Use fixed color or cycle through colors
        if self.color:
            color = self.color
        else:
            color = wheel((self.color_offset + self.frame_count) % 256)

        final_color = scale_color(color, brightness)

        # Fill all LEDs
        for i in range(len(self.pixels)):
            self.pixels[i] = final_color

        return True  # Run forever (manager will stop after beats)
