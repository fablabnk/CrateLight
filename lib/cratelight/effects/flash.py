"""Flash and strobe effects"""

from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS
from ..utils import scale_color


class FlashOnBeat(Effect, BPMSyncedEffect):
    """Flash bright on each beat"""

    def setup(self):
        self.beat_color = COLORS["WHITE"]

    def update(self):
        phase = self.get_beat_phase()

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
    """Strobe on every beat"""

    def setup(self):
        self.colors = [COLORS["RED"], COLORS["BLUE"], COLORS["GREEN"], COLORS["YELLOW"]]
        self.color_index = 0

    def update(self):
        # Change color on beat
        if self.is_beat(tolerance=0.15):
            self.color_index = (self.color_index + 1) % len(self.colors)

        phase = self.get_beat_phase()

        # Quick flash
        if phase < 0.2:
            color = self.colors[self.color_index]
        else:
            color = COLORS["OFF"]

        for i in range(len(self.pixels)):
            self.pixels[i] = color

        return True
