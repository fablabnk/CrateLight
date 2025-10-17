"""Scrolling color effects"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS
from ..utils import wheel

# Constants for rainbow scroll
RAINBOW_SCROLL_VERTICAL_COLOR_STEP = 50  # Color gradient spread for vertical
RAINBOW_SCROLL_HORIZONTAL_COLOR_STEP = 12  # Color gradient spread for horizontal
RAINBOW_SCROLL_BASE_BPM = 120.0  # Baseline BPM for speed scaling


class RainbowScroll(Effect, BPMSyncedEffect):
    """
    Smooth rainbow scroll effect - SYNCED TO BEAT PHASE!
    Movement is now locked to the beat for perfect timing

    Usage:
        manager.add_effect(RainbowScroll, beats=16, axis="horizontal", speed=1.5)
        manager.add_effect(RainbowScroll, beats=16, axis="vertical", speed=1.0, direction=-1)
        manager.add_effect(RainbowScroll, beats=16, axis="random", speed=1.0)  # Random axis each time
        manager.add_effect(RainbowScroll, beats=16, axis="horizontal", direction="random")  # Random dir
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 axis="horizontal", direction=1, speed=1.0):
        """
        Args:
            axis: "horizontal", "vertical", or "random"
            direction: 1 for right/up, -1 for left/down, or "random"
            speed: Scroll speed multiplier (cycles per beat)
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.axis = axis.lower()
        self.direction = direction
        self.speed = speed

    def setup(self):
        self.beat_count = 0
        self.offset = 0.0

        # Pick random axis if requested
        if self.axis == "random":
            self.active_axis = random.choice(["horizontal", "vertical"])
        else:
            self.active_axis = self.axis

        # Pick random direction if requested
        if self.direction == "random":
            self.active_direction = random.choice([1, -1])
        else:
            self.active_direction = self.direction

    def update(self):
        # Track beats for full cycle offset
        if self.beat_occurred():
            self.beat_count += 1

        # Use beat phase to create smooth movement locked to beat
        phase = self.get_beat_phase()
        # Offset combines beat count (for continuous scrolling) with phase (for smooth interpolation)
        self.offset = (self.beat_count + phase) * self.speed * 256 / 16  # 16 pixels per full color cycle

        # Fill entire grid
        for y in range(self.height):
            for x in range(self.width):
                if self.active_axis == "vertical":
                    # Vertical scroll - colors change by row
                    color_pos = int((y * RAINBOW_SCROLL_VERTICAL_COLOR_STEP + self.offset * self.active_direction) % 256)
                else:
                    # Horizontal scroll - colors change by column
                    color_pos = int((x * RAINBOW_SCROLL_HORIZONTAL_COLOR_STEP + self.offset * self.active_direction) % 256)

                color = wheel(color_pos)
                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])
