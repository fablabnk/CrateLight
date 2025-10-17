"""Sparkle and twinkle effects"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS, get_random_color
from ..utils import wheel

# Constants
SPARKLE_DECAY_RATE = 0.15  # How fast sparkles fade (0.0-1.0)
SPARKLE_MIN_BRIGHTNESS = 0.1  # Minimum brightness before pixel turns off
SPARKLE_PIXELS_PER_BEAT = 8  # Number of new sparkles added per beat
SPARKLE_RAINBOW_HUE_STEP = 30  # Hue change per beat in rainbow mode


class SparkleEffect(Effect, BPMSyncedEffect):
    """
    Random pixels light up on beats and fade out - like stars twinkling!

    Usage:
        manager.add_effect(SparkleEffect, beats=16, rainbow=True)
        manager.add_effect(SparkleEffect, beats=16, random_color=True, density=12)
        manager.add_effect(SparkleEffect, beats=16, color=COLORS["CYAN"])
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 rainbow=False, random_color=False, color=None, density=SPARKLE_PIXELS_PER_BEAT):
        """
        Initialize sparkle effect

        Args:
            rainbow: Cycle through rainbow colors
            random_color: Each sparkle gets random color
            color: Fixed color (overrides other modes)
            density: Number of new sparkles per beat
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.rainbow = rainbow
        self.random_color = random_color
        self.fixed_color = color
        self.density = density

    def setup(self):
        self.num_leds = len(self.pixels)
        # Track brightness and color of each pixel
        self.sparkle_brightness = [0.0] * self.num_leds
        self.sparkle_colors = [(0, 0, 0)] * self.num_leds
        self.rainbow_offset = 0

    def update(self):
        # Add new sparkles on beat
        if self.beat_occurred():
            for _ in range(self.density):
                led_id = random.randint(0, self.num_leds - 1)

                # Pick color based on mode
                if self.fixed_color:
                    color = self.fixed_color
                elif self.random_color:
                    color = get_random_color()
                elif self.rainbow:
                    color = wheel(self.rainbow_offset)
                else:
                    color = COLORS["WHITE"]

                self.sparkle_colors[led_id] = color
                self.sparkle_brightness[led_id] = 1.0

            # Advance rainbow offset
            if self.rainbow:
                self.rainbow_offset = (self.rainbow_offset + SPARKLE_RAINBOW_HUE_STEP) % 256

        # Update all pixels: fade existing sparkles
        for i in range(self.num_leds):
            if self.sparkle_brightness[i] > SPARKLE_MIN_BRIGHTNESS:
                # Fade out
                self.sparkle_brightness[i] *= (1.0 - SPARKLE_DECAY_RATE)

                # Apply brightness to color
                r, g, b = self.sparkle_colors[i]
                brightness = self.sparkle_brightness[i]
                self.pixels[i] = (
                    int(r * brightness),
                    int(g * brightness),
                    int(b * brightness)
                )
            else:
                # Turn off dim pixels
                self.pixels[i] = COLORS["OFF"]
                self.sparkle_brightness[i] = 0.0

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])
