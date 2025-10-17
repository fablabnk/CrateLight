"""Rainbow and color cycling effects"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import wheel, scale_color

# Constants for rainbow chase configuration
CHASE_COLOR_STEP_PER_PIXEL = 8  # Hue change between adjacent pixels
CHASE_COLOR_STEP_PER_BEAT = 32  # Hue rotation per beat
CHASE_BRIGHTNESS_CENTER = 1.0  # Brightness at chase center
CHASE_BRIGHTNESS_TAIL = 0.8  # Starting brightness for tail
CHASE_BRIGHTNESS_BACKGROUND = 0.1  # Dim background brightness
CHASE_CENTER_WIDTH = 2  # Pixels in bright center
CHASE_TAIL_LENGTH = 8  # Length of trailing gradient


class RainbowChase(Effect, BPMSyncedEffect):
    """
    Rainbow chase that sweeps with the beat - now with configurable direction!

    Usage:
        manager.add_effect(RainbowChase, beats=8, direction="right")  # Default
        manager.add_effect(RainbowChase, beats=8, direction="left")
        manager.add_effect(RainbowChase, beats=8, direction="up")
        manager.add_effect(RainbowChase, beats=8, direction="down")
        manager.add_effect(RainbowChase, beats=8, direction="random")  # Picks new direction each time
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 direction="right"):
        """
        Initialize rainbow chase

        Args:
            direction: "right", "left", "up", "down", or "random"
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.direction = direction

    def setup(self):
        self.beat_count = 0

        # Pick random direction if requested
        if self.direction == "random":
            self.active_direction = random.choice(["right", "left", "up", "down"])
        else:
            self.active_direction = self.direction

    def update(self):
        # Check if beat occurred THIS frame (most reliable method)
        beat_now = self.clock and self.clock.beat_occurred()

        # Get phase for smooth interpolation within beat
        phase = self.get_beat_phase()

        if beat_now:
            self.beat_count += 1

        # Calculate sweep position based on direction
        for y in range(self.height):
            for x in range(self.width):
                # Determine distance from chase position based on direction
                if self.active_direction == "right":
                    beat_position = phase * self.width
                    distance = abs(x - beat_position)
                    color_pos = (x * CHASE_COLOR_STEP_PER_PIXEL + self.beat_count * CHASE_COLOR_STEP_PER_BEAT) % 256
                elif self.active_direction == "left":
                    beat_position = (1.0 - phase) * self.width
                    distance = abs(x - beat_position)
                    color_pos = ((self.width - x) * CHASE_COLOR_STEP_PER_PIXEL + self.beat_count * CHASE_COLOR_STEP_PER_BEAT) % 256
                elif self.active_direction == "down":
                    beat_position = phase * self.height
                    distance = abs(y - beat_position)
                    color_pos = (y * CHASE_COLOR_STEP_PER_PIXEL + self.beat_count * CHASE_COLOR_STEP_PER_BEAT) % 256
                else:  # up
                    beat_position = (1.0 - phase) * self.height
                    distance = abs(y - beat_position)
                    color_pos = ((self.height - y) * CHASE_COLOR_STEP_PER_PIXEL + self.beat_count * CHASE_COLOR_STEP_PER_BEAT) % 256

                # Sharp, bright chase with longer tail
                if distance < CHASE_CENTER_WIDTH:
                    brightness = CHASE_BRIGHTNESS_CENTER
                elif distance < CHASE_TAIL_LENGTH:
                    brightness = CHASE_BRIGHTNESS_TAIL - (distance - CHASE_CENTER_WIDTH) / 10.0
                else:
                    brightness = CHASE_BRIGHTNESS_BACKGROUND

                color = scale_color(wheel(color_pos), brightness)

                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        return True
