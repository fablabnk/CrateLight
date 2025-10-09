"""Rainbow and color cycling effects"""

from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import wheel, scale_color


class RainbowChase(Effect, BPMSyncedEffect):
    """Rainbow that moves with the beat"""

    def setup(self):
        self.position = 0

    def update(self):
        phase = self.get_beat_phase()

        # Move position based on beat phase
        beat_position = int(phase * self.width)

        for y in range(self.height):
            for x in range(self.width):
                # Rainbow color based on position
                distance = abs(x - beat_position)
                color_pos = (x * 8 + self.frame_count) % 256
                brightness = max(0, 1.0 - distance / 8.0)

                color = scale_color(wheel(color_pos), brightness)

                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        return True
