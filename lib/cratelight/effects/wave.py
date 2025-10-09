"""Wave and ripple effects"""

from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import wheel


class WaveEffect(Effect, BPMSyncedEffect):
    """Wave pattern synced to BPM"""

    def setup(self):
        self.offset = 0

    def update(self):
        phase = self.get_beat_phase()

        for y in range(self.height):
            for x in range(self.width):
                # Wave based on position and beat
                wave_pos = (x + y + phase * 10) % 256
                color = wheel(int(wave_pos))

                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        return True
